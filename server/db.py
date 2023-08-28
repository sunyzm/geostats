from gquery_lib import GQueryEngine
from flask import current_app, g

def get_query_engine():
    if "query_engine" not in g:
        g.query_engine = GQueryEngine(current_app.config["DATAFILE"])

    return g.query_engine