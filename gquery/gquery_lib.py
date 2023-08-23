import pandas as pd
import os


class GQueryEngine:
    __worldcity_df = None

    def __init__(self, datafile_path, debug_enabled = False):
        if not os.path.exists(datafile_path):
            raise FileExistsError(f"File '{datafile_path}' does not exists")

        self.__worldcity_df = pd.read_csv(datafile_path)
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
            print(f"{city_name} is not found")
            return None
        
        city_data = matched_rows.iloc[0].to_dict()
        del city_data['city_ascii']
        del city_data['city_normalized']

        return city_data

    def print(self, city_name):     
        city_data = self.retrieve(city_name)
        if city_data is not None:   
            print(city_data)
