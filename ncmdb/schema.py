__author__ = 'kobnar'

import translationstring
from colander import Invalid, Schema, SchemaNode, SequenceSchema, String,\
    Integer, Range

from .validators import URIValidator

_ = translationstring.TranslationStringFactory('colander')


class IDSequenceSchema(SequenceSchema):
    """
    A flat list of id fields.
    """
    id = SchemaNode(Integer(), validator=Range(min=1))


class PersonSchema(Schema):
    """
    A form handler for any CRUD operations involving people.
    """
    name = SchemaNode(String())
    img_uri = SchemaNode(String(), validator=URIValidator(), missing=None)
    producer_credits = IDSequenceSchema(missing=[])
    director_credits = IDSequenceSchema(missing=[])
    writer_credits = IDSequenceSchema(missing=[])
    editor_credits = IDSequenceSchema(missing=[])
    cast_credits = IDSequenceSchema(missing=[])
    musician_credits = IDSequenceSchema(missing=[])


class FilmSchema(Schema):
    """
    A form handler for any CRUD operations involving films.
    """
    title = SchemaNode(String())
    rating = SchemaNode(String(), missing=None)
    year = SchemaNode(Integer(), validator=Range(min=0), missing=None)
    running_time = SchemaNode(Integer(), validator=Range(min=0), missing=None)
    producers = IDSequenceSchema(missing=[])
    directors = IDSequenceSchema(missing=[])
    writers = IDSequenceSchema(missing=[])
    editors = IDSequenceSchema(missing=[])
    cast = IDSequenceSchema(missing=[])
    musicians = IDSequenceSchema(missing=[])
    poster_uri = SchemaNode(String(), validator=URIValidator(), missing=None)
    trailer_uri = SchemaNode(String(), validator=URIValidator(), missing=None)
    wiki_uri = SchemaNode(String(), validator=URIValidator(), missing=None)
