#!/usr/bin/python2
# import MySQLdb # super legacy
import mysql.connector
import json
from datetime import datetime
from decimal import Decimal

class JiraEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        if isinstance(obj, Decimal):
            return str(obj)
        return json.JSONEncoder.default(self, obj)

config = {
    'user': 'root',
    'password': 'OBTAIN_FROM_ENVIRONMENT_OR_SOMETHING',
    'host': 'localhost',
    'database': 'jira',
}

def pop_multiple(table, key, value, cnx, issueobj):
    cur = cnx.cursor(dictionary=True)
    stmt="SELECT * FROM "+table+" WHERE "+key+"='"+value+"'"
    #print(stmt)
    cur.execute(stmt)
    results = []
    for row in cur.fetchall():
        results.append(row)
    if len(results) > 0:
        issueobj[table] = results

#cnx = cur = None
cnx = mysql.connector.connect(**config)
cur = cnx.cursor(dictionary=True)

# TODO: one query per table. populate all the issue objects in memory simultaneously.
# this will make it faster, at the possible expense of memory usage.

cur.execute("SELECT * FROM jiraissue LIMIT 3")
for row in cur.fetchall():
    issueobj = row
    # print(json.dumps(issueobj, cls=JiraEncoder))
    issueid = str(row['ID'])
    pop_multiple('worklog', 'issueid', issueid, cnx, issueobj)
    pop_multiple('jiraaction', 'issueid', issueid, cnx, issueobj)
    print(json.dumps(issueobj, cls=JiraEncoder))



cur.close()
cnx.close()
