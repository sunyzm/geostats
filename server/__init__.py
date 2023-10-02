from flask import (
    abort,
    flash,
    Flask,
    redirect,
    render_template,
    request,
    url_for,
)
from . import db
from gquery.coordinate import compute_coord_distance, LengthUnit
import os


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_mapping(
        SECRET_KEY="dev",
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile("config.py", silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route("/", methods=["GET", "POST"])
    @app.route("/index.html", methods=["GET", "POST"])
    def index():
        if request.method == "POST":
            query_engine = db.get_query_engine()

            city_name = request.form["city1"].strip()
            if not city_name:
                flash("Input is empty.")
                return redirect(url_for("index"))

            cities = query_engine.retrieve(city_name)
            if len(cities) == 0:
                flash(f'City "{city_name}" is not found.')
                return redirect(url_for("index"))
            else:
                return redirect(
                    url_for("show_city_info", city_id=cities[0].index)
                )

        return render_template("index.html")

    @app.route("/compare.html", methods=["GET", "POST"])
    def compare():
        if request.method == "POST":
            query_engine = db.get_query_engine()

            city_names = [
                city.strip()
                for city in [request.form["city1"], request.form["city2"]]
            ]
            for city in city_names:
                if not city:
                    flash("Input is empty.")
                    return redirect(url_for("compare"))

            cities_and_info = [
                (city, query_engine.retrieve(city, max_num=1))
                for city in city_names
            ]
            for city, info in cities_and_info:
                if len(info) == 0:
                    flash(f'City "{city}" is not found.')
                    return redirect(url_for("compare"))

            distance, unit = compute_coord_distance(
                cities_and_info[0][1][0].coord,
                cities_and_info[1][1][0].coord,
                unit=LengthUnit.KM,
            )
            dist_display = f"{distance:.1f} {unit}"

            return render_template(
                "show_comparison.html",
                cities_info=[info[0] for (_, info) in cities_and_info],
                dist_display=dist_display,
            )

        return render_template("compare.html")

    @app.route("/id/<int:city_id>")
    def show_city_info(city_id):
        query_engine = db.get_query_engine()
        city_info = query_engine.get(id=city_id)
        if city_info is None:
            abort(404)

        return render_template("city.html", city_info=city_info)

    return app
