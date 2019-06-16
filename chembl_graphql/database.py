from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Molecule(Base):
    __tablename__ = "molecule_dictionary"

    molregno = Column(Integer, primary_key=True)
    pref_name = Column(String, nullable=True)
    chembl_id = Column(String, nullable=False)
