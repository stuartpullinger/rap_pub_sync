#!/usr/bin/env python
"""Connects to a database, runs query and prints the result in json on stdout.

The script takes a database configuration file (currently only supports MySQL)
and an SQL query file. It connects the database, runs the query and iterates
over the results converting each row to a object in the JSON which is written
to STDOUT."""

import MySQLdb
import json
import ConfigParser
from optparse import OptionParser
import sys

# Parse the commandline options
opt_parser = OptionParser(description=__doc__)
opt_parser.add_option('-d', '--db', help='the location of database config file', 
                      default='/etc/apel/db.cfg')
opt_parser.add_option('-q', '--query', help='the query file')
(options, args) = opt_parser.parse_args()

# Parse the database configuration file
try:
    dbcp = ConfigParser.ConfigParser()
    dbcp.read(options.db)

    DB_BACKEND = dbcp.get('db', 'backend')
    DB_HOSTNAME = dbcp.get('db', 'hostname')
    DB_PORT = int(dbcp.get('db', 'port'))
    DB_NAME = dbcp.get('db', 'name')
    DB_USERNAME = dbcp.get('db', 'username')
    DB_PASSWORD = dbcp.get('db', 'password')

except (ConfigParser.Error, ValueError, IOError), err:
    sys.stderr.write('Error in configuration file %s: %s'
                     % (options.db, str(err)))
    sys.stderr.write('The system will exit.')
    sys.exit(1)

# Connect to the database
try:
    db = MySQLdb.connect(host=DB_HOSTNAME, port=DB_PORT, user=DB_USERNAME,
                         passwd=DB_PASSWORD, db=DB_NAME)
except MySQLdb.Error, err:
    sys.stderr.write('Error connecting to database: %s', err)
    sys.stderr.write('The system will exit.')
    sys.exit(1)

# Read the SQL query file
queryfile = open(options.query, 'r')
query = queryfile.read()
queryfile.close()

# Query the database
try:
    c = db.cursor(cursorclass=MySQLdb.cursors.SSDictCursor)
    c.execute(query)
except MySQLdb.Error, err:
    sys.stderr.write('Error during getting records: %s', err)
    sys.stderr.write('The system will exit.')
    sys.exit(1)
except MySQLdb.Warning, warning:
    sys.stderr.write('Warning from MySQL: %s', warning)

# Create the json and write it to stdout
rows = [dict(row) for row in c.fetchall()]
json.dump(rows, sys.stdout)
