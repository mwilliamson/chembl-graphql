import graphlayer as g
import graphlayer.sqlalchemy as gsql
import graphlayer.graphql

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


resolvers = (resolve_molecule, resolve_molecule_synonym)
