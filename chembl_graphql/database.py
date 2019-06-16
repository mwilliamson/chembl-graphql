from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class Molecule(Base):
    __tablename__ = "molecule_dictionary"

    molregno = Column(Integer, primary_key=True)
    pref_name = Column(String, nullable=True)
    chembl_id = Column(String, nullable=False)


class MoleculeSynonym(Base):
    __tablename__ = "molecule_synonyms"

    molregno = Column(Integer, ForeignKey(Molecule.molregno), nullable=False)
    molecule = relationship(Molecule)
    molsyn_id = Column(Integer, primary_key=True)
    name = Column("synonyms", String, nullable=True)
