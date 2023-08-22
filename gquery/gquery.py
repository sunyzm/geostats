from absl import app
from absl import flags
from gquery_lib import GQueryEngine
import os

FLAGS = flags.FLAGS
flags.DEFINE_string("data_path", None, "Path to data files.")
flags.DEFINE_string("info", None, "Show info of a given city.")
flags.DEFINE_string("compare", None, "Show info of a list of cities, separate by comma.")

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

if __name__ == "__main__":
    app.run(main)