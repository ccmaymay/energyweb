=========
energyweb
=========

energyweb is an energy usage monitoring/display system developed for
Harvey Mudd College, particularly for use during the November Energy
Competition.  It is not intended to be a general-purpose system, but
it will hopefully be found useful (and there are plans to use these
ideas as a starting point for a general-purpose utility monitoring
system).

------------
Requirements
------------

energyweb has been tested on Linux, using the following packages and
versions.  It may work on other platforms or with other versions, but
this is not guaranteed.

* Django 1.2
* Python 2.6.5, 2.6.6
* PostgreSQL 8.4.5, 8.4.6
* psycopg 2.0.13, 2.2.1

In addition, energyweb includes the following JavaScript packages.

* jQuery 1.4.4
* jQuery UI 1.8.7
* flot 0.6

----------
Background
----------

Power monitoring devices developed by Joseph King in the Engineering
Department are installed around campus.  These are cheap to make, thus
providing an attractive alternative to many energy monitoring solutions 
today.

Each device listens on a TCP port.  It can accept only one client.
When it has a client, it sends 45 bytes of energy data about once 
every 10 seconds.

energyweb essentially consists of ``energymon``, a service (implemented
as a Django command) that connects to a Rhizome device and records the
data it receives in the database, and a Django-based web interface to 
that data.

---------
Licensing
---------

energyweb is published under the MIT License.
