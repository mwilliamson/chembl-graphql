import graphlayer as g
import sqlalchemy.orm

from . import molecules, query


_resolvers = (
    molecules.resolvers,
    query.resolvers,
)


_graph_definition = g.define_graph(resolvers=_resolvers)


def create_graph(*, session):
    return _graph_definition.create_graph({sqlalchemy.orm.Session: session})


Query = query.Query
