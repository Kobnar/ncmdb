__author__ = 'kobnar'

from nose.plugins.attrib import attr
from unittest import TestCase


@attr('schema')
class TestPersonSchema(TestCase):
    """
    Unit tests for :class:`schema.PersonSchema` (including integration tests
    for :class:`schema.IDSequenceSchema`).
    """

    def setUp(self):
        from ..schema import PersonSchema
        self.schema = PersonSchema()
        self.params = {'name': 'Nicolas Cage'}

    def test_name_required(self):
        """PersonSchema raises an exception if no name is provided
        """
        from colander import Invalid
        with self.assertRaises(Invalid):
            self.schema.deserialize({})

    def test_default_output(self):
        """PersonSchema sets appropriate default parameters
        """
        data = self.schema.deserialize(self.params)
        self.assertEqual(data['img_uri'], None)
        self.assertEqual(data['producer_credits'], [])
        self.assertEqual(data['director_credits'], [])
        self.assertEqual(data['writer_credits'], [])
        self.assertEqual(data['editor_credits'], [])
        self.assertEqual(data['cast_credits'], [])
        self.assertEqual(data['musician_credits'], [])

    def test_missing_img_uri_does_not_raise_exception(self):
        """PersonSchema raises an exception for a missing image URI
        """
        from colander import Invalid
        try:
            self.schema.deserialize(self.params)
        except Invalid:
            self.fail('Missing image URI raised an exception.')

    def test_invalid_img_uri_raises_exception(self):
        """PersonSchema raises an exception for an invalid image URI
        """
        self.params['img_uri'] = 'invalid_image_uri'
        from colander import Invalid
        with self.assertRaises(Invalid):
            self.schema.deserialize(self.params)

    def test_zero_id_raises_exception(self):
        """IDSequenceSchema raises exception if an ID is set to 0
        """
        self.params['producer_credits'] = [0]
        from colander import Invalid
        with self.assertRaises(Invalid):
            self.schema.deserialize(self.params)

    def test_duplicate_id_raises_exception(self):
        """IDSequenceSchema raises exception if a duplicate ID is detected
        """
        self.params['producer_credits'] = [1, 1]
        from colander import Invalid
        with self.assertRaises(Invalid):
            self.schema.deserialize(self.params)


@attr('schema')
class TestFilmSchema(TestCase):
    """
    Unit tests for :class:`schema.FilmSchema`.
    """

    def setUp(self):
        from ..schema import FilmSchema
        self.schema = FilmSchema()
        self.params = {'title': 'Leaving Las Vegas'}

    def test_title_required(self):
        """FilmSchema raises an exception if no ttile is provided
        """
        from colander import Invalid
        with self.assertRaises(Invalid):
            self.schema.deserialize({})

    def test_default_output(self):
        """FilmSchema sets appropriate default parameters
        """
        data = self.schema.deserialize(self.params)
        self.assertEqual(data['rating'], None)
        self.assertEqual(data['year'], None)
        self.assertEqual(data['running_time'], None)
        self.assertEqual(data['producers'], [])
        self.assertEqual(data['directors'], [])
        self.assertEqual(data['writers'], [])
        self.assertEqual(data['editors'], [])
        self.assertEqual(data['cast'], [])
        self.assertEqual(data['musicians'], [])
        self.assertEqual(data['poster_uri'], None)
        self.assertEqual(data['trailer_uri'], None)
        self.assertEqual(data['wiki_uri'], None)

    def test_missing_poster_uri_does_not_raise_exception(self):
        """FilmSchema does not raise an exception for a missing poster URI
        """
        from colander import Invalid
        try:
            self.schema.deserialize(self.params)
        except Invalid:
            self.fail('Missing poster URI raised an exception.')

    def test_invalid_poster_uri_raises_exception(self):
        """FilmSchema raises an exception for an invalid poster URI
        """
        self.params['poster_uri'] = 'invalid_poster_uri'
        from colander import Invalid
        with self.assertRaises(Invalid):
            self.schema.deserialize(self.params)

    def test_missing_trailer_uri_does_not_raise_exception(self):
        """FilmSchema does not raise an exception for a missing trailer URI
        """
        from colander import Invalid
        try:
            self.schema.deserialize(self.params)
        except Invalid:
            self.fail('Missing trailer URI raised an exception.')

    def test_invalid_trailer_uri_raises_exception(self):
        """FilmSchema raises an exception for an invalid trailer URI
        """
        self.params['trailer_uri'] = 'invalid_trailer_uri'
        from colander import Invalid
        with self.assertRaises(Invalid):
            self.schema.deserialize(self.params)

    def test_missing_wiki_uri_does_not_raise_exception(self):
        """FilmSchema does not raise an exception for a missing wiki URI
        """
        from colander import Invalid
        try:
            self.schema.deserialize(self.params)
        except Invalid:
            self.fail('Missing wiki URI raised an exception.')

    def test_invalid_wiki_uri_raises_exception(self):
        """FilmSchema raises an exception for an invalid wiki URI
        """
        self.params['wiki_uri'] = 'invalid_wiki_uri'
        from colander import Invalid
        with self.assertRaises(Invalid):
            self.schema.deserialize(self.params)
