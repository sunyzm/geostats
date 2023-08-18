from absl import app
from absl import flags
from gquery_lib import GQueryEngine

FLAGS = flags.FLAGS
flags.DEFINE_string("data_path", None, "Path to data files.")


def main(argv):
    del argv  # Unused.

    query_engine = GQueryEngine(FLAGS.data_path + "worldcities.csv")
    query_engine.print("new york")


if __name__ == "__main__":
    app.run(main)
