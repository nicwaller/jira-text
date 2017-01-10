"""Fetch JIRA issues from database

Defines a schema using SQLalchemy
"""

from __future__ import absolute_import
from __future__ import print_function

import logging
import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import sessionmaker
from sqlalchemy.dialects.mysql import LONGTEXT
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from progressbar import ProgressBar


Base = declarative_base()


class Issue(Base):
    __tablename__ = 'jiraissue'
    issueid = Column('ID', Integer, primary_key=True)
    issuestatus = Column(Integer, ForeignKey('issuestatus.ID')) # never NULL
    component = Column("COMPONENT", String) # always NULL
    environment = Column("ENVIRONMENT", String) # mostly NULL
    fixfor = Column("FIXFOR", String) # always NULL
    created = Column("CREATED", DateTime) # never NULL
    priority = Column("PRIORITY", Integer, ForeignKey('priority.ID')) # never NULL
    security = Column("SECURITY", Integer) # always NULL
    resolution = Column("RESOLUTION", Integer, ForeignKey('resolution.ID')) # Never NULL. Surprisingly.
    time_estimate = Column("TIMEESTIMATE", String) # Almost always NULL
    pkey = Column(String)
    votes = Column("VOTES", Integer) # never NULL, always zero
    reporter = Column("REPORTER", String) # never NULL (wow)
    summary = Column("SUMMARY", String) # never NULL
    project = Column("PROJECT", Integer, ForeignKey('project.ID')) # never NULL
    assignee = Column("ASSIGNEE", String) # occasionally NULL
    workflow_id = Column("WORKFLOW_ID", Integer, ForeignKey('workflowscheme.ID'))
    time_spent = Column("TIMESPENT", String) # almost always NULL
    timeoriginalestimate = Column("TIMEORIGINALESTIMATE", String) # almost always NULL
    duedate = Column("DUEDATE", DateTime) # very commonly NULL
    updated = Column("UPDATED", DateTime)
    description = Column("DESCRIPTION", String) # commonly NULL
    resolutiondate = Column("RESOLUTIONDATE", DateTime)
    issuetype = Column("issuetype", Integer, ForeignKey('issuetype.ID'))

    actions_r = relationship("JiraAction", back_populates="issue")
    issuestatus_r = relationship("IssueStatus", back_populates="issue")
    issuetype_r = relationship("IssueType", back_populates="issue")
    # There is a bug in resolving the workflow relationship but I don't care to work it out
    workflowscheme_r = relationship("WorkflowScheme", back_populates="issue")
    project_r = relationship("Project", back_populates="issue")
    resolution_r = relationship("Resolution", back_populates="issue")
    priority_r = relationship("Priority", back_populates="issue")

    # play nice with JSON serialization
    def as_dict(self):
        # Copy scalar types
        serial = {column.key: getattr(self, attr) for attr, column in self.__mapper__.c.items()}
        # Resolve many-to-one relationships and substitute scalar value
        serial['issuestatus'] = self.issuestatus_r.as_dict()['pname']
        serial['issuetype'] = self.issuetype_r.as_dict()['pname']
        serial['project'] = self.project_r.as_dict()
        if self.resolution_r:
            serial['resolution'] = self.resolution_r.as_dict()['pname']
        serial['priority'] = {
            'pname': self.priority_r.as_dict()['pname'],
            'status_color': self.priority_r.as_dict()['STATUS_COLOR'],
        }
        if self.workflowscheme_r:
            serial['workflow'] = self.workflowscheme_r.as_dict()['name']
        # Resolve one-to-many relationships into a list
        serial['actions'] = []
        for x in self.actions_r:
            serial['actions'].append(x.as_dict())
        return serial


class JiraAction(Base):
    __tablename__ = 'jiraaction'

    id = Column('ID', Integer, primary_key=True)
    issueid = Column(Integer, ForeignKey('jiraissue.ID'))
    issue = relationship("Issue", back_populates="actions_r")
    author = Column("AUTHOR", String)
    actiontype = Column(String)
    actionlevel = Column(String)
    rolelevel = Column(Integer)
    actionbody = Column(LONGTEXT)
    created = Column("CREATED", DateTime)
    updateauthor = Column("UPDATEAUTHOR", String)
    updated = Column("UPDATED", DateTime)
    actionnum = Column(Integer) # TODO: or Decimal?

    # play nice with JSON serialization
    def as_dict(self):
        serial = {column.key: getattr(self, attr) for attr, column in self.__mapper__.c.items()}
        return serial


