import os

from graphql import GraphQLError
import flask
import sqlalchemy.orm

from . import graphql


def local_path(path):
    return os.path.join(os.path.dirname(__file__), "..", path)


app = flask.Flask(__name__, static_folder=local_path("static"))


@app.route("/")
def graphiql():
    with open(local_path("graphiql/index.html"), encoding="utf-8") as fileobj:
        return fileobj.read()


@app.route("/graphql", methods=["POST"])
def graphql_api():
    args = flask.request.get_json()

    engine = sqlalchemy.create_engine(os.environ["DATABASE"])
    session = sqlalchemy.orm.Session(engine)
    result = graphql.execute(
        args["query"],
        variables=args.get("variables"),
        session=session,
    )

    return flask.jsonify({
        "data": result.data,
        "errors": list(map(_render_error, result.errors or ())),
    })


def _render_error(error):
    if isinstance(error, GraphQLError):
        return {
            "message": error.message,
            "locations": [
                {"line": location.line, "column": location.column}
                for location in (getattr(error, "locations", None) or [])
            ],
        }
    else:
        return {
            "message": "Internal server error",
        }
