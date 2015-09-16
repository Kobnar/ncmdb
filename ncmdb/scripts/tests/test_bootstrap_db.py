__author__ = 'kobnar'
from nose.plugins.attrib import attr
from unittest import TestCase


@attr('bootstrap')
class PeopleDataTests(TestCase):
    def test_all_names_unique(self):
        """All people names in the bootstrap script should be unique
        """
        from ..bootstrap_db import PEOPLE
        names = [x['name'] for x in PEOPLE]
        checked = []
        for name in names:
            if name not in checked:
                checked.append(name)
            else:
                self.fail('Duplicate name detected: {}'.format(name))


@attr('bootstrap')
class FilmDataTests(TestCase):
    def test_no_titles_empty(self):
        """All film titles in the bootstrap script should be populated
        """
        from ..bootstrap_db import FILMS
        for title in [x['title'] for x in FILMS]:
            if not title:
                self.fail('Duplicate name detected: {}'.format(title))

    def test_all_titles_unique(self):
        """All film titles in the bootstrap script should be unique
        """
        from ..bootstrap_db import FILMS
        titles = [x['title'] for x in FILMS]
        checked = []
        for title in titles:
            if title not in checked:
                checked.append(title)
            else:
                self.fail('Duplicate name detected: {}'.format(title))

    def test_all_years_positive(self):
        """All film years in the bootstrap script should be positive
        """
        from ..bootstrap_db import FILMS
        for film in FILMS:
            title = film['title']
            year = film['year']
            if year < 0:
                self.fail('Invalid year detected: \'{}\' ({})'.format(title, year))

    def test_all_running_times_positive(self):
        """All running times in the bootstrap script should be positive
        """
        from ..bootstrap_db import FILMS
        for film in FILMS:
            title = film['title']
            running_time = film['running_time']
            if running_time < 0:
                self.fail('Invalid running time detected: \'{}\' ({})'.format(
                    title, running_time))

    def test_all_producers_accounted_for(self):
        """All producers have an entry in the list of known people
        """
        from ..bootstrap_db import PEOPLE
        producers = [x['name'] for x in PEOPLE]
        missing = set()
        from ..bootstrap_db import FILMS
        for film in FILMS:
            for producer in film['producers']:
                if producer and producer not in producers:
                    missing.add(producer)
        if missing:
            missing_str = ', '.join(missing)
            self.fail('The following people are unaccounted for: {}'.format(
                missing_str))

    def test_all_directors_accounted_for(self):
        """All directors have an entry in the list of known people
        """
        from ..bootstrap_db import PEOPLE
        producers = [x['name'] for x in PEOPLE]
        missing = set()
        from ..bootstrap_db import FILMS
        for film in FILMS:
            for producer in film['producers']:
                if producer and producer not in producers:
                    missing.add(producer)
        if missing:
            missing_str = ', '.join(missing)
            self.fail('The following people are unaccounted for: {}'.format(
                missing_str))

    def test_all_writers_accounted_for(self):
        """All writers have an entry in the list of known people
        """
        from ..bootstrap_db import PEOPLE
        writers = [x['name'] for x in PEOPLE]
        missing = set()
        from ..bootstrap_db import FILMS
        for film in FILMS:
            for writer in film['writers']:
                if writer and writer not in writers:
                    missing.add(writer)
        if missing:
            missing_str = ', '.join(missing)
            self.fail('The following people are unaccounted for: {}'.format(
                missing_str))

    def test_all_editors_accounted_for(self):
        """All editors have an entry in the list of known people
        """
        from ..bootstrap_db import PEOPLE
        editors = [x['name'] for x in PEOPLE]
        missing = set()
        from ..bootstrap_db import FILMS
        for film in FILMS:
            for editor in film['editors']:
                if editor and editor not in editors:
                    missing.add(editor)
        if missing:
            missing_str = ', '.join(missing)
            self.fail('The following people are unaccounted for: {}'.format(
                missing_str))

    def test_all_cast_accounted_for(self):
        """All cast have an entry in the list of known people
        """
        from ..bootstrap_db import PEOPLE
        cast = [x['name'] for x in PEOPLE]
        missing = set()
        from ..bootstrap_db import FILMS
        for film in FILMS:
            for actor in film['cast']:
                if actor and actor not in cast:
                    missing.add(actor)
        if missing:
            missing_str = ', '.join(missing)
            self.fail('The following people are unaccounted for: {}'.format(
                missing_str))

    def test_nic_cage_in_everything(self):
        """Nicolas Ford Coppola should be in every movie
        """
        from ..bootstrap_db import FILMS
        missing = set()
        for film in FILMS:
            if 'Nicolas Cage' not in film['cast']:
                missing.add(film['title'])
        if missing:
            missing_str = ', '.join(missing)
            self.fail('Propper credit for our Lord and Savior, Nicolas Cage,'
                      'is missing in the following films: {}'.format(missing_str))