class IssueStatus(Base):
    __tablename__ = 'issuestatus'

    id = Column('ID', Integer, primary_key=True)
    sequence = Column('SEQUENCE', Integer)
    pname = Column(String)
    description = Column('DESCRIPTION', String) # TODO: actually Text, not VARCHAR
    iconurl = Column('ICONURL', String)

    issue = relationship("Issue", back_populates="issuestatus_r")

    # play nice with JSON serialization
    def as_dict(self):
        serial = {column.key: getattr(self, attr) for attr, column in self.__mapper__.c.items()}
        return serial


class IssueType(Base):
    __tablename__ = 'issuetype'

    id = Column('ID', Integer, primary_key=True)
    sequence = Column('SEQUENCE', Integer)
    pname = Column(String)
    pstyle = Column(String)
    description = Column('DESCRIPTION', String)
    iconurl = Column('ICONURL', String)

    issue = relationship("Issue", back_populates="issuetype_r")

    # play nice with JSON serialization
    def as_dict(self):
        serial = {column.key: getattr(self, attr) for attr, column in self.__mapper__.c.items()}
        return serial


class WorkflowScheme(Base):
    __tablename__ = 'workflowscheme'

    id = Column('ID', Integer, primary_key=True)
    name = Column('NAME', String)
    description = Column('DESCRIPTION', String)

    issue = relationship("Issue", back_populates="workflowscheme_r")

    # play nice with JSON serialization
    def as_dict(self):
        serial = {column.key: getattr(self, attr) for attr, column in self.__mapper__.c.items()}
        return serial


class Project(Base):
    __tablename__ = 'project'

    id = Column('ID', Integer, primary_key=True)
    pname = Column(String)
    url = Column('URL', String)
    lead = Column('LEAD', String)
    description = Column('DESCRIPTION', String)
    pkey = Column(String)
    pcounter = Column(Integer)
    assigneetype = Column('ASSIGNEETYPE', Integer)
    avatar = Column('AVATAR', Integer)

    issue = relationship("Issue", back_populates="project_r")

    # play nice with JSON serialization
    def as_dict(self):
        serial = {column.key: getattr(self, attr) for attr, column in self.__mapper__.c.items()}
        return serial


class Resolution(Base):
    __tablename__ = 'resolution'

    id = Column('ID', Integer, primary_key=True)
    sequence = Column('SEQUENCE', Integer)
    pname = Column(String)
    description = Column('DESCRIPTION', String)
    iconurl = Column('ICONURL', String)

    issue = relationship("Issue", back_populates="resolution_r")

    # play nice with JSON serialization
    def as_dict(self):
        serial = {column.key: getattr(self, attr) for attr, column in self.__mapper__.c.items()}
        return serial


class Priority(Base):
    __tablename__ = 'priority'

    id = Column('ID', Integer, primary_key=True)
    sequence = Column('SEQUENCE', Integer)
    pname = Column(String)
    description = Column('DESCRIPTION', String)
    iconurl = Column('ICONURL', String)
    status_color = Column('STATUS_COLOR', String)

    issue = relationship("Issue", back_populates="priority_r")

    # play nice with JSON serialization
    def as_dict(self):
        serial = {column.key: getattr(self, attr) for attr, column in self.__mapper__.c.items()}
        return serial


def get_all_issues(user, password, host="localhost", database="jira"):
    """Get all the JIRA issues from a database.
    """

    connstr = 'mysql+pymysql://'+user+':'+password+'@'+host+'/'+database
    engine = sqlalchemy.create_engine(connstr, echo=False)
    engine.connect() # TODO: can this be removed?
    Session = sessionmaker(bind=engine)
    session = Session()

    count = session.query(Issue).count()
    logging.info("About to pull "+str(count)+" objects from database...")

    # TODO: do not show the progress bar in quiet mode
    with ProgressBar(max_value=count) as progressbar:
        # how sweet would be it to colorize the progress bar to show errors. (so sweet)

        results = [] # TODO: can we do this in a way that is more memory-efficient?
        completed = 0
        for issue in session.query(Issue):
            try:
                results.append(issue.as_dict())
            except Exception:
                # Do not try to attach the sqlalchemy record as extra info. There be dragons.
                logging.error("Uncaught exception trying to process a record. Oh well. Too bad.", exc_info=True)
            finally:
                completed = completed + 1
                progressbar.update(completed)
    return results
