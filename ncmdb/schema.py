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


class CreatePersonSchema(Schema):
    """
    A Colander schema used to validate input for CREATE operations involving
    people.
    """
    name = SchemaNode(String())
    img_uri = SchemaNode(String(), validator=URIValidator(), missing=None)
    producer_credits = _IDSequenceSchema(missing=[])
    director_credits = _IDSequenceSchema(missing=[])
    writer_credits = _IDSequenceSchema(missing=[])
    editor_credits = _IDSequenceSchema(missing=[])
    cast_credits = _IDSequenceSchema(missing=[])
    musician_credits = _IDSequenceSchema(missing=[])


class RetrievePersonSchema(Schema):
    """
    A Colander schema used to validate input for RETRIEVE operations involving
    people.

    NOTE: Declared fields are the only fields returned.
    """
    fields = _PersonFieldsSequenceSchema(missing=[])


class UpdatePersonSchema(CreatePersonSchema):
    """
    A Colander schema used to validate input for UPDATE operations involving
    people.

    NOTE: Overrides `name` field of CreatePersonSchema to make all fields
    optional.
    """
    name = SchemaNode(String(), missing=None)


class CreateFilmSchema(Schema):
    """
    A Colander schema used to validate input for CREATE operations involving
    films.
    """
    title = SchemaNode(String())
    rating = SchemaNode(String(), missing=None)
    year = SchemaNode(Integer(), validator=Range(min=0), missing=None)
    running_time = SchemaNode(Integer(), validator=Range(min=0), missing=None)
    producers = _IDSequenceSchema(missing=[])
    directors = _IDSequenceSchema(missing=[])
    writers = _IDSequenceSchema(missing=[])
    editors = _IDSequenceSchema(missing=[])
    cast = _IDSequenceSchema(missing=[])
    musicians = _IDSequenceSchema(missing=[])
    poster_uri = SchemaNode(String(), validator=URIValidator(), missing=None)
    trailer_uri = SchemaNode(String(), validator=URIValidator(), missing=None)
    wiki_uri = SchemaNode(String(), validator=URIValidator(), missing=None)


class RetrieveFilmSchema(Schema):
    """
    A Colander schema used to validate input for RETRIEVE operations involving
    films.

    NOTE: Declared fields are the only fields returned.
    """
    fields = _FilmFieldsSequenceSchema(missing=[])


class UpdateFilmSchema(CreateFilmSchema):
    """
    A Colander schema used to validate input for UPDATE operations involving
    people.

    NOTE: Overrides `name` field of CreateFilmSchema to make all fields
    optional.
    """
    title = SchemaNode(String(), missing=None)
