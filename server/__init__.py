from flask import Flask, render_template
import os
import sys


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    sys.path.append(
        os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir, "gquery")
    )
    from gquery_lib import GQueryEngine

    datafile = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), os.pardir, "data/worldcities.csv"
    )
    query_engine = GQueryEngine(datafile)

    @app.route("/")
    @app.route("/index.html")
    def index():
        return render_template("index.html")

    @app.route("/id/<int:city_id>")
    def show_city_info(city_id):
        city_info = {"name": "San Francisco", "population": 900000, "country": "USA"}
        return render_template("city.html", city_info=city_info)

    return app
