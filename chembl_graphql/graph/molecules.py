import base64

import graphlayer as g
import graphlayer.sqlalchemy as gsql
import graphlayer.graphql
import sqlalchemy.orm

from .. import database


Molecule = g.ObjectType(
    "Molecule",
    fields=lambda: (
        g.field("pref_name", type=g.NullableType(g.String)),
        g.field("chembl_id", type=g.String),
        g.field("synonyms", type=g.ListType(MoleculeSynonym)),
    ),
)


class MoleculeQuery(object):
    @staticmethod
    def select(query):
        return gsql.select(query)

    @staticmethod
    def select_by_molregno(query, molregnos):
        return gsql.select(query).by(database.Molecule.molregno, molregnos)


resolve_molecule = gsql.sql_table_resolver(
    Molecule,
    database.Molecule,
    fields=lambda: {
        Molecule.fields.pref_name: gsql.expression(database.Molecule.pref_name),
        Molecule.fields.chembl_id: gsql.expression(database.Molecule.chembl_id),
        Molecule.fields.synonyms: lambda graph, field_query: gsql.join(
            key=database.Molecule.molregno,
            resolve=lambda molregnos: graph.resolve(
                MoleculeSynonymQuery.select_by_molregno(field_query.type_query, molregnos),
            ),
        ),
    },
)


def molecules_connection_field(name):
    return g.field(name, type=MoleculesConnection, params=(
        g.param("after", type=g.NullableType(g.String), default=None),
        g.param("first", type=g.Int),
    ))


MoleculesConnection = g.ObjectType(
    "MoleculesConnection",
    fields=lambda: (
        g.field("edges", type=g.ListType(MoleculeEdge)),
        g.field("page_info", type=PageInfo),
    ),
)


class MoleculesConnectionQuery(object):
    @staticmethod
    def select_field(query, *, args):
        return MoleculesConnectionQuery(type_query=query, first=args.first, after=args.after)

    def __init__(self, *, type_query, first, after):
        self.type = MoleculesConnectionQuery
        self.type_query = type_query
        self.first = first
        self.after = after


@g.dependencies(session=sqlalchemy.orm.Session)
@g.resolver(MoleculesConnectionQuery)
def resolve_molecules_connection(graph, query, *, session):
    build_molecules_connection = g.create_object_builder(query.type_query)

    def fetch_cursors(*, after_cursor, limit):
        query = session.query(database.Molecule.molregno) \
            .order_by(database.Molecule.molregno)

        if after_cursor is not None:
            query = query.filter(database.Molecule.molregno > _decode_cursor(after_cursor))

        query = query.limit(limit)

        return [molregno for molregno, in query]

    edge_cursors = fetch_cursors(after_cursor=query.after, limit=query.first + 1)
    if len(edge_cursors) > query.first:
        edge_cursors = edge_cursors[:-1]
        has_next_page = True
    else:
        has_next_page = False

    @build_molecules_connection.field(MoleculesConnection.fields.edges)
    def field_edges(field_query):

        build_edge = g.create_object_builder(field_query.type_query.element_query)

        @build_edge.getter(MoleculeEdge.fields.cursor)
        def field_cursor(cursor):
            return _encode_cursor(cursor)

        @build_edge.field(MoleculeEdge.fields.node)
        def field_node(field_query):
            edges = graph.resolve(
                MoleculeQuery.select_by_molregno(field_query.type_query, edge_cursors)
            )

            return lambda edge_cursor: edges[edge_cursor]

        return lambda _: [
            build_edge(edge_cursor)
            for edge_cursor in edge_cursors
        ]

    @build_molecules_connection.field(MoleculesConnection.fields.page_info)
    def field_page_info(field_query):
        build_page_info = g.create_object_builder(field_query.type_query)

        @build_page_info.getter(PageInfo.fields.has_next_page)
        def field_has_next_page(_):
            return has_next_page

        @build_page_info.getter(PageInfo.fields.end_cursor)
        def field_end_cursor(_):
            if edge_cursors:
                return _encode_cursor(edge_cursors[-1])
            else:
                return None

        return lambda _: build_page_info(None)

    return build_molecules_connection(None)


def _encode_cursor(cursor):
    return base64.b64encode(str(cursor).encode("ascii")).decode("ascii")


def _decode_cursor(cursor):
    return int(base64.b64decode(cursor.encode("ascii")).decode("ascii"))


MoleculeEdge = g.ObjectType(
    "MoleculeEdge",
    fields=lambda: (
        g.field("cursor", type=g.String),
        g.field("node", type=Molecule),
    ),
)


PageInfo = g.ObjectType(
    "PageInfo",
    fields=lambda: (
        g.field("end_cursor", type=g.NullableType(g.String)),
        g.field("has_next_page", type=g.Boolean),
    ),
)


MoleculeSynonym = g.ObjectType(
    "MoleculeSynonym",
    fields=lambda: (
        g.field("name", type=g.String),
    ),
)


class MoleculeSynonymQuery(object):
    @staticmethod
    def select_by_molregno(query, molregnos):
        return gsql.select(query).by(database.MoleculeSynonym.molregno, molregnos)


resolve_molecule_synonym = gsql.sql_table_resolver(
    MoleculeSynonym,
    database.MoleculeSynonym,
    fields=lambda: {
        MoleculeSynonym.fields.name: gsql.expression(database.MoleculeSynonym.name),
    },
)


resolvers = (
    resolve_molecule,
    resolve_molecules_connection,
    resolve_molecule_synonym,
)
