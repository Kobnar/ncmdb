import translationstring
from colander import Schema, SchemaNode, SequenceSchema, String, Integer, \
    Range, OneOf, Sequence, Invalid
from .validators import URIValidator
from .models import Person, Film

__author__ = 'kobnar'

_ = translationstring.TranslationStringFactory('colander')


class URISequenceSchema(SequenceSchema):
    """
    A child of :class:`colander.SequenceSchema` that parses a URI formatted
    list of values into a standard Python list for Colander to work with.

    Example: `'John,Max,Susan'` becomes `['John', 'Max', 'Susan']`
    """
    def _split(self, cstruct):
        if hasattr(cstruct, '__iter__') and not hasattr(cstruct, 'get'):
            if isinstance(cstruct, str):
                return cstruct.split(',')
            return list(cstruct)
        return [cstruct]

    def deserialize(self, cstruct):
        if cstruct:
            cstruct = self._split(cstruct)
        return super(URISequenceSchema, self).deserialize(cstruct)


class _IDNode(SchemaNode):
    """
    An integer representation of a row's primary key ID field.
    """
    schema_type = Integer
    validator = Range(min=1)


class _IDSequenceSchema(URISequenceSchema):
    """
    A list of integers representing one or more primary key IDs for a given
    collection of table rows.
    """
    id = _IDNode()


class IdSchema(Schema):
    """
    A schema to validate a resource ID before it is used to retrieve a specific
    row.
    """
    id = _IDNode()


class _StringSequenceSchema(URISequenceSchema):
    """
    A schema used to deserialize and serialize a list of strings.
    """
    item = SchemaNode(String())


class CreatePersonSchema(Schema):
    """
    A schema to validate row-level input parameters intended to CREATE a
    new person.
    """
    name = SchemaNode(String())
    image_uri = SchemaNode(String(), validator=URIValidator(), missing=None)
    producer_credits = _IDSequenceSchema(missing=None)
    director_credits = _IDSequenceSchema(missing=None)
    writer_credits = _IDSequenceSchema(missing=None)
    editor_credits = _IDSequenceSchema(missing=None)
    cast_credits = _IDSequenceSchema(missing=None)
    musician_credits = _IDSequenceSchema(missing=None)


class _PersonFieldsSequenceSchema(URISequenceSchema):
    """
    A list of field names desired for a specific person or collection of people.
    """
    fields = SchemaNode(String(), validator=OneOf(Person.FIELD_CHOICES))


class RetrievePeopleSchema(Schema):
    """
    A schema to validate table-level query parameters intended to RETRIEVE a
    list of of people by name (as opposed to ID).
    """
    name = SchemaNode(String(), missing=None)
    cast_credit = SchemaNode(String(), missing=None)
    fields = _PersonFieldsSequenceSchema(missing=[])


class RetrievePersonSchema(Schema):
    """
    A schema to validate a desired collection of fields during a RETRIEVE
    operation for a specific person.
    """
    fields = _PersonFieldsSequenceSchema(missing=[])


class UpdatePersonSchema(CreatePersonSchema):
    """
    A schema to validate input parameters intended to UPDATE an existing person.
    """
    name = SchemaNode(String(), missing=None)


class CreateFilmSchema(Schema):
    """
    A schema to validate row-level input parameters intended to CREATE a
    new film.
    """
    title = SchemaNode(String())
    rating = SchemaNode(String(), missing=None)
    year = SchemaNode(Integer(), validator=Range(min=0), missing=None)
    runtime = SchemaNode(Integer(), validator=Range(min=0), missing=None)
    producers = _IDSequenceSchema(missing=None)
    directors = _IDSequenceSchema(missing=None)
    writers = _IDSequenceSchema(missing=None)
    editors = _IDSequenceSchema(missing=None)
    cast = _IDSequenceSchema(missing=None)
    musicians = _IDSequenceSchema(missing=None)
    poster_uri = SchemaNode(String(), validator=URIValidator(), missing=None)
    trailer_uri = SchemaNode(String(), validator=URIValidator(), missing=None)
    wiki_uri = SchemaNode(String(), validator=URIValidator(), missing=None)


class _FilmFieldsSequenceSchema(URISequenceSchema):
    """
    A list of field names desired for a specific film or collection of films.
    """
    fields = SchemaNode(String(), validator=OneOf(Film.FIELD_CHOICES))


class RetrieveFilmsSchema(Schema):
    """
    A schema to validate table-level query parameters intended to RETRIEVE a
    list of of films by name (as opposed to ID).
    """
    title = SchemaNode(String(), missing=None)
    cast = SchemaNode(String(), missing=None)
    fields = _FilmFieldsSequenceSchema(missing=[])


class RetrieveFilmSchema(Schema):
    """
    A schema to validate a desired collection of fields during a RETRIEVE
    operation for a specific film.
    """
    fields = _FilmFieldsSequenceSchema(missing=[])


class UpdateFilmSchema(CreateFilmSchema):
    """
    A schema to validate input parameters intended to UPDATE an existing film.
    """
    title = SchemaNode(String(), missing=None)
