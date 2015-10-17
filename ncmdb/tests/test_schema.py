from nose.plugins.attrib import attr
from unittest import TestCase

__author__ = 'kobnar'


class URISequenceSchemaTests(TestCase):
    """
    Unit tests for :class:`schema.URISequenceSchema` using a mock schema to
    test various field types.
    """
    from ..schema import URISequenceSchema

    class IntUriSequenceSchema(URISequenceSchema):
        from colander import SchemaNode, Integer
        int_field = SchemaNode(Integer())

    class StrUriSequenceSchema(URISequenceSchema):
        from colander import SchemaNode, String
        str_field = SchemaNode(String())

    def test_single_int_becomes_int_list(self):
        """URISequenceSchema should convert a single integer into a list with an integer
        """
        schema = self.IntUriSequenceSchema()
        target = 12
        expected = [12]
        result = schema.deserialize(target)
        self.assertEqual(expected, result)

    def test_single_string_int_becomes_int_list(self):
        """URISequenceSchema should convert a single integer string into a list with an integer
        """
        schema = self.IntUriSequenceSchema()
        target = '12'
        expected = [12]
        result = schema.deserialize(target)
        self.assertEqual(expected, result)

    def test_multiple_string_ints_becomes_int_list(self):
        """URISequenceSchema should convert multiple integers in a string string into a list of integers
        """
        schema = self.IntUriSequenceSchema()
        target = '12,34,56,78,90'
        expected = [12, 34, 56, 78, 90]
        result = schema.deserialize(target)
        self.assertEqual(expected, result)

    def test_accepts_list(self):
        """URISequenceSchema accepts a list
        """
        schema = self.IntUriSequenceSchema()
        target = [12]
        expected = [12]
        result = schema.deserialize(target)
        self.assertEqual(expected, result)

    def test_multiple_string_strings_becomes_string_list(self):
        """URISequenceSchema should convert multiple strings into a list of strings
        """
        schema = self.StrUriSequenceSchema()
        target = 'John,Jim,James,Jones'
        expected = ['John', 'Jim', 'James', 'Jones']
        result = schema.deserialize(target)
        self.assertEqual(expected, result)


