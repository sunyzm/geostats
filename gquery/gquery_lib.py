import pandas as pd
import os


class GQueryEngine:
    __worldcity_df = None

    def __init__(self, datafile_path):
        if not os.path.exists(datafile_path):
            raise FileExistsError(f"File '{datafile_path}' does not exists")

        self.__worldcity_df = pd.read_csv(datafile_path)
        self.__worldcity_df.drop(
            columns=["iso2", "iso3", "capital", "id"], inplace=True
        )
        self.__worldcity_df["city_ascii"] = self.__worldcity_df[
            "city_ascii"
        ].str.lower()
        print("GQueryEngine has been initalized.")

    def retrieve(self, city_name):
        df = self.__worldcity_df

        matched_rows = df[df["city_ascii"] == city_name.lower()]
        if matched_rows.empty:
            print(f"{city_name} is not found")
            return None

        return matched_rows.iloc[0].to_dict()

    def print(self, city_name):     
        city_data = self.retrieve(city_name)
        if city_data != None:   
            print(city_data)
