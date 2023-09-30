from absl import app
from gquery.engine import GQueryEngine

def main(argv):
    del argv  # Unused.

    query_engine = GQueryEngine(debug_enabled=True)
    query_engine.print("New York")
    query_engine.print("san francisco")
    query_engine.print("Utopia City")


if __name__ == "__main__":
    app.run(main)
