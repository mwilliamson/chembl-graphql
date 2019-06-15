import pytest
import sqlalchemy.orm

from chembl_graphql import database
from chembl_graphql.graphql import execute
from .builder import Builder


@pytest.fixture(name="builder")
def fixture_builder(session):
    return Builder(session=session)


@pytest.fixture(name="session")
def fixture_session():
    engine = sqlalchemy.create_engine("sqlite:///:memory:")
    database.Base.metadata.create_all(engine)
    return sqlalchemy.orm.Session(engine)


@pytest.fixture(name="graphql")
def fixture_graphql(session):
    def graphql(*args, **kwargs):
        result = execute(*args, **kwargs, session=session)
        if result.errors:
            raise result.errors[0]
        else:
            return result.data

    return graphql
