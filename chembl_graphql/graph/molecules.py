import graphlayer as g
import graphlayer.sqlalchemy as gsql
import graphlayer.graphql

from .. import database


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


resolvers = (resolve_molecule, )
