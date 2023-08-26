from flask import Flask, render_template, g, url_for, redirect, request, abort
from gquery_lib import GQueryEngine
import os
import sys


def get_query_engine():
    if "query_engine" not in g:
        datafile = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            os.pardir,
            "data/worldcities.csv",
        )
        g.query_engine = GQueryEngine(datafile)

    return g.query_engine


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route("/", methods=["GET", "POST"])
    @app.route("/index.html", methods=["GET", "POST"])
    def index():
        if request.method == "POST":
            query_engine = get_query_engine()
            city_name = request.form["city1"]
            if not city_name:
                abort(404)

            city_data = query_engine.retrieve(city_name)
            if not city_data:
                abort(404)
            else:
                return redirect(url_for("show_city_info", city_id=city_data['index']))

        return render_template("index.html")

    @app.route("/id/<int:city_id>")
    def show_city_info(city_id):
        city_info = {"name": "Not Found", "population": "NA", "country": "NA"}

        query_engine = get_query_engine()
        city_data = query_engine.get(id=city_id)
        if city_data is not None:
            city_info["name"] = city_data["city"]
            city_info["population"] = city_data["population"]
            city_info["country"] = city_data["country"]

        return render_template("city.html", city_info=city_info)

    return app
