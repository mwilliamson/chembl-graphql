import graphlayer as g
import graphlayer.graphql

from . import molecules


Query = g.ObjectType(
    "Query",
    fields=lambda: (
        g.field("molecules", type=g.ListType(molecules.Molecule)),
    ),
)


resolve_query = g.root_object_resolver(Query)


@resolve_query.field(Query.fields.molecules)
def query_resolve_molecules(graph, query, args):
    return graph.resolve(molecules.MoleculeQuery.select(query))


resolvers = (resolve_query, )