class IDSchemaTests(TestCase):
    """
    Unit tests for :class:`schema.IdSchema`.
    """

    def setUp(self):
        from ..schema import IdSchema
        self.schema = IdSchema()

    def test_int_passes_validation(self):
        """IdSchema.id should pass validation with a valid integer string
        """
        params = {'id': 1}
        from colander import Invalid
        try:
            self.schema.deserialize(params)
        except Invalid as err:
            self.fail(err.msg)

    def test_int_sets_value(self):
        """IdSchema.id should deserialize a valid integer string
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
        """IdSchema.id should raise an exception for a value of zero
        """
        params = {'id': 0}
        from colander import Invalid
        with self.assertRaises(Invalid):
            self.schema.deserialize(params)

    def test_negative_id_raises_exception(self):
        """IdSchema.id should raise an exception for a negative value
        """
        params = {'id': -1}
        from colander import Invalid
        with self.assertRaises(Invalid):
            self.schema.deserialize(params)


class CreatePersonSchemaTests(TestCase):
    """
    Unit tests for :class:`schema.CreatePersonSchema` and integration tests for
    :class:`schema._IDSequenceSchema`.
    """

    def setUp(self):
        from ..schema import CreatePersonSchema
        self.schema = CreatePersonSchema()
        self.params = {'name': 'Nicolas Cage'}
        self.seq_fields = [
            'producer_credits',
            'director_credits',
            'writer_credits',
            'editor_credits',
            'cast_credits',
            'musician_credits']

    def test_name_string_passes_validation(self):
        """CreatePersonSchema does not raise an exception with valid parameters
        """
        from colander import Invalid
        try:
            self.schema.deserialize(self.params)
        except Invalid as err:
            self.fail(err.msg)

    def test_missing_name_raises_exception(self):
        """CreatePersonSchema raises an exception if a name is not provided
        """
        from colander import Invalid
        with self.assertRaises(Invalid):
            self.schema.deserialize({})

    def test_default_output(self):
        """CreatePersonSchema sets all undeclared fields to `None`
        """
        data = self.schema.deserialize(self.params)
        for field in self.seq_fields:
            self.assertEqual(None, data[field])

    def test_sequences_raise_exception_for_invalid_type(self):
        """CreatePersonSchema raises an exception if fields weren't given integers
        """
        dummy_id = 'non_int'
        for field in self.seq_fields:
            new_params = self.params
            new_params[field] = dummy_id
            from colander import Invalid
            with self.assertRaises(Invalid):
                self.schema.deserialize(new_params)

    def test_sequences_deserialize_single_item(self):
        """CreatePersonSchema converts URI formatted lists containing a single item into a Python list
        """
        dummy_id = '123'
        expected = [123]
        for field in self.seq_fields:
            new_params = self.params
            new_params[field] = dummy_id
            output = self.schema.deserialize(new_params)
            result = output[field]
            self.assertEqual(expected, result)

    def test_sequences_deserialize_into_lists(self):
        """CreatePersonSchema converts URI formatted lists into Python lists
        """
        dummy_ids = '12,34,56,67,89,123'
        expected = [12, 34, 56, 67, 89, 123]
        for field in self.seq_fields:
            new_params = self.params
            new_params[field] = dummy_ids
            output = self.schema.deserialize(new_params)
            result = output[field]
            self.assertEqual(expected, result)

    def test_missing_image_uri_does_not_raise_exception(self):
        """CreatePersonSchema raises an exception for a missing image URI
        """
        from colander import Invalid
        try:
            self.schema.deserialize(self.params)
        except Invalid as err:
            self.fail(err.msg)

    def test_invalid_image_uri_raises_exception(self):
        """CreatePersonSchema raises an exception for an invalid image URI
        """
        self.params['image_uri'] = 'invalid_image_uri'
        from colander import Invalid
        with self.assertRaises(Invalid):
            self.schema.deserialize(self.params)

    def test_zero_id_raises_exception(self):
        """CreatePersonSchema.producer_credits raises exception if an ID is set to 0
        """
        self.params['producer_credits'] = [0]
        from colander import Invalid
        with self.assertRaises(Invalid):
            self.schema.deserialize(self.params)

    @attr('onhold')
    def test_duplicate_id_raises_exception(self):
        """CreatePersonSchema.producer_credits raises exception if a duplicate ID is detected (ON HOLD)
        """
        self.params['producer_credits'] = [1, 1]
        from colander import Invalid
        with self.assertRaises(Invalid):
            self.schema.deserialize(self.params)


class RetrievePeopleSchemaTests(TestCase):
    """
    Unit tests for :class:`RetrievePeopleSchema`.
    """
    def setUp(self):
        from ..schema import RetrievePeopleSchema
        self.schema = RetrievePeopleSchema()
        self.seq_fields = [
            # 'producer_credits',
            # 'director_credits',
            # 'writer_credits',
            # 'editor_credits',
            'cast_credit',]
            # 'musician_credits']

    @attr('onhold')
    def test_credits_cast_string_list_with_single_string(self):
        """RetrievePeopleSchema credit fields return a list with a string if a single string is provided (ON HOLD)
        """
        for field in self.seq_fields:
            params = {field: 'test_value'}
            expected = ['test_value']
            result = self.schema.deserialize(params)
            self.assertEqual(expected, result[field])

    @attr('onhold')
    def test_credits_cast_string_list_with_many_strings(self):
        """RetrievePeopleSchema credit fields return a list of strings (ON HOLD)
        """
        for field in self.seq_fields:
            params = {field: 'value 0,value-1,value_2'}
            expected = ['value 0', 'value-1', 'value_2']
            result = self.schema.deserialize(params)
            self.assertEqual(expected, result[field])

    def test_credits_defaults_are_none(self):
        """RetrievePeopleSchema sequence fields set default value
        """
        result = self.schema.deserialize({})
        for field in self.seq_fields:
            self.assertEqual(None, result[field])

    def test_fields_default_empty_list(self):
        """RetrievePeopleSchema `fields` field defaults to empty list
        """
        result = self.schema.deserialize({})
        self.assertEqual([], result['fields'])


class RetrievePersonSchemaTests(TestCase):
    """
    Unit tests for :class:`schema.RetrievePersonSchema`.
    """

    def setUp(self):
        from ..schema import RetrievePersonSchema
        self.schema = RetrievePersonSchema()

    def test_no_fields_work(self):
        """RetrievePersonSchema does not raise an exception if no fields are provided
        """
        from colander import Invalid
        try:
            self.schema.deserialize({})
        except Invalid as err:
            self.fail(err.msg)

    def test_no_fields_sets_empty_list(self):
        """RetrievePersonSchema deserializes missing fileds into an empty list
        """
        result = self.schema.deserialize({})
        self.assertEqual([], result['fields'])

    def test_invalid_field_raises_exception(self):
        """RetrievePersonSchema raises an exception if invalid fields are set
        """
        params = {'fields': 'invalid_field'}
        from colander import Invalid
        with self.assertRaises(Invalid):
            self.schema.deserialize(params)

    def test_valid_fields_work(self):
        """RetrievePersonSchema does not raise an exception for any valid fields
        """
        from ..models import Person
        field_choices = Person.FIELD_CHOICES
        params = {'fields': field_choices}
        from colander import Invalid
        try:
            self.schema.deserialize(params)
        except Invalid as err:
            self.fail(err.msg)


class UpdatePersonSchemaTests(TestCase):
    """
    Unit tests for :class:`schema.UpdatePersonSchema`.

    NOTE: Test case only checks explicitly overwritten attributes.
    """

    def setUp(self):
        from ..schema import UpdatePersonSchema
        self.schema = UpdatePersonSchema()

    def test_nothing_mandatory(self):
        """UpdatePersonSchema does not require a name field
        """
        from colander import Invalid
        try:
            self.schema.deserialize({})
        except Invalid as err:
            self.fail(err.msg)

    def test_missing_name_sets_default(self):
        """UpdatePersonSchema sets a missing name field to a reasonable default
        """
        result = self.schema.deserialize({})
        self.assertEqual(None, result['name'])


class CreateFilmSchemaTests(TestCase):
    """
    Unit tests for :class:`schema.CreateFilmSchema`.
    """

    def setUp(self):
        from ..schema import CreateFilmSchema
        self.schema = CreateFilmSchema()
        self.params = {'title': 'Leaving Las Vegas'}
        self.req_fields = [
            'title']
        self.str_fields = [
            'rating']
        self.int_fields = [
            'year',
            'runtime']
        self.seq_fields = [
            'producers',
            'directors',
            'writers',
            'editors',
            'cast',
            'musicians']
        self.uri_fields = [
            'poster_uri',
            'trailer_uri',
            'wiki_uri']

    def test_title_required(self):
        """CreateFilmSchema raises an exception if no tile is provided
        """
        from colander import Invalid
        with self.assertRaises(Invalid):
            self.schema.deserialize({})

    def test_title_passes_validation(self):
        """CreateFilmSchema accepts a valid title
        """
        result = self.schema.deserialize(self.params)
        self.assertEqual(self.params['title'], result['title'])

    def test_default_output_str_fields(self):
        """CreateFilmSchema sets appropriate default parameters for string fields
        """
        result = self.schema.deserialize(self.params)
        self.assertEqual(None, result['rating'])

    def test_default_output_int_fields(self):
        """CreateFilmSchema sets appropriate default parameters for integer fields
        """
        result = self.schema.deserialize(self.params)
        fields = self.int_fields
        for field in fields:
            self.assertEqual(None, result[field])

    def test_default_output_seq_fields(self):
        """CreateFilmSchema sets appropriate default parameters for sequence fields
        """
        result = self.schema.deserialize(self.params)
        fields = self.seq_fields
        for field in fields:
            self.assertEqual(None, result[field])

    def test_missing_poster_uri_does_not_raise_exception(self):
        """CreateFilmSchema does not raise an exception for a missing poster_cache URI
        """
        from colander import Invalid
        try:
            self.schema.deserialize(self.params)
        except Invalid:
            self.fail('Missing poster_cache URI raised an exception.')

    def test_invalid_poster_uri_raises_exception(self):
        """CreateFilmSchema raises an exception for an invalid poster_cache URI
        """
        self.params['poster_uri'] = 'invalid_poster_uri'
        from colander import Invalid
        with self.assertRaises(Invalid):
            self.schema.deserialize(self.params)

    def test_missing_trailer_uri_does_not_raise_exception(self):
        """CreateFilmSchema does not raise an exception for a missing trailer URI
        """
        from colander import Invalid
        try:
            self.schema.deserialize(self.params)
        except Invalid:
            self.fail('Missing trailer URI raised an exception.')

    def test_invalid_trailer_uri_raises_exception(self):
        """CreateFilmSchema raises an exception for an invalid trailer URI
        """
        self.params['trailer_uri'] = 'invalid_trailer_uri'
        from colander import Invalid
        with self.assertRaises(Invalid):
            self.schema.deserialize(self.params)

    def test_missing_wiki_uri_does_not_raise_exception(self):
        """CreateFilmSchema does not raise an exception for a missing wiki URI
        """
        from colander import Invalid
        try:
            self.schema.deserialize(self.params)
        except Invalid:
            self.fail('Missing wiki URI raised an exception.')

    def test_invalid_wiki_uri_raises_exception(self):
        """CreateFilmSchema raises an exception for an invalid wiki URI
        """
        self.params['wiki_uri'] = 'invalid_wiki_uri'
        from colander import Invalid
        with self.assertRaises(Invalid):
            self.schema.deserialize(self.params)


class RetrieveFilmsSchemaTests(TestCase):
    """
    Unit tests for :class:`RetrievePeopleSchema`.
    """
    def setUp(self):
        from ..schema import RetrieveFilmsSchema
        self.schema = RetrieveFilmsSchema()
        self.seq_fields = [
            # 'producers',
            # 'directors',
            # 'writers',
            # 'editors',
            'cast',]
            # 'musicians']

    @attr('onhold')
    def test_credits_cast_string_list_with_single_string(self):
        """RetrieveFilmsSchema credit fields return a list with a string if a single string is provided (ON HOLD)
        """
        for field in self.seq_fields:
            params = {field: 'test_value'}
            expected = ['test_value']
            result = self.schema.deserialize(params)
            self.assertEqual(expected, result[field])

    @attr('onhold')
    def test_credits_cast_string_list_with_many_strings(self):
        """RetrieveFilmsSchema credit fields return a list of strings (ON HOLD)
        """
        for field in self.seq_fields:
            params = {field: 'value 0,value-1,value_2'}
            expected = ['value 0', 'value-1', 'value_2']
            result = self.schema.deserialize(params)
            self.assertEqual(expected, result[field])

    def test_credits_defaults_are_none(self):
        """RetrieveFilmsSchema sequence fields set default value
        """
        result = self.schema.deserialize({})
        for field in self.seq_fields:
            self.assertEqual(None, result[field])

    def test_fields_default_empty_list(self):
        """RetrieveFilmsSchema `fields` field defaults to empty list
        """
        result = self.schema.deserialize({})
        self.assertEqual([], result['fields'])


class RetrieveFilmSchemaTests(TestCase):
    """
    Unit tests for :class:`schema.RetrieveFilmSchema`.
    """

    def setUp(self):
        from ..schema import RetrieveFilmSchema
        self.schema = RetrieveFilmSchema()

    def test_no_fields_work(self):
        """RetrieveFilmSchema does not raise an exception if no fields are provided
        """
        from colander import Invalid
        try:
            self.schema.deserialize({})
        except Invalid as err:
            self.fail(err.msg)

    def test_invalid_field_raises_exception(self):
        """RetrieveFilmSchema raises an exception if invalid fields are set
        """
        params = {'fields': 'invalid_field'}
        from colander import Invalid
        with self.assertRaises(Invalid):
            self.schema.deserialize(params)

    def test_valid_fields_work(self):
        """RetrieveFilmSchema does not raise an exception for any valid fields
        """
        from ..models import Film
        field_choices = Film.FIELD_CHOICES
        params = {'fields': field_choices}
        from colander import Invalid
        try:
            self.schema.deserialize(params)
        except Invalid as err:
            self.fail(err.msg)


class UpdateFilmSchemaTests(TestCase):
    """
    Unit tests for :class:`schema.UpdateFilmSchema`

    NOTE: Test case only checks explicitly overwritten attributes.
    """

    def setUp(self):
        from ..schema import UpdateFilmSchema
        self.schema = UpdateFilmSchema()

    def test_nothing_mandatory(self):
        """UpdateFilmSchema does not require a title field
        """
        from colander import Invalid
        try:
            self.schema.deserialize({})
        except Invalid as err:
            self.fail(err.msg)

    def test_missing_title_sets_default(self):
        """UpdateFilmSchema sets a missing title field to a reasonable default
        """
        result = self.schema.deserialize({})
        self.assertEqual(None, result['title'])
