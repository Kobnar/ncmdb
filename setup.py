import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.md')) as f:
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
    'colander',
    'waitress',
    'nose',
    ]

setup(name='ncmdb',
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
      test_suite='ncmdb',
      install_requires=requires,
      entry_points="""\
      [paste.app_factory]
      main = ncmdb:main
      [console_scripts]
      initialize_ncmdb_db = ncmdb.scripts.initializedb:main
      """,
      )
