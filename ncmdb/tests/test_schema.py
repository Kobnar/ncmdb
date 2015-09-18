__author__ = 'kobnar'

from nose.plugins.attrib import attr
from unittest import TestCase


@attr('schema')
class IDSchemaTests(TestCase):
    """
    Unit tests for :class:`schema.IdSchema
    """

    def setUp(self):
        from ..schema import IdSchema
        self.schema = IdSchema()

    def test_int_works(self):
        """IdSchema.id should pass validation and set a valid ID integer
        """
        params = {'id': 1}
        result = self.schema.deserialize(params)
        self.assertEqual(1, result['id'])

    def test_int_string_cast(self):
        """IdSchema.id should cast an ID string into an int
        """
        params = {'id': '1'}
        result = self.schema.deserialize(params)
        self.assertIsInstance(result['id'], int)
        self.assertEqual(1, result['id'])

    def test_zero_id_raises_exception(self):
        """IdSchema.id should raise an exception for a zero value
        """
        params = {'id': 0}
        from colander import Invalid
        with self.assertRaises(Invalid):
            self.schema.deserialize(params)

    def test_negative_id_raises_exception(self):
        """IdSchema.id should raise an exception for negative IDs
        """
        params = {'id': -1}
        from colander import Invalid
        with self.assertRaises(Invalid):
            self.schema.deserialize(params)


@attr('schema')
class CreatePersonSchemaTests(TestCase):
    """
    Unit tests for :class:`schema.CreatePersonRowSchema` (including integration
    tests for :class:`schema._IDSequenceSchema`).
    """

    def setUp(self):
        from ..schema import CreatePersonRowSchema
        self.schema = CreatePersonRowSchema()
        self.params = {'name': 'Nicolas Cage'}

    def test_name_required(self):
        """CreatePersonRowSchema raises an exception if no name is provided
        """
        from colander import Invalid
        with self.assertRaises(Invalid):
            self.schema.deserialize({})

    def test_default_output(self):
        """CreatePersonRowSchema sets appropriate default parameters
        """
        data = self.schema.deserialize(self.params)
        self.assertEqual(data['img_uri'], None)
        self.assertEqual(data['producer_credits'], None)
        self.assertEqual(data['director_credits'], None)
        self.assertEqual(data['writer_credits'], None)
        self.assertEqual(data['editor_credits'], None)
        self.assertEqual(data['cast_credits'], None)
        self.assertEqual(data['musician_credits'], None)

    def test_missing_img_uri_does_not_raise_exception(self):
        """CreatePersonRowSchema raises an exception for a missing image URI
        """
        from colander import Invalid
        try:
            self.schema.deserialize(self.params)
        except Invalid as err:
            self.fail(err.msg)

    def test_invalid_img_uri_raises_exception(self):
        """CreatePersonRowSchema raises an exception for an invalid image URI
        """
        self.params['img_uri'] = 'invalid_image_uri'
        from colander import Invalid
        with self.assertRaises(Invalid):
            self.schema.deserialize(self.params)

    def test_zero_id_raises_exception(self):
        """CreatePersonRowSchema.producer_credits raises exception if an ID is set to 0
        """
        self.params['producer_credits'] = [0]
        from colander import Invalid
        with self.assertRaises(Invalid):
            self.schema.deserialize(self.params)

    def test_duplicate_id_raises_exception(self):
        """CreatePersonRowSchema.producer_credits raises exception if a duplicate ID is detected (ON HOLD)
        """
        self.params['producer_credits'] = [1, 1]
        from colander import Invalid
        with self.assertRaises(Invalid):
            self.schema.deserialize(self.params)


@attr('schema')
class RetrievePersonSchemaTests(TestCase):
    """
    Unit tests for :class:`schema.RetrievePersonRowSchema`.
    """

    def setUp(self):
        from ..schema import RetrievePersonRowSchema
        self.schema = RetrievePersonRowSchema()

    def test_no_fields_work(self):
        """RetrievePersonRowSchema does not raise an exception if no fields are provided
        """
        from colander import Invalid
        try:
            self.schema.deserialize({})
        except Invalid as err:
            self.fail(err.msg)

    def test_invalid_field_raises_exception(self):
        """RetrievePersonRowSchema raises an exception if invalid fields are set
        """
        params = {'fields': 'invalid_field'}
        from colander import Invalid
        with self.assertRaises(Invalid):
            self.schema.deserialize(params)

    def test_valid_fields_work(self):
        """RetrievePersonRowSchema does not raise an exception for any valid fields
        """
        from ..models import Person
        field_choices = Person.FIELD_CHOICES
        params = {'fields': field_choices}
        from colander import Invalid
        try:
            self.schema.deserialize(params)
        except Invalid as err:
            self.fail(err.msg)


@attr('schema')
class UpdatePersonSchemaTests(TestCase):
    """
    Unit tests for :class:`schema.UpdatePersonRowSchema` (only includes overridden
    fields).
    """

    def setUp(self):
        from ..schema import UpdatePersonRowSchema
        self.schema = UpdatePersonRowSchema()

    def test_nothing_mandatory(self):
        """UpdatePersonRowSchema does not require a name field
        """
        from colander import Invalid
        try:
            self.schema.deserialize({})
        except Invalid as err:
            self.fail(err.msg)

    def test_missing_name_sets_default(self):
        """UpdatePersonRowSchema sets a missing name field to a reasonable default
        """
        result = self.schema.deserialize({})
        self.assertEqual(None, result['name'])


