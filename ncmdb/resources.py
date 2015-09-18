__author__ = 'kobnar'

from sqlalchemy.exc import IntegrityError

from .models import DBSession, Person, Film


class IndexResource(object):
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


class RowResource(IndexResource):
    """
    A base resource used to RETRIEVE, UPDATE and DELETE row-level data from
    SQLite.

    NOTE This class must be sub-classed to work properly.
    """

    def __init__(self, parent, row_id, db_session=DBSession):
        self._db = db_session
        IndexResource.__init__(self, parent, str(row_id))
        self._table = parent.table

    @property
    def id(self):
        """
        The current row's ID (primary key).
        """
        return int(self.__name__)

    @property
    def table(self):
        """
        The current row's associated table.
        """
        return self._table

    def retrieve(self):
        """
        Fetches the current row from the database.

        :return: An instanced version of the current row
        """
        return self._query.first()

    def update(self, row_data):
        """
        Updates the current row in the database using a specified dict of valid
        parameters.

        NOTE: Only fields explicitly defined in the table's FIELD_CHOICES list
        are accepted as valid parameters.

        :param row_data: A dictionary of row data
        :return: An instanced version of the current row
        """
        valid_data = {k: v for k, v in row_data.items()
                      if k in self.table.FIELD_CHOICES}
        if valid_data:
            self._query.update(valid_data)
            self._db.flush()
            return self.retrieve()

    def delete(self):
        """
        Deletes the current row from the database.

        :return: None
        """
        self._query.delete()

    @property
    def _query(self):
        return self._db.query(self.table).filter_by(id=self.id)


class TableResource(IndexResource):
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
        """
        The current table.
        """
        return self._table

    def create(self, row_data):
        """
        Saves a new row in the current table based on a dictionary of data.

        :param row_data: A dictionary of row data
        :return: An instanced version of the newly created row
        """
        valid_data = {k: v for k, v in row_data.items()
                      if k in self.table.FIELD_CHOICES}
        row_obj = self.table(**valid_data)
        self._db.add(row_obj)
        try:
            self._db.flush()
        except IntegrityError:
            self._db.rollback()
            return None
        return row_obj

    def retrieve(self, row_data=None):
        """
        Fetches every row in the database which matches the given query. If no
        query is provided, dumps every item in the table.

        :param row_data: A dictionary of row data.
        :return: A list of instanced versions of each matching row
        """
        if not row_data:
            valid_data = {}
        else:
            valid_data = {k: v for k, v in row_data.items()
                          if k in self.table.FIELD_CHOICES}
        query = self._db.query(self.table)
        for field, value in valid_data.items():
            query = query.filter(getattr(self.table, field).like('%%%s%%' % value))
        return [x for x in query]


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
