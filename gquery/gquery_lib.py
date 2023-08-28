import pandas as pd
import os
from math import radians, cos, sin, asin, sqrt, floor


def coord_distance(lat1, lat2, lon1, lon2, use_mile=False):
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

    # Radius of earth.
    r = 3958.8 if use_mile else 6371

    return c * r


def decimal_to_degree(val, is_lat):
    abs_val = abs(val)
    degree = floor(abs_val)
    minute = abs_val - degree
    direction = (
        ("N" if val >= 0 else "S") if is_lat else ("E" if val >= 0 else "W")
    )
    return f"{degree}{chr(176)} {round(minute*60.0)}' {direction}"


def print_city(city_data):
    print(f"[{city_data['city']}]")
    # print(f"- Latitude: {city_data['lat']:.2f}")
    # print(f"- Longtitude: {city_data['lng']:.2f}")
    lat = city_data["lat"]
    lng = city_data["lng"]
    print(
        f"- Coordinates: {decimal_to_degree(lat, is_lat=True)}, {decimal_to_degree(lng, is_lat=False)}"
    )
    print(f"- Country: {city_data['country']}")
    print(f"- Administration: {city_data['admin_name']}")
    print(f"- Population: {int(city_data['population']):,}")
    print(f"- Index: {city_data['index']}")


class CityInfo:
    def __init__(self, city_data):
        self.index = city_data["index"]
        self.name = city_data["city"]
        self.population = int(city_data["population"])
        self.country = city_data["country"]
        self.admin = city_data["admin_name"]
        self.lat = city_data["lat"]
        self.lng = city_data["lng"]
        self.coord = f"{decimal_to_degree(self.lat, is_lat=True)}, {decimal_to_degree(self.lng, is_lat=False)}"


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

    def get(self, id):
        df = self.__worldcity_df
        matched_rows = df[df.index == id]
        if matched_rows.empty:
            print(f"Error: City ID {id} is not valid")
            return None

        city_data = matched_rows.iloc[0].to_dict()
        del city_data["city_ascii"]
        del city_data["city_normalized"]

        return city_data

    def retrieve(self, city_name):
        df = self.__worldcity_df
        matched_rows = df[df["city_normalized"] == city_name.lower()]
        if matched_rows.empty:
            print(f"ERROR: {city_name} is not found")
            return None

        city_data = matched_rows.iloc[0].to_dict()
        del city_data["city_ascii"]
        del city_data["city_normalized"]

        return city_data

    def print(self, city_name):
        city_data = self.retrieve(city_name)
        if city_data is not None:
            print_city(city_data)
