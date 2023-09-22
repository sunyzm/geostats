import gquery_lib
import os
import pyinputplus as pyip
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
        case ("info", *city_names):
            for city_name in city_names:
                matched_cities = query_engine.retrieve(city_name)
                if len(matched_cities) == 1:
                    print(matched_cities[0])
                elif len(matched_cities) > 1:
                    print("There are multiple matches:")
                    for i in range(len(matched_cities)):
                        city_info = matched_cities[i]
                        print(
                            f"{i+1}. {city_info.name} ({city_info.country}, {city_info.admin})"
                        )
                    selected = pyip.inputInt(
                        f"Please select a city [1-{len(matched_cities)}]:",
                        default=1,
                        min=1,
                        max=len(matched_cities) + 1,
                    )
                    print(matched_cities[selected - 1])
        case ("distance", city1, city2, *extra_arg):
            matched_cities_1 = query_engine.retrieve(city1, max_num=1)
            matched_cities_2 = query_engine.retrieve(city2, max_num=1)
            if len(matched_cities_1) == 0 or len(matched_cities_2) == 0:
                exit(1)

            city1, city2 = matched_cities_1[0], matched_cities_2[0]

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
                city1.coord, city2.coord, unit
            )
            print(
                f"Distance between {city1.name} and "
                f"{city2.name}: {distance:.1f} {unit_symbol}"
            )
        case _:
            print("Unrecognized arguments")
            exit(1)


if __name__ == "__main__":
    main(sys.argv)