@attr('schema')
class CreateFilmSchemaTests(TestCase):
    """
    Unit tests for :class:`schema.CreateFilmRowSchema`.
    """

    def setUp(self):
        from ..schema import CreateFilmRowSchema
        self.schema = CreateFilmRowSchema()
        self.params = {'title': 'Leaving Las Vegas'}

    def test_title_required(self):
        """CreateFilmRowSchema raises an exception if no ttile is provided
        """
        from colander import Invalid
        with self.assertRaises(Invalid):
            self.schema.deserialize({})

    def test_default_output(self):
        """CreateFilmRowSchema sets appropriate default parameters
        """
        data = self.schema.deserialize(self.params)
        self.assertEqual(data['rating'], None)
        self.assertEqual(data['year'], None)
        self.assertEqual(data['running_time'], None)
        self.assertEqual(data['producers'], None)
        self.assertEqual(data['directors'], None)
        self.assertEqual(data['writers'], None)
        self.assertEqual(data['editors'], None)
        self.assertEqual(data['cast'], None)
        self.assertEqual(data['musicians'], None)
        self.assertEqual(data['poster_uri'], None)
        self.assertEqual(data['trailer_uri'], None)
        self.assertEqual(data['wiki_uri'], None)

    def test_missing_poster_uri_does_not_raise_exception(self):
        """CreateFilmRowSchema does not raise an exception for a missing poster URI
        """
        from colander import Invalid
        try:
            self.schema.deserialize(self.params)
        except Invalid:
            self.fail('Missing poster URI raised an exception.')

    def test_invalid_poster_uri_raises_exception(self):
        """CreateFilmRowSchema raises an exception for an invalid poster URI
        """
        self.params['poster_uri'] = 'invalid_poster_uri'
        from colander import Invalid
        with self.assertRaises(Invalid):
            self.schema.deserialize(self.params)

    def test_missing_trailer_uri_does_not_raise_exception(self):
        """CreateFilmRowSchema does not raise an exception for a missing trailer URI
        """
        from colander import Invalid
        try:
            self.schema.deserialize(self.params)
        except Invalid:
            self.fail('Missing trailer URI raised an exception.')

    def test_invalid_trailer_uri_raises_exception(self):
        """CreateFilmRowSchema raises an exception for an invalid trailer URI
        """
        self.params['trailer_uri'] = 'invalid_trailer_uri'
        from colander import Invalid
        with self.assertRaises(Invalid):
            self.schema.deserialize(self.params)

    def test_missing_wiki_uri_does_not_raise_exception(self):
        """CreateFilmRowSchema does not raise an exception for a missing wiki URI
        """
        from colander import Invalid
        try:
            self.schema.deserialize(self.params)
        except Invalid:
            self.fail('Missing wiki URI raised an exception.')

    def test_invalid_wiki_uri_raises_exception(self):
        """CreateFilmRowSchema raises an exception for an invalid wiki URI
        """
        self.params['wiki_uri'] = 'invalid_wiki_uri'
        from colander import Invalid
        with self.assertRaises(Invalid):
            self.schema.deserialize(self.params)


@attr('schema')
class RetrieveFilmSchemaTests(TestCase):
    """
    Unit tests for :class:`schema.RetrieveFilmRowSchema`.
    """

    def setUp(self):
        from ..schema import RetrieveFilmRowSchema
        self.schema = RetrieveFilmRowSchema()

    def test_no_fields_work(self):
        """RetrieveFilmRowSchema does not raise an exception if no fields are provided
        """
        from colander import Invalid
        try:
            self.schema.deserialize({})
        except Invalid as err:
            self.fail(err.msg)

    def test_invalid_field_raises_exception(self):
        """RetrieveFilmRowSchema raises an exception if invalid fields are set
        """
        params = {'fields': 'invalid_field'}
        from colander import Invalid
        with self.assertRaises(Invalid):
            self.schema.deserialize(params)

    def test_valid_fields_work(self):
        """RetrieveFilmRowSchema does not raise an exception for any valid fields
        """
        from ..models import Film
        field_choices = Film.FIELD_CHOICES
        params = {'fields': field_choices}
        from colander import Invalid
        try:
            self.schema.deserialize(params)
        except Invalid as err:
            self.fail(err.msg)


@attr('schema')
class UpdateFilmSchemaTests(TestCase):
    """
    Unit tests for :class:`schema.UpdateFilmRowSchema` (only includes overridden
    fields).
    """

    def setUp(self):
        from ..schema import UpdateFilmRowSchema
        self.schema = UpdateFilmRowSchema()

    def test_nothing_mandatory(self):
        """UpdateFilmRowSchema does not require a title field
        """
        from colander import Invalid
        try:
            self.schema.deserialize({})
        except Invalid as err:
            self.fail(err.msg)

    def test_missing_title_sets_default(self):
        """UpdateFilmRowSchema sets a missing title field to a reasonable default
        """
        result = self.schema.deserialize({})
        self.assertEqual(None, result['title'])
