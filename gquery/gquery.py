from absl import app
from absl import flags
from gquery_lib import GQueryEngine
from math import radians, cos, sin, asin, sqrt
import os

FLAGS = flags.FLAGS
flags.DEFINE_string("data_path", None, "Path to data files.")
flags.DEFINE_string("distance", None, "Compute the distance between two cities.")
flags.DEFINE_string("info", None, "Show info of a given city.")
flags.DEFINE_string(
    "compare", None, "Show info of a list of cities, separate by comma."
)


def coord_distance(lat1, lat2, lon1, lon2):
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

    # Radius of earth in kilometers. Use 3956 for miles.
    r = 6371

    return c * r


def main(argv):
    del argv  # Unused.

    # Check the data_path has a trailing backslash.
    if FLAGS.data_path[::-1] != "/":
        FLAGS.data_path += "/"

    file_path = FLAGS.data_path + "worldcities.csv"
    if not os.path.exists(file_path):
        raise FileExistsError(f"File '{file_path}' does not exists")

    query_engine = GQueryEngine(file_path)

    if FLAGS.info is not None:
        city_data = query_engine.retrieve(FLAGS.info)
        if city_data is not None:
            print(city_data)
    elif FLAGS.compare is not None:
        city_names = [s.strip() for s in str(FLAGS.compare).split(",")]
        for city in city_names:
            city_data = query_engine.retrieve(city)
            if city_data is not None:
                print(city_data)
    elif FLAGS.distance is not None:
        city_names = [s.strip() for s in str(FLAGS.distance).split(",")]
        if len(city_names) != 2:
            print("Must specify two cities.")
            return

        city1_data = query_engine.retrieve(city_names[0])
        city2_data = query_engine.retrieve(city_names[1])

        if (city1_data is None) or (city2_data is None):
            return

        distance = coord_distance(
            city1_data["lat"], city2_data["lat"], city1_data["lng"], city2_data["lng"]
        )
        print(
            f"Distance between {city1_data['city']} and {city2_data['city']}: {distance:.1f}km"
        )


if __name__ == "__main__":
    app.run(main)
