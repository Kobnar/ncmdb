# Nicolas Cage Movie Database

The Nicolas Cage Movie Database, may his name shine for a thousand years, is
a repository of His Lord Cage's many works, intended to provide the layman with
but a rudimentary guide to grasping the vast array and holiness of His many
films.

## Getting started

The Nicolas Cage Movie Database is a Pyramid web application which has not been
changed in any fundamental way to manage real-world deployment. In short, it
should run like any other Pyramid web application, with minimal dependencies
or set-up required.

While reviewing this readme, all paths to resources or commands to be issued
are provided from the project's root directory (i.e. the directory of this
README).

### Dependencies

The Nicolas Cage Movie Database has the following system dependencies:

* Python 3.4+
* SQLite 3.8+

In order to run the Nicolas Cage Movie Database, it is recommended that you
create and use a virtual environment located in the root directory of the
project. To embark on this wondrous trek, simply execute the following commands
from your terminal emulator of choice:

```
..ncmdb/ $ virtualenv -p python3 env
..ncmdb/ $ source env/bin/activate
(env) ..ncmdb/ $ python setup.py develop
```

All of the python libraries used by the Nicolas Cage Movie Database should be
available for free by running the setuptools script. For a complete list, check
out the requirements listed in `setup.py`.

### Bootstrapping the database
 
The Nicolas Cage Movie Database comes pre-loaded with some of our Lord and
Savior's fine expressions of character. In order to start the site with these
excellent works included, a bootstrap script has been provided for you. To run
this script and begin your journey through His amazing filmography, start a
Python shell and issue the following commands. Take heed: His works are many
and prolific, which will take time to load and cache.

```
..ncmdb/ $ python
>>> from ncmdb.scripts.bootstrap import NCMDBManager
>>> manager = NCMDBManager()
>>> manager.load()
```

As the bootstrap script populates the database, you will see relevant output in
the terminal. This is normal. Take some time to reflect on His extensive
collection of miracles. Now strive to watch them all.

If you have made contributions to the database, you can save those changes by
instantiating the `NCMDBManager` in the Python shell (as seen above) and calling
`NCMDBManager.save()`.

### Running the Pyramid web application

Assuming you have activated your virtual environment, run the setuptools script,
and run the database bootstrap script, you should be ready to start the web
application. To do this, run the following command:

```
..ncmdb/ $ pserve development.ini
Starting server in PID 984.
serving on http://0.0.0.0:6543
```

Once the app is running, open your browser and head to `localhost:6543`, and
there you should see His works in all their glory.

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

Tragically, the REST interface is not very complete. Creating and updating
data is simple, however foreign relations are still defined using IDs. Querying
films or peope based on credits, additionally, only supports querying actors.
Later versions shall implement a more complete interface.

*NOTE: By default queries are greedy and running a query without parameters
dumps the entire table. For example, a query looking for `id=2` will return
every id which includes the number `2` (including `23`, `12`, etc.).*

### Using the bootstrap script:

Changes can also be made using the bootstrap script by altering the source data
provided in `ncmdb/scripts/ncmdb.json`. After making your changes to the JSON
data file, you can simply repeat the bootstrap operations and the manager will
load the changes you've made. Make sure to save a backup, lest you make a
mistake and are forced to reset the repository to the last official commit.

*WARNING: If you want to take this route and you have already made changes using
the REST interface, it is recommended you save your existing data first by
running `NCMDBManager.save()`!*

# To-Do:

  * Consolidate common code in API views
  * Complete REST interface (e.g. producer credits)
  * Complete the database (e.g. all trailers)
  * Add cast roles (e.g. "Lula", the character)
  * Add writer credits (e.g. "story by", "screenplay", "novel", etc.)
  * Add strict access rules on certain fields (e.g. `Film.image_cache`)
