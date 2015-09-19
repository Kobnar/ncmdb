# Nicolas Cage Movie Database

NOTE: All commands are provided from the root directory of the project (i.e.
the directory of this README).

## Getting Started

### Dependencies

The Nicolas Cage Movie Database has the following system dependencies:

* Python 3.4
* SQLite 3.8

In order to run the Nicolas Cage Movie Database, it is recommended that you
create and use a virtual environment located in the root directory of the
project. To embark on this wondrous trek, simply execute the following commands
from your terminal emulator of choice:

```
..ncmdb/ $ virtualenv -p python3 env
..ncmdb/ $ source env/bin/activate
(env) ..ncmdb/ $ python setup.py develop
```

All of the libraries used by the Nicolas Cage Movie Database are available for
free using `pip` (or whatever package manager your distro employs).

NOTE: This project will always and only operate in a development capacity. None
of the production environment settings have been set.

### Bootstrapping the Database
 
The Nicolas Cage Movie Database comes pre-loaded with some of our Lord and
Savior's fine expressions of character. In order to start the site with these
excellent works pre-loaded, a bootstrap script has been provided for you. To run
this script and begin your journey through His amazing filmography, use the
one-shot command seen here:

```
..ncmdb/ $ python -c 'from ncmdb.scripts import bootstrap_db'
```

As the bootstrap script populates the database, you will see relevant output in
the terminal. This is normal. Take some time to reflect on His prolific
collection of miracles. Now strive to watch them all.

# To-Do:

  * Cast roles (e.g. "Lula")
  * Writer credits (e.g. "story by", "screenplay", "novel", etc.)
