from chembl_graphql import database


class Builder(object):
    def __init__(self, session):
        self._session = session

    def __enter__(self):
        return self

    def __exit__(self, exception_type, exception, traceback):
        self._session.flush()

    def add_molecule(self, **kwargs):
        return self._add_instance(self._generate_molecule(**kwargs))

    def _generate_molecule(self, **kwargs):
        return database.Molecule(**kwargs)

    def _add_instance(self, instance):
        self._session.add(instance)
