from absl import app
from absl import flags
from gquery_lib import GQueryEngine
import os

FLAGS = flags.FLAGS
flags.DEFINE_string("data_path", None, "Path to data files.")


def main(argv):
    del argv  # Unused.

    if FLAGS.data_path[::-1] != "/":
        FLAGS.data_path += "/"

    file_path = FLAGS.data_path + "worldcities.csv"
    if not os.path.exists(file_path):
        raise FileExistsError(f"File '{file_path}' does not exists")


    query_engine = GQueryEngine(file_path)
    query_engine.print("New York")
    query_engine.print("san francisco")
    query_engine.print("Utopia City")


if __name__ == "__main__":
    app.run(main)
