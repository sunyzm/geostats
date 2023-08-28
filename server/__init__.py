from flask import (
    Flask,
    current_app,
    render_template,
    g,
    url_for,
    redirect,
    request,
    abort,
)
from gquery_lib import GQueryEngine, CityInfo
import os


def get_query_engine():
    if "query_engine" not in g:
        g.query_engine = GQueryEngine(current_app.config["DATAFILE"])

    return g.query_engine


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_mapping(
        SECRET_KEY="dev",
        DATAFILE=os.path.join(app.instance_path, "data/worldcities.csv"),
    )

    print("Datafile:", app.config["DATAFILE"])

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
            query_engine = get_query_engine()
            city_name = request.form["city1"]
            if not city_name:
                abort(404)

            city_data = query_engine.retrieve(city_name)
            if not city_data:
                abort(404)
            else:
                return redirect(
                    url_for("show_city_info", city_id=city_data.index)
                )

        return render_template("index.html")

    @app.route("/id/<int:city_id>")
    def show_city_info(city_id):
        query_engine = get_query_engine()
        city_info = query_engine.get(id=city_id)
        if city_info is None:
            abort(404)

        return render_template("city.html", city_info=city_info)

    return app
