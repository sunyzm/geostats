import gquery_lib
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

    query_engine = gquery_lib.GQueryEngine(datafile_path)

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
                exit(1)

            unit = gquery_lib.LengthUnit.KM
            for arg in extra_arg:
                if arg.startswith("--unit="):
                    unit_str = arg.split(sep="=", maxsplit=1)[1].lower()
                    match unit_str:
                        case "mi" | "mile":
                            unit = gquery_lib.LengthUnit.MI
                        case "km" | "kilometer":
                            unit = gquery_lib.LengthUnit.KM
                        case _:
                            print(f"Unrecognized unit {unit}")
                            exit(1)

            distance, unit_symbol = gquery_lib.compute_coord_distance(
                city1_data.coord, city2_data.coord, unit
            )
            print(
                f"Distance between {city1_data.name} and "
                f"{city2_data.name}: {distance:.1f} {unit_symbol}"
            )
        case _:
            print("Unrecognized arguments")
            exit(1)


if __name__ == "__main__":
    main(sys.argv)
