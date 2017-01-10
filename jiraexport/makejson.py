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

    def default(self, obj): # pylint: disable=E0202
        if isinstance(obj, datetime):
            return obj.isoformat()
        if isinstance(obj, Decimal):
            return str(obj)
        return json.JSONEncoder.default(self, obj)


def export(all_issues, directory):
    """Save all the issues to directory
    """

    # TODO: how do we make a `with` block conditional in order to respect quiet mode?
    logging.info("Writing "+str(len(all_issues))+" JSON files to disk")
    with ProgressBar(max_value=len(all_issues)) as progressbar:
        index = 0
        for issue in all_issues:
            index = index + 1 # TODO: what is the pythonic way to get my index
            progressbar.update(index)
            pkey = issue['pkey'] # eg. UA-451
            filename = pkey + ".json"
            outfile = os.path.join(directory, filename)

            with open(outfile, 'w') as outfile:
                try:
                    outfile.write(json.dumps(issue, cls=JiraEncoder))
                except UnicodeDecodeError:
                    # How do I make output work nicely with the progress bar?
                    # logging.error("augh, unicode decode errors")
                    pass
