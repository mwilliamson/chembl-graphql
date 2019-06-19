import graphlayer as g
import graphlayer.graphql

from . import molecules


Query = g.ObjectType(
    "Query",
    fields=lambda: (
        g.field("molecules", type=g.ListType(molecules.Molecule)),
        molecules.molecules_connection.field("molecules_connection"),
    ),
)


resolve_query = g.root_object_resolver(Query)


@resolve_query.field(Query.fields.molecules)
def query_resolve_molecules(graph, query, args):
    return graph.resolve(molecules.MoleculeQuery.select(query))


@resolve_query.field(Query.fields.molecules_connection)
def query_resolve_molecules_connection(graph, query, args):
    return graph.resolve(molecules.molecules_connection.select_field(query, args=args))


resolvers = (resolve_query, )
