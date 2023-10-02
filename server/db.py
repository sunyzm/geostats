from flask import current_app, g
from gquery.engine import GQueryEngine


def get_query_engine() -> GQueryEngine:
    if "query_engine" not in g:
        g.query_engine = GQueryEngine()

    return g.query_engine
