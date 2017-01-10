import click
import makejson
import mysqlalchemy
import os
import logging
import sys

# TODO: add a force (--force ?) flag to overwrite whatever is in a directory

@click.command()
@click.option('--format', '-f', type=click.Choice(['json', 'html', 'text']), default="text")
# I'm using the same option names as what `mysql` provides
@click.option('--user', '-u', default="root", help="MySQL username")
@click.option('--password', '-p', prompt=True, hide_input=True, help="MySQL password", envvar="MYSQL_PWD")
@click.option('--host', '-h', default="localhost", help="MySQL hostname", envvar="MYSQL_HOST")
@click.option('--database', '-D', default="jira", help="MySQL database name")
@click.option('--quiet', '-q', is_flag=True, help="Suppress warnings")
@click.option('--verbose', '-v', is_flag=True, help="Lively output")
@click.option('--force', is_flag=True, help="Overwrite contents in target directory")
@click.version_option(version="0.1.0")
@click.argument('directory')
def main(format, user, password, host, database, quiet, verbose, force, directory):
    """Export a JIRA database as flat files into a directory.
    """

    if quiet:
        logging.getLogger("").setLevel(logging.ERROR)
    elif verbose:
        logging.getLogger("").setLevel(logging.INFO)
    else:
        logging.getLogger("").setLevel(logging.WARNING)

    # Target doesn't exist? Let's create it.
    if not os.path.exists(directory):
        os.makedirs(directory)

    if os.listdir(directory) != []:
        if force:
            logging.warning("Target directory not empty. Some files may be overwritten.")
        else:
            logging.error("The target directory must be empty.")
            sys.exit(1)

    logging.info("Using directory: " + directory)

    all_issues = mysqlalchemy.get_all_issues(user, password, host, database)
    # I don't feel super good about having passing this GIANT object around
    makejson.export(all_issues, directory, force, quiet)

if __name__ == "__main__":
    main()

    # TODO: have a quiet mode. It's nice for cron jobs.
    # TODO: write to a file. Stdout/stderr is better for info/warning/error?
    # TODO: peek/preview mode that writes a few records to stdout. maybe even selected records.
