__author__ = 'kobnar'

from nose.plugins.attrib import attr
from unittest import TestCase


class SerializeOMDBIntTests(TestCase):
    def test_int_strings_cast(self):
        int_strings = (('123', 123), ('123 min', 123))
        from ..bootstrap import serialize_omdb_int
        for int_str, expected in int_strings:
            result = serialize_omdb_int(int_str)
            self.assertEqual(expected, result)


class ParseNamesTests(TestCase):
    def test_parse(self):
        credit_strings = (
            (
                'Jerry B. Jenkins (based on novel)',
                'Jerry B. Jenkins', 'based on novel'
            ),
            (
                'Tim LaHaye (based on novel)',
                'Tim LaHaye', 'based on novel'
            ),
            (
                'Chris Sanders (screenplay)',
                'Chris Sanders', 'screenplay'
            ),
            (
                'Kirk De Micco (story)',
                'Kirk De Micco', 'story'
            ),
            (
                'David S. Goyer (story)',
                'David S. Goyer', 'story'
            ),
            (
                'Lawrence Konner (screen story)',
                'Lawrence Konner', 'screen story'
            ),
            (
                'Victor Argo (earlier film "Bad Lieutenant")',
                'Victor Argo', 'earlier film "Bad Lieutenant"'
            ),
            (
                'Zoë Lund (earlier film "Bad Lieutenant")',
                'Zoë Lund', 'earlier film "Bad Lieutenant"'
            ),
            (
                'Osamu Tezuka (manga)',
                'Osamu Tezuka', 'manga'
            ),
            (
                'Oren Aviv (characters)',
                'Oren Aviv', 'characters'
            ),
            (
                'Philip K. Dick (novel)',
                'Philip K. Dick', 'novel'
            ),
            (
                'John Davies (fake trailer segment "Hobo with a Shotgun")',
                'John Davies', 'fake trailer segment "Hobo with a Shotgun"'
            ),
            (
                'Mark Steven Johnson (screen story)',
                'Mark Steven Johnson', 'screen story'
            ),
            (
                'John McLoughlin (true story)',
                'John McLoughlin', 'true story'
            ),
            (
                'John Nickle (book)',
                'John Nickle', 'book'
            ),
            (
                'Jim Haskins (pictorial history "The Cotton Club")',
                'Jim Haskins', 'pictorial history "The Cotton Club"'
            ),
            (
                'William Wharton (based on the novel by)',
                'William Wharton', 'based on the novel by'
            )
        )
        from ..bootstrap import parse_credit
        for credit in credit_strings:
            target, name_check, note_check = credit
            name_result, note_result = parse_credit(target)
            self.assertEqual(name_check, name_result)
            self.assertEqual(note_check, note_result)

    def test_normal_names(self):
        """parse_credit() correctly parses credit lines without notes
        """
        normal_strings = (
            (
                'Jennifer Jason Leigh',
                'Jennifer Jason Leigh', None
            ),
            (
                'Robert Bierman',
                'Robert Bierman', None
            )
        )
        from ..bootstrap import parse_credit
        for credit in normal_strings:
            target, name_check, note_check = credit
            name_result, note_result = parse_credit(target)
            self.assertEqual(name_check, name_result)
            self.assertEqual(note_check, note_result)


class SerializeOMDBPeople(TestCase):
    def test_none_works(self):
        self.fail()
