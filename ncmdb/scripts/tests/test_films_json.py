__author__ = 'kobnar'

from nose.plugins.attrib import attr
from unittest import TestCase


@attr('JSON')
class FilmsJSONDataTests(TestCase):
    def setUp(self):
        import json
        with open('ncmdb/scripts/films.json') as data_file:
            self.film_data = json.load(data_file)

    def test_cage_in_every_film(self):
        missing = set()
        for film in self.film_data:
            if 'Nicolas Cage' not in film['Actors']:
                missing.add(film['Title'])
        if missing:
            self.fail('Nicolas Cage acting credit missing from the following'
                      'works: {}'.format(', '.join(missing)))
