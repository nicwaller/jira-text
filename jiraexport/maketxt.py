"""Take list of JIRA issues and write them into a directory as text files
"""

from __future__ import absolute_import
from __future__ import print_function

import logging
import os
from progressbar import ProgressBar


def textlines(issue):
    """Yield a bunch of results

    Now I'm just showing off because I think generators are kinda cool.
    """
    yield '{}\n\n'.format(issue['pkey'])
    yield 'Issue Type: {}\n'.format(issue['issuetype'])
    # yield 'Issue ID: {}\n'.format(issue['ID'])
    # yield 'Component: {}\n'.format(issue['COMPONENT'])
    # yield 'Environment: {}\n'.format(issue['ENVIRONMENT'])
    # yield 'Fixed For: {}\n'.format(issue['FIXFOR'])
    yield 'Created: {}\n'.format(issue['CREATED'])
    yield 'Priority: {}\n'.format(issue['priority']['pname'])
    yield 'Reporter: {}\n'.format(issue['REPORTER'])
    # yield 'Assignee: {}\n'.format(issue['ASSIGNEE'])
    # yield 'Security: {}\n'.format(issue['SECURITY'])
    if issue.has_key('resolution'):
        yield 'Resolution: {} ({})\n'.format((issue['resolution'] or 'N/A'), issue['RESOLUTIONDATE'])
    yield 'Issue Status: {}\n'.format(issue['issuestatus'])
    # yield 'Time Estimate: {}\n'.format(issue['TIMEESTIMATE'])
    # yield 'Votes: {}\n'.format(issue['VOTES'])
    # yield 'Project: {}\n'.format(issue['PROJECT'])
    # yield 'Workflow ID: {}\n'.format(issue['WORKFLOW_ID'])
    # yield 'Time Spent: {}\n'.format(issue['TIMESPENT'])
    # yield 'Original Estimate: {}\n'.format(issue['TIMEORIGINALESTIMATE'])
    # yield 'Due Date: {}\n'.format(issue['DUEDATE'])
    # yield 'Updated: {}\n'.format(issue['UPDATED'])
    # yield 'Resolution Date: {}\n'.format(issue['RESOLUTIONDATE'])

    yield 'Summary: {}\n'.format(issue['SUMMARY'].encode('utf-8'))
    yield '\n'
    yield '{}\n'.format((issue['DESCRIPTION'] or 'N/A').encode('utf-8'))

    for action in issue['actions']:
        yield '\n'
        yield '='*71 + '[ ACTION ]\n'
        yield 'Created: ' + str(action['CREATED']) + '\n'  # It is a DateTime + '\n'
        yield 'Author: ' + action['AUTHOR'] + '\n'
        # yield action['UPDATEAUTHOR'] + '\n'
        # yield 'Updated: ' + str(action['UPDATED']) + '\n'
        # yield 'Action Level: ' + (action['actionlevel'] or '').encode('utf-8') + '\n'
        # yield 'Action Type: ' + action['actiontype'] + '\n'
        # yield 'Role Level: ' + (action['rolelevel'] or '').encode('utf-8') + '\n'
        # yield 'ID: ' + str(action['ID'] or '') + '\n'
        # yield 'Action Number: ' + str(action['actionnum']) + '\n'
        yield '\n'
        yield action['actionbody'].encode('utf-8') + '\n'
    yield '\n'


def export(issue_count, issue_generator, directory):
    """Save all the issues to directory
    """

    # TODO: how do we make a `with` block conditional in order to respect quiet mode?
    logging.info('Writing {} text files to disk'.format(issue_count))
    with ProgressBar(max_value=issue_count) as progressbar:
        for index, issue in enumerate(issue_generator):
            progressbar.update(index)
            pkey = issue['pkey']  # eg. UA-451
            filename = pkey + ".txt"
            outfile = os.path.join(directory, filename)

            with open(outfile, 'w') as outfile:
                outfile.writelines(textlines(issue))
