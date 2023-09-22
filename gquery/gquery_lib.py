from dataclasses import dataclass
from enum import Enum
from math import radians, cos, sin, asin, sqrt, floor, isnan
import os
import pandas as pd


def decimal_to_degree(val: float, is_lat: bool) -> str:
    abs_val = abs(val)
    degree = floor(abs_val)
    minute = abs_val - degree
    direction = (
        ("N" if val >= 0 else "S") if is_lat else ("E" if val >= 0 else "W")
    )
    return f"{degree}{chr(176)} {round(minute*60.0)}' {direction}"


@dataclass(frozen=True)
class Coordinate:
    lat: float
    lng: float

    def __str__(self):
        return (
            f"{decimal_to_degree(self.lat, is_lat=True)}, "
            f"{decimal_to_degree(self.lng, is_lat=False)}"
        )


class LengthUnit(Enum):
    KM = 1
    MI = 2


def coord_distance(
    lat1, lat2, lon1, lon2, unit: LengthUnit
) -> tuple[float, str]:
    # Convert from degrees to radians.
    lon1 = radians(lon1)
    lon2 = radians(lon2)
    lat1 = radians(lat1)
    lat2 = radians(lat2)

    # Haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2

    c = 2 * asin(sqrt(a))

    use_mile = unit == LengthUnit.MI
    # Radius of earth.
    r = 3958.8 if use_mile else 6371

    return c * r, "mi" if use_mile else "km"


def compute_coord_distance(
    coord1: Coordinate, coord2: Coordinate, unit: LengthUnit = LengthUnit.KM
) -> tuple[float, str]:
    return coord_distance(
        coord1.lat,
        coord2.lat,
        coord1.lng,
        coord2.lng,
        unit,
    )


@dataclass
class CityInfo:
    index: int
    name: str
    population: float
    population_display: str
    country: str
    admin: str
    coord: Coordinate

    def __init__(self, city_data):
        self.index = city_data["index"]
        self.name = city_data["city"]
        self.population = city_data["population"]
        self.population_display = (
            f"{round(self.population):,}"
            if not isnan(self.population)
            else "NA"
        )
        self.country = city_data["country"]
        self.admin = city_data["admin_name"]
        self.coord = Coordinate(city_data["lat"], city_data["lng"])

    def __str__(self):
        return (
            f"{self.name}\n"
            f"- Coordinates: {self.coord}\n"
            f"- Country: {self.country}\n"
            f"- Administration: {self.admin}\n"
            f"- Population: {self.population_display}"
            # f"\n- Index: {self.index}"
        )


class GQueryEngine:
    __worldcity_df = None

    def __init__(self, datafile_path, debug_enabled=False):
        if not os.path.exists(datafile_path):
            raise FileExistsError(f"File '{datafile_path}' does not exists")

        df = pd.read_csv(datafile_path, header=0, engine="c")
        df = df.assign(index=df.index)
        df.drop(columns=["iso2", "iso3", "capital", "id"], inplace=True)
        df["city_normalized"] = df["city_ascii"].str.lower()

        self.__worldcity_df = df

        if debug_enabled:
            print("GQueryEngine has been initalized.")

    def get(self, id: int) -> CityInfo | None:
        df = self.__worldcity_df
        matched_rows = df[df.index == id]
        if matched_rows.empty:
            print(f"ERROR: City ID {id} is not valid")
            return None

        city_data = matched_rows.iloc[0].to_dict()
        return CityInfo(city_data)

    def retrieve(self, city_name: str, max_num: int = -1) -> list[CityInfo]:
        df = self.__worldcity_df
        matched_rows = df[df["city_normalized"] == city_name.lower()]
        if matched_rows.empty:
            return []

        matched_cities = [
            CityInfo(row.to_dict()) for _, row in matched_rows.iterrows()
        ]
        return matched_cities[:max_num] if max_num > 0 else matched_cities

    def print(self, city_name: str):
        matched_cities = self.retrieve(city_name)
        if len(matched_cities) == 0:
            print(f"{city_name} is not found")
        else:
            print(matched_cities[0])
