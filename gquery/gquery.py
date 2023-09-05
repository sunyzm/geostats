from gquery_lib import GQueryEngine, coord_distance
import os
import sys


def main(argv):
    datafile_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        os.pardir,
        "data/worldcities.csv",
    )
    if not os.path.exists(datafile_path):
        raise FileExistsError(f"File '{datafile_path}' does not exists")

    query_engine = GQueryEngine(datafile_path)

    match argv[1:]:
        case ("info", *city):
            city_name = " ".join(city)
            city_info = query_engine.retrieve(city_name)
            if city_info is not None:
                print(city_info)
        case ("compare", *city_names):
            for city in city_names:
                city_info = query_engine.retrieve(city)
                if city_info is not None:
                    print(city_info)
        case ("distance", city1, city2, *extra_arg):
            city1_data = query_engine.retrieve(city1)
            city2_data = query_engine.retrieve(city2)
            if (city1_data is None) or (city2_data is None):
                return

            use_mile = (len(extra_arg) > 0) and (extra_arg[0] == "--unit=mi")

            distance = coord_distance(
                city1_data.lat,
                city2_data.lat,
                city1_data.lng,
                city2_data.lng,
                use_mile,
            )
            print(
                f"Distance between {city1_data.name} and "
                f"{city2_data.name}: {distance:.1f} "
                + ("mi" if use_mile else "km")
            ) 
        case _:
            raise ValueError("Unrecognized arguments")


if __name__ == "__main__":
    main(sys.argv)
