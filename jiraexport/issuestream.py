"""Fetch JIRA issues from database

Defines a schema using SQLalchemy
"""

from __future__ import absolute_import
from __future__ import print_function

import logging
import sqlalchemy
from sqlalchemy.orm import sessionmaker
from . import jiraschema


def get_issues(user, password, host="localhost", database="jira"):
    """Get all the JIRA issues from a database.
    """

    connstr = 'mysql+pymysql://{}:{}@{}/{}?charset=utf8'.format(user, password, host, database)
    engine = sqlalchemy.create_engine(connstr, echo=False)
    connection = engine.connect()
    connection.execution_options(stream_results=True)
    Session = sessionmaker(bind=engine)
    session = Session()

    # This is a bit of a hack. How else are you supposed to make a progress bar with a generator?
    count = session.query(jiraschema.Issue).count()
    yield count

    for issue in session.query(jiraschema.Issue):
        try:
            yield issue.as_dict()
        except Exception:
            # Do not try to attach the sqlalchemy record as extra info. There be dragons.
            logging.error("Uncaught exception trying to process a record. Oh well. Too bad.", exc_info=True)
