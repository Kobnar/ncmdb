import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.txt')) as f:
    README = f.read()
with open(os.path.join(here, 'CHANGES.txt')) as f:
    CHANGES = f.read()

requires = [
    'pyramid',
    'pyramid_chameleon',
    'pyramid_debugtoolbar',
    'pyramid_tm',
    'pyramid_jinja2',
    'SQLAlchemy',
    'transaction',
    'zope.sqlalchemy',
    'waitress',
    'nose',
    ]

setup(name='movie_trailer_website',
      version='0.0',
      description='A simple movie trailer website for Udacity\'s Full Stack Web'
                  'Developer Nanodegree using the Pyramid framework',
      long_description=README + '\n\n' + CHANGES,
      classifiers=[
        "Programming Language :: Python",
        "Framework :: Pyramid",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
        ],
      author='',
      author_email='',
      url='',
      keywords='web wsgi bfg pylons pyramid',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      test_suite='movie_trailer_website',
      install_requires=requires,
      entry_points="""\
      [paste.app_factory]
      main = movie_trailer_website:main
      [console_scripts]
      initialize_movie_trailer_website_db = movie_trailer_website.scripts.initializedb:main
      """,
      )
