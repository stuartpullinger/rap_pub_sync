# rap_pub_sync
Pub and Sync tests for APEL's rap host

$ python db2json.py --help
Usage: db2json.py [options]

Connects to a database, runs query and prints the result in json on stdout.
The script takes a database configuration file (currently only supports MySQL)
and an SQL query file. It connects the database, runs the query and iterates
over the results converting each row to a object in the JSON which is written
to STDOUT.

Options:
  -h, --help            show this help message and exit
  -d DB, --db=DB        the location of database config file
  -q QUERY, --query=QUERY
                        the query file
