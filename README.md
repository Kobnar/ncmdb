# Nicolas Cage Movie Database

*NOTE: All commands are provided from the root directory of the project (i.e.
the directory of this README).*

## Getting started

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

### Bootstrapping the database
 
The Nicolas Cage Movie Database comes pre-loaded with some of our Lord and
Savior's fine expressions of character. In order to start the site with these
excellent works pre-loaded, a bootstrap script has been provided for you. To run
this script and begin your journey through His amazing filmography, use the
one-shot command seen here:

```
..ncmdb/ $ python
>>> from ncmdb.scripts.bootstrap import NCMDBManager
>>> manager = NCMDBManager()
>>> manager.load()
```

As the bootstrap script populates the database, you will see relevant output in
the terminal. This is normal. Take some time to reflect on His prolific
collection of miracles. Now strive to watch them all.

## Making changes to the database

There are two ways to alter the data in the Nicolas Cage Movie Database: using
the NCMDb REST interface or using the bootstrap script.

### Using the API:

NCMDb includes a simple REST API for both films and people to allow basic CRUD
operations to manipulate the database. Each resource type has an index, from
which you can CREATE a new resource or RETRIEVE a list of resources matching a
specific query (NOTE: no parameters dumps the entire database). Each individual
resource has its own location as well, from which you can UPDATE, RETRIEVE and
DELETE using the corresponding HTTP methods. For example:

CREATE a new person:
```
..ncmdb/ $ curl http://localhost:6543/api/v1/people/ -X POST -d "name=John Doe"
```

RETRIEVE a list of people matching certain parameters:
```
..ncmdb/ $ curl http://localhost:6543/api/v1/people/?name=Mike -x GET
```

RETRIEVE a specific person:
```
..ncmdb/ $ curl http://localhost:6543/api/v1/people/23/ -x GET
```

UPDATE a specific person:
```
..ncmdb/ $ curl http://localhost:6543/api/v1/people/23/ -x PUT -d "name=Jane Doe"
```

DELETE a specific person:
```
..ncmdb/ $ curl http://localhost:6543/api/v1/people/23/ -x DELETE
```

*NOTE: By default queries are greedy and running a query without parameters
dumps the entire table. For example, a query looking for `id=2` will return
every id which includes the number `2` (including `23`, `12`, etc.).*

### Using the bootstrap script:

Changes can also be made using the bootstrap script by altering the source data
provided in `ncmdb/scripts/ncmdb.json`. After making your changes to the JSON
data file, you can simply repeat the bootstrap operations and the manager will
load the changes you've made.

*WARNING: If you want to take this route and you have already made changes using
the REST interface, it is recommended you save your existing data first by
running `NCMDBManager.save()`!*

# To-Do:

  * Consolidate common code in API views
  * Cast roles (e.g. "Lula")
  * Writer credits (e.g. "story by", "screenplay", "novel", etc.)
  * Stricter access rules on certain fields (e.g. `Film.image_cache`)
