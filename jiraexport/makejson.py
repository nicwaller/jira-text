import json
import os
from progressbar import ProgressBar
from datetime import datetime
from decimal import Decimal
import logging

class JiraEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        if isinstance(obj, Decimal):
            return str(obj)
        return json.JSONEncoder.default(self, obj)

def export(all_issues, directory, force, quiet):
    # TODO: how do we make a `with` block conditional in order to respect quiet mode?
    logging.info("Writing "+str(len(all_issues))+" JSON files to disk")
    with ProgressBar(max_value=len(all_issues)) as bar:
        index = 0
        for issue in all_issues:
            index = index + 1 # TODO: what is the pythonic way to get my index
            bar.update(index)
            pkey = issue['pkey'] # eg. UA-451
            filename = pkey + ".json"
            outfile = os.path.join(directory, filename)

            with open(outfile, 'w') as f:
                try:
                    f.write(json.dumps(issue, cls=JiraEncoder))
                except UnicodeDecodeError:
                    # How do I make output work nicely with the progress bar?
                    # logging.error("augh, unicode decode errors")
                    pass
