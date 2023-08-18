import pandas as pd
import os


class GQueryEngine:
    __worldcity_df = None

    def __init__(self, datafile_path):
        if not os.path.exists(datafile_path):
            raise FileExistsError(f"File '{datafile_path}' does not exists")

        self.__worldcity_df = pd.read_csv(datafile_path)
        self.__worldcity_df["city_ascii"] = self.__worldcity_df[
            "city_ascii"
        ].str.lower()
        print("GQueryEngine initalized.")

    def print(self, city_name):
        df = self.__worldcity_df
        print(df[df["city_ascii"] == city_name])
