"""Jiraexport CLI module

Handy commands to help you export your JIRA issues.
"""

# Because Click makes our main() function look weird
# pylint: disable=E1120
# pylint: disable=R0913

from __future__ import absolute_import
from __future__ import print_function

import logging
import os
import sys
import click
from . import makejson
from . import maketxt
from . import issuestream
from .logger import logger, setup_logging
import sqlalchemy

# TODO: add a force (--force ?) flag to overwrite whatever is in a directory


@click.command()
@click.option('--format', '-f', type=click.Choice(['json', 'html', 'text']), default="json")
# I'm using the same option names as what `mysql` provides
@click.option('--user', '-u', default="root", help="MySQL username")
@click.option('--password', '-p', prompt='MySQL Password', hide_input=True, help="MySQL password", envvar="MYSQL_PWD")
@click.option('--host', '-h', default="localhost", help="MySQL hostname", envvar="MYSQL_HOST")
@click.option('--database', '-D', default="jira", help="MySQL database name")
@click.option('--quiet', '-q', is_flag=True, help="Suppress warnings")
@click.option('--verbose', '-v', is_flag=True, help="Lively output")
@click.option('--force', is_flag=True, help="Overwrite contents in target directory")
@click.version_option(version="0.1.1")
@click.argument('directory')
def main(format, user, password, host, database, quiet, verbose, force, directory):
    """Export a JIRA database as flat files into a directory.
    """

    setup_logging(quiet=quiet, verbose=verbose)

    # Target doesn't exist? Let's create it.
    # if not os.path.exists(directory):
    try:
        os.makedirs(directory)
    except OSError as e:
        if e.errno == 17:
            logger.warning('The directory already exists. Some contents may be overwritten.')
        else:
            raise

    if os.listdir(directory) != []:
        if force:
            logger.warning('Target directory not empty. Some files may be overwritten.')
        else:
            logger.error('The target directory must be empty.')
            sys.exit(1)

    logger.info('Using directory: ' + directory)

    try:
        issues = issuestream.get_issues(user, password, host, database)
    except sqlalchemy.exc.OperationalError:
        print('Connection failed. Maybe you provided the wrong password?')
        sys.exit(1)
    count = issues.next()

    if format == 'json':
        makejson.export(count, issues, directory)
    elif format == 'text':
        maketxt.export(count, issues, directory)
    else:
        print('The requested format ' + format + ' is not implemented yet.')


if __name__ == '__main__':
    main()
