from sqlalchemy import or_
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import joinedload, aliased
from .models import DBSession, Person, Film

__author__ = 'kobnar'


class IndexResource(object):
    """
    A base resource used for Pyramid's traversal URL handling system.

    Raises an exception if `parent` is neither an instance of
    :class:`.IndexResource` nor `None` and if `name` is not a string.
    """

    def __init__(self, parent, name):
        if not (parent is None or isinstance(parent, IndexResource))\
                or not (isinstance(name, str)):
            raise TypeError()
        self.__parent__ = parent
        self.__name__ = name
        self._items = {}

    def __setitem__(self, name, cls):
        """
        Adds a child resource to the traversal tree.

        Raises an exception if `cls` is not a type of IndexResource.
        """
        child = cls(self, name)
        if not isinstance(child, IndexResource):
            raise TypeError()
        self._items[name] = child

    def __getitem__(self, item):
        return self._items[item]


class _SQLResource(IndexResource):
    """
    A base resource containing common methods for both :class:`.RowResource`
    and :class:`.TableResource`.
    """

    @property
    def table(self):
        """
        The current table.
        """
        return self._table

    def _validate_data(self, row_data):
        valid_fields = self.table.FIELD_CHOICES
        return {k: v for k, v in row_data.items()
                if k in valid_fields and v}


class RowResource(_SQLResource):
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

    def retrieve(self):
        """
        Fetches the current row from the database.

        :return: An instanced version of the current row
        """
        return self.query.first()

    def update(self, row_data):
        """
        Updates the current row in the database using a specified dict of valid
        parameters.

        NOTE: Only fields explicitly defined in the table's FIELD_CHOICES list
        are accepted as valid parameters.

        :param row_data: A dictionary of row data
        :return: An instanced version of the current row
        """
        valid_data = self._validate_data(row_data)
        if valid_data:
            valid_data['id'] = self.id
            self.query.update(valid_data)
            self._db.flush()
            return self.retrieve()

    def delete(self):
        """
        Deletes the current row from the database.

        :return: None
        """

        self.query.delete()

    @property
    def session(self):
        return self._db

    @property
    def query(self):
        return self.session.query(self.table).\
            filter_by(id=self.id)


class TableResource(_SQLResource):
    """
    A base resource used to CREATE and RETRIEVE table-level data from SQLite.

    NOTE: This class must be sub-classed to work properly.
    """

    _table = None
    _row_resource = RowResource

    def __init__(self, parent, name, db_session=DBSession):
        self._db = db_session
        super(TableResource, self).__init__(parent, name)

    def __getitem__(self, name):
        """
        Attempts to use ``name`` as an integer to instantiate a specific
        row-level resource. If ``name`` is not a valid integer, it will call
        ``getitem__()`` of :class:`.IndexResource` to resolve the route.
        """
        try:
            name = int(name)
        except ValueError:
            return super(TableResource, self).__getitem__(name)
        return self._row_resource(self, name, self._db)

    def create(self, row_data):
        """
        Saves a new row in the current table based on a dictionary of data.

        :param row_data: A dictionary of row data
        :return: An instanced version of the newly created row
        """
        assert row_data
        valid_data = self._validate_data(row_data)
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

        :param row_data: A dictionary of row data
        :return: A list of instanced versions of each matching row
        """
        if not row_data:
            row_data = {}
        return self.filter(row_data).all()

    def filter(self, row_data):
        """
        Applies filters to the query based on desired row data.

        NOTE: The default filter is very greedy and will blast any matching
        parameter out to the interblag.

        :param row_data: A dictionary of row data
        :return: A filtered query object
        """
        query = self.query
        for field, value in row_data.items():
            query = query.filter(
                getattr(self.table, field).like('%%%s%%' % value))
        return query

    @property
    def session(self):
        return self._db

    @property
    def query(self):
        """
        A default, aggressively loaded query object.
        """
        return self.session.query(self.table)


class PersonRowResource(RowResource):
    def __init__(self, *args, **kwargs):
        super(PersonRowResource, self).__init__(*args, **kwargs)


class PersonTableResource(TableResource):
    _table = Person
    _row_resource = PersonRowResource

    def filter(self, row_data):
        """
        Filters query based on the specific needs of fetching a list of people.
        """

        # Get query:
        query = self.query

        # Join relationships:
        query = query.options(joinedload('*'))

        # Query all people with a similar 'name':
        name = row_data.get('name')
        if name:
            query = self.query.filter(
                Person.name.like('%%{}%%'.format(name)))

        # Query all people with any similar 'cast_credit':
        cast_cred = row_data.get('cast_credit')
        if cast_cred:
            # TODO: Load all credits, not just cast credits
            # aliases = []
            # for field in cred_fields:
            #     alias = aliased(Film)
            #     attribute = getattr(Person, field)
            #     query = query.options(joinedload(attribute))
            #     query = query.join(alias, attribute)
            #     aliases.append(alias)
            # cond = or_(x.title.like('%%{}%%'.format(cred)) for x in aliases)
            # query = query.filter(cond)
            query = query.join(
                Film, Person.cast_credits)
            query = query.filter(
                Film.title.like('%%{}%%'.format(cast_cred)))

        return query


class FilmRowResource(RowResource):
    def __init__(self, *args, **kwargs):
        super(FilmRowResource, self).__init__(*args, **kwargs)


class FilmTableResource(TableResource):
    _table = Film
    _row_resource = FilmRowResource

    def filter(self, row_data):
        """
        Filters query based on the specific needs of fetching a list of films.
        """

        # Get query:
        query = self.query

        # Join relationships:
        query = query.options(joinedload('*'))

        # Filter films with a similar 'title':
        title = row_data.get('title')
        if title:
            query = query.filter(
                Film.title.like('%%{}%%'.format(title)))

        # Filter films with matching 'cast_credit':
        cast_cred = row_data.get('cast_credit')
        if cast_cred:
            # TODO: Load all credits not just cast credits
            query = query.join(
                Person, Film.cast)
            query = query.filter(
                Person.name.like('%%{}%%'.format(cast_cred)))

        return query
