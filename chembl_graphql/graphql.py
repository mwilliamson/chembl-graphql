import graphlayer as g
import graphlayer.sqlalchemy as gsql
import graphlayer.graphql
import sqlalchemy.orm

from . import database


Molecule = g.ObjectType(
    "Molecule",
    fields=lambda: (
        g.field("chembl_id", type=g.String),
    ),
)


class MoleculeQuery(object):
    @staticmethod
    def select(query):
        return gsql.select(query)


resolve_molecule = gsql.sql_table_resolver(
    Molecule,
    database.Molecule,
    fields=lambda: {
        Molecule.fields.chembl_id: gsql.expression(database.Molecule.chembl_id),
    },
)


Query = g.ObjectType(
    "Query",
    fields=lambda: (
        g.field("molecules", type=g.ListType(Molecule)),
    ),
)


resolve_query = g.root_object_resolver(Query)


@resolve_query.field(Query.fields.molecules)
def query_resolve_molecules(graph, query, args):
    return graph.resolve(MoleculeQuery.select(query))


_resolvers = (resolve_query, resolve_molecule)
_graph_definition = g.define_graph(resolvers=_resolvers)
_executor = graphlayer.graphql.executor(query_type=Query)


def execute(query, *, session):
    graph = _graph_definition.create_graph({sqlalchemy.orm.Session: session})
    return _executor(query, graph=graph)
