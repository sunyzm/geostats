from flask import (
    abort,
    flash,
    Flask,
    redirect,
    render_template,
    request,
    url_for,
)
from gquery_lib import GQueryEngine, CityInfo
from . import db
import os


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_mapping(
        SECRET_KEY="dev",
        DATAFILE=os.path.join(app.instance_path, "data/worldcities.csv"),
    )

    app.logger.info("Datafile: %s", app.config["DATAFILE"])

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

            city_name = request.form["city1"]
            if not city_name:
                flash("Input is empty.")
                return redirect(url_for("index"))

            city_data = query_engine.retrieve(city_name)
            if not city_data:
                flash(f"City \"{city_name}\" is not found.")
                return redirect(url_for("index"))
            else:
                return redirect(
                    url_for("show_city_info", city_id=city_data.index)
                )

        return render_template("index.html")

    @app.route("/id/<int:city_id>")
    def show_city_info(city_id):
        query_engine = db.get_query_engine()
        city_info = query_engine.get(id=city_id)
        if city_info is None:
            abort(404)

        return render_template("city.html", city_info=city_info)

    return app
