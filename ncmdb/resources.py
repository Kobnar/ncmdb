__author__ = 'kobnar'

from sqlalchemy import insert, update, delete

from .models import DBSession, Person, Film


class RootResource(object):
    """
    A base resource used for Pyramid's traversal URL handling system.
    """

    def __init__(self, parent, name):
        self.__parent__ = parent
        self.__name__ = name
        self._items = {}

    def __getitem__(self, item):
        return self._items[item]

    def __setitem__(self, name, cls):
        child = cls(self, name)
        self._items[name] = child


class RowResource(RootResource):
    """
    A base resource used to RETRIEVE, UPDATE and DELETE row-level data from
    SQLite.

    NOTE This class must be sub-classed to work properly.
    """

    def __init__(self, parent, row_id, db_session=DBSession):
        self._db = db_session
        RootResource.__init__(self, parent, row_id)
        self._table = parent.table

    @property
    def id(self):
        return self.__name__

    @property
    def table(self):
        return self._table

    def retrieve(self):
        return self._query.first()

    def update(self, json_doc):
        self._query.update(json_doc)
        self._db.commit()
        return self.retrieve()

    def delete(self):
        self._query.delete()

    @property
    def _query(self):
        return self._db.query(self.table).filter_by(id=self.id)


class TableResource(RootResource):
    """
    A base resource used to CREATE and RETRIEVE table-level data from SQLite.

    NOTE: This class must be sub-classed to work properly.
    """
    _table = None
    _row_resource = None

    def __init__(self, parent, name, db_session=DBSession):
        self._db = db_session
        super(TableResource, self).__init__(parent, name)

    def __getitem__(self, row_id):
        return self._row_resource(self, row_id, self._db)

    @property
    def table(self):
        return self._table

    def create(self, fields_dict):
        row = self.table(**fields_dict)
        self._db.add(row)
        self._db.commit()
        return row

    def retrieve(self, filter_dict=None):
        if not filter_dict:
            filter_dict = {}
        return [x for x in self._db.query(self.table).filter_by(**filter_dict)]


class PersonRowResource(RowResource):
    def __init__(self, *args, **kwargs):
        super(PersonRowResource, self).__init__(*args, **kwargs)


class PersonTableResource(TableResource):
    _table = Person
    _row_resource = PersonRowResource


class FilmRowResource(RowResource):
    def __init__(self, *args, **kwargs):
        super(FilmRowResource, self).__init__(*args, **kwargs)


class FilmTableResource(TableResource):
    _table = Film
    _row_resource = FilmRowResource
