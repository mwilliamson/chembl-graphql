import graphlayer.graphql

from .graph import create_graph, Query


_executor = graphlayer.graphql.executor(query_type=Query)


def execute(query, *, session, variables=None):
    graph = create_graph(session=session)
    return _executor(query, graph=graph, variables=variables)
