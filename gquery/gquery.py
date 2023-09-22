import gquery_lib
import os
import pyinputplus as pyip
import sys


def find_city(
    query_engine: gquery_lib.GQueryEngine, city_name: str
) -> gquery_lib.CityInfo | None:
    matched_cities = query_engine.retrieve(city_name)
    if len(matched_cities) == 0:
        print("No matched city is found.")
        return None
    elif len(matched_cities) == 1:
        return matched_cities[0]
    else:
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
        return matched_cities[selected - 1]


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
                if (
                    matched_city := find_city(query_engine, city_name)
                ) is not None:
                    print(matched_city)
        case ("distance", city1, city2, *extra_arg):
            city_info_1 = find_city(query_engine, city1)
            city_info_2 = find_city(query_engine, city2)
            if city_info_1 is None or city_info_2 is None:
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
                city_info_1.coord, city_info_2.coord, unit
            )
            print(
                f"Distance between {city_info_1.name} and "
                f"{city_info_2.name}: {distance:.1f} {unit_symbol}"
            )
        case _:
            print("Unrecognized arguments")
            exit(1)


if __name__ == "__main__":
    main(sys.argv)
