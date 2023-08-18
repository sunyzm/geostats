import pandas as pd


class GQueryEngine:
    __worldcity_df = None

    def __init__(self, data_path):
        self.__worldcity_df = pd.read_csv(data_path)
        self.__worldcity_df["city_ascii"] = self.__worldcity_df[
            "city_ascii"
        ].str.lower()
        print("GQueryEngine initalized.")

    def print(self, city_name):
        df = self.__worldcity_df
        print(df[df["city_ascii"] == city_name])
