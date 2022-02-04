import os

from flask import Flask


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'todolist.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from . import db
    db.init_app(app)

    from . import auth
    app.register_blueprint(auth.bp)

    from . import blog
    app.register_blueprint(blog.bp)
    app.add_url_rule('/', endpoint='index')

    @app.route("/")
    def index():
         return redirect(url_for("auth.login"))

    @app.route("/hello")
    def hello():
        return "<p>hello world</p>"

    @app.route("/about")
    def about():
        return "<p>about me</p>"

    @app.route("/add/<date>/<task>")
    def add(date,task):
        return "<p>Added {task} on {date}, returning id</p>"

    @app.route("/markcomplete/<date>/<int:taskid>")
    def markcomplete(date,taskid):
        return "<p>deleted {task} on {date}</p>"

    @app.route("/delete/<date>/<int:taskid>")
    def delete(date,taskid):
        return "<p>deleted {task} on {date}</p>"

    return app