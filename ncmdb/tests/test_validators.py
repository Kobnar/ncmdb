__author__ = 'kobnar'
from unittest import TestCase


class ValidateURITests(TestCase):
    """
    These tests make sure `validators.validate_uri()` accepts good URI patterns
    that are known to be good and rejects those that are known to be bad.
    """
    def test_good_uris_pass(self):
        from ..validators import validate_uri
        from . import PROFILE_URIS
        for uri in PROFILE_URIS:
            self.assertIsNotNone(validate_uri(uri))
        from . import POSTER_URIS
        for uri in POSTER_URIS:
            self.assertIsNotNone(validate_uri(uri))
        from . import WIKI_URIS
        for uri in WIKI_URIS:
            self.assertIsNotNone(validate_uri(uri))

    def test_bad_uris_fail(self):
        from ..validators import validate_uri
        from . import BAD_URIS
        for uri in BAD_URIS:
            self.assertIsNone(validate_uri(uri))


class URIValidatorTests(TestCase):
    """
    These tests make sure :class:`validators.URIValidator` accepts good URI
    patterns that are known to be good and raises a :class:`colander.Invalid`
    exception for those that are known to be bad.
    """
    def setUp(self):
        from ..validators import URIValidator
        self.validator = URIValidator()

    def test_good_uris_pass(self):
        from colander import Invalid
        from . import PROFILE_URIS, POSTER_URIS, WIKI_URIS
        for uri in PROFILE_URIS + POSTER_URIS + WIKI_URIS:
            try:
                self.validator('uri', uri)
            except Invalid:
                self.fail('URI failed validation: {}'.format(uri))

    def test_bad_uris_fail(self):
        from colander import Invalid
        from . import BAD_URIS
        for uri in BAD_URIS:
            with self.assertRaises(Invalid):
                self.validator('uri', uri)
