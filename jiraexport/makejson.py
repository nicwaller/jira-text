"""Take list of JIRA issues and write them into a directory as JSON files
"""

from __future__ import absolute_import
from __future__ import print_function

import json
import logging
import os
from datetime import datetime
from decimal import Decimal
from progressbar import ProgressBar


class JiraEncoder(json.JSONEncoder):
    """Add support for datetime and Decimal
    """

    def default(self, obj):  # pylint: disable=E0202
        if isinstance(obj, datetime):
            return obj.isoformat()
        if isinstance(obj, Decimal):
            return str(obj)
        return json.JSONEncoder.default(self, obj)


def export(issue_count, issue_generator, directory):
    """Save all the issues to directory
    """

    # TODO: how do we make a `with` block conditional in order to respect quiet mode?
    logging.info('Writing {} JSON files to disk'.format(issue_count))
    with ProgressBar(max_value=issue_count) as progressbar:
        for index, issue in enumerate(issue_generator):
            progressbar.update(index)
            pkey = issue['pkey']  # eg. UA-451
            filename = pkey + ".json"
            outfile = os.path.join(directory, filename)

            with open(outfile, 'w') as outfile:
                outfile.write(json.dumps(issue, cls=JiraEncoder))
