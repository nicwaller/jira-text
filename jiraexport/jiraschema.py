"""Define schema of the JIRA database

At least the parts we care about.
"""

# We don't need "missing docstring" because this is very simple code
# pylint: disable=C0111

# And a schema definition will always have "too few public methods"
# pylint: disable=R0903

from __future__ import absolute_import
from __future__ import print_function

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.mysql import LONGTEXT
from sqlalchemy.ext.declarative import declarative_base


DeclarativeBase = declarative_base()


class Issue(DeclarativeBase):
    __tablename__ = 'jiraissue'
    issueid = Column('ID', Integer, primary_key=True)
    issuestatus = Column(Integer, ForeignKey('issuestatus.ID'))  # never NULL
    component = Column("COMPONENT", String)  # always NULL
    environment = Column("ENVIRONMENT", String)  # mostly NULL
    fixfor = Column("FIXFOR", String)  # always NULL
    created = Column("CREATED", DateTime)  # never NULL
    priority = Column("PRIORITY", Integer, ForeignKey('priority.ID'))  # never NULL
    security = Column("SECURITY", Integer)  # always NULL
    resolution = Column("RESOLUTION", Integer, ForeignKey('resolution.ID'))  # Never NULL. Surprisingly.
    time_estimate = Column("TIMEESTIMATE", String)  # Almost always NULL
    pkey = Column(String)
    votes = Column("VOTES", Integer)  # never NULL, always zero
    reporter = Column("REPORTER", String)  # never NULL (wow)
    summary = Column("SUMMARY", String)  # never NULL
    project = Column("PROJECT", Integer, ForeignKey('project.ID'))  # never NULL
    assignee = Column("ASSIGNEE", String)  # occasionally NULL
    workflow_id = Column("WORKFLOW_ID", Integer, ForeignKey('workflowscheme.ID'))
    time_spent = Column("TIMESPENT", String)  # almost always NULL
    timeoriginalestimate = Column("TIMEORIGINALESTIMATE", String)  # almost always NULL
    duedate = Column("DUEDATE", DateTime)  # very commonly NULL
    updated = Column("UPDATED", DateTime)
    description = Column("DESCRIPTION", String)  # commonly NULL
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


class JiraAction(DeclarativeBase):
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
    actionnum = Column(Integer)  # TODO: or Decimal?

    # play nice with JSON serialization
    def as_dict(self):
        serial = {column.key: getattr(self, attr) for attr, column in self.__mapper__.c.items()}
        return serial


class IssueStatus(DeclarativeBase):
    __tablename__ = 'issuestatus'

    id = Column('ID', Integer, primary_key=True)
    sequence = Column('SEQUENCE', Integer)
    pname = Column(String)
    description = Column('DESCRIPTION', String)  # TODO: actually Text, not VARCHAR
    iconurl = Column('ICONURL', String)

    issue = relationship("Issue", back_populates="issuestatus_r")

    # play nice with JSON serialization
    def as_dict(self):
        serial = {column.key: getattr(self, attr) for attr, column in self.__mapper__.c.items()}
        return serial


class IssueType(DeclarativeBase):
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


class WorkflowScheme(DeclarativeBase):
    __tablename__ = 'workflowscheme'

    id = Column('ID', Integer, primary_key=True)
    name = Column('NAME', String)
    description = Column('DESCRIPTION', String)

    issue = relationship("Issue", back_populates="workflowscheme_r")

    # play nice with JSON serialization
    def as_dict(self):
        serial = {column.key: getattr(self, attr) for attr, column in self.__mapper__.c.items()}
        return serial


class Project(DeclarativeBase):
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


class Resolution(DeclarativeBase):
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


class Priority(DeclarativeBase):
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
