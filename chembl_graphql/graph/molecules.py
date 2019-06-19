import graphlayer as g
import graphlayer.sqlalchemy as gsql
import graphlayer.graphql
import sqlalchemy.orm

from .. import database
from . import connections


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


@g.dependencies(session=sqlalchemy.orm.Session)
def _fetch_molecule_cursors(*, after_cursor, limit, session):
    query = session.query(database.Molecule.molregno) \
        .order_by(database.Molecule.molregno)

    if after_cursor is not None:
        query = query.filter(database.Molecule.molregno > after_cursor)

    query = query.limit(limit)

    return [molregno for molregno, in query]


molecules_connection = connections.forward_connection(
    connection_type_name="MoleculesConnection",
    node_type=Molecule,
    select_by_cursor=MoleculeQuery.select_by_molregno,
    fetch_cursors=_fetch_molecule_cursors,
    cursor_encoding=connections.int_cursor_encoding,
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
    molecules_connection.resolvers,
    resolve_molecule_synonym,
)
