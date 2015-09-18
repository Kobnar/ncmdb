__author__ = 'kobnar'

import translationstring
from colander import Schema, SchemaNode, SequenceSchema, String, Integer, \
    Range, OneOf

from .validators import URIValidator
from .models import Person, Film


_ = translationstring.TranslationStringFactory('colander')


_id_node = SchemaNode(Integer(), validator=Range(min=1))


class _IDSequenceSchema(SequenceSchema):
    """
    A flat list of id fields.
    """
    id = _id_node


class _PersonFieldsSequenceSchema(SequenceSchema):
    """
    A SequenceSchema defining a list of acceptable fields for a single person.
    """
    fields = SchemaNode(String(), validator=OneOf(Person.FIELD_CHOICES))


class _FilmFieldsSequenceSchema(SequenceSchema):
    """
    A SequenceSchema defining a list of acceptable fields for a single film.
    """
    fields = SchemaNode(String(), validator=OneOf(Film.FIELD_CHOICES))


class IdSchema(Schema):
    """
    A simple form schema used to validate a resource ID before it is used in a
    query.
    """
    id = _id_node


class CreatePersonRowSchema(Schema):
    """
    A Colander schema used to validate input for CREATE operations involving
    people.
    """
    name = SchemaNode(String())
    img_uri = SchemaNode(String(), validator=URIValidator(), missing=None)
    producer_credits = _IDSequenceSchema(missing=None)
    director_credits = _IDSequenceSchema(missing=None)
    writer_credits = _IDSequenceSchema(missing=None)
    editor_credits = _IDSequenceSchema(missing=None)
    cast_credits = _IDSequenceSchema(missing=None)
    musician_credits = _IDSequenceSchema(missing=None)


class RetrievePersonRowSchema(Schema):
    """
    A Colander schema used to validate input for RETRIEVE operations involving
    people.

    NOTE: Declared fields are the only fields returned.
    """
    fields = _PersonFieldsSequenceSchema(missing=None)


class UpdatePersonRowSchema(CreatePersonRowSchema):
    """
    A Colander schema used to validate input for UPDATE operations involving
    people.

    NOTE: This schema is also used for performing RETRIEVE operations on the
    entire table.
    """
    name = SchemaNode(String(), missing=None)


class CreateFilmRowSchema(Schema):
    """
    A Colander schema used to validate input for CREATE operations involving
    films.
    """
    title = SchemaNode(String())
    rating = SchemaNode(String(), missing=None)
    year = SchemaNode(Integer(), validator=Range(min=0), missing=None)
    running_time = SchemaNode(Integer(), validator=Range(min=0), missing=None)
    producers = _IDSequenceSchema(missing=None)
    directors = _IDSequenceSchema(missing=None)
    writers = _IDSequenceSchema(missing=None)
    editors = _IDSequenceSchema(missing=None)
    cast = _IDSequenceSchema(missing=None)
    musicians = _IDSequenceSchema(missing=None)
    poster_uri = SchemaNode(String(), validator=URIValidator(), missing=None)
    trailer_uri = SchemaNode(String(), validator=URIValidator(), missing=None)
    wiki_uri = SchemaNode(String(), validator=URIValidator(), missing=None)


class RetrieveFilmRowSchema(Schema):
    """
    A Colander schema used to validate input for RETRIEVE operations involving
    films.

    NOTE: Declared fields are the only fields returned.
    """
    fields = _FilmFieldsSequenceSchema(missing=[])


class UpdateFilmRowSchema(CreateFilmRowSchema):
    """
    A Colander schema used to validate input for UPDATE operations involving
    people.

    NOTE: This schema is also used for performing RETRIEVE operations on the
    entire table.
    """
    title = SchemaNode(String(), missing=[])
