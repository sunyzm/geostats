from absl import app
from absl import flags
from gquery_lib import GQueryEngine
import os

FLAGS = flags.FLAGS
flags.DEFINE_string(
    "data_path",
    os.path.join(
        os.path.dirname(os.path.abspath(__file__)), os.pardir, "data/worldcities.csv"
    ),
    "Path to world city data file.",
)


def main(argv):
    del argv  # Unused.

    if not os.path.exists(FLAGS.data_path):
        raise FileExistsError(f"File '{FLAGS.data_path}' does not exists")

    query_engine = GQueryEngine(FLAGS.data_path, True)
    query_engine.print("New York")
    query_engine.print("san francisco")
    query_engine.print("Utopia City")


if __name__ == "__main__":
    app.run(main)
