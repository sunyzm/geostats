import pandas as pd
import os
from math import radians, cos, sin, asin, sqrt


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


def print_city(city_data):
    print(f"[{city_data['city']}]")
    print(f"- Latitude: {city_data['lat']:.2f}")
    print(f"- Longtitude: {city_data['lng']:.2f}")
    print(f"- Country: {city_data['country']}")
    print(f"- Administration: {city_data['admin_name']}")
    print(f"- Population: {int(city_data['population']):,}")


class GQueryEngine:
    __worldcity_df = None

    def __init__(self, datafile_path, debug_enabled=False):
        if not os.path.exists(datafile_path):
            raise FileExistsError(f"File '{datafile_path}' does not exists")

        self.__worldcity_df = pd.read_csv(datafile_path, engine="c")
        self.__worldcity_df = self.__worldcity_df.reset_index()

        self.__worldcity_df.drop(
            columns=["iso2", "iso3", "capital", "id"], inplace=True
        )
        self.__worldcity_df["city_normalized"] = self.__worldcity_df[
            "city_ascii"
        ].str.lower()

        if debug_enabled:
            print("GQueryEngine has been initalized.")

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
