from setuptools import setup, find_packages
import os

version_file = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'jiraexport', 'VERSION'))
version = version_file.read().strip()

setup(
    name='jiraexport',
    version=version,
    author='Nic Waller',
    author_email='code@nicwaller.com',
    description='Export issues from a JIRA database to flat files',
    url='https://github.com/nicwaller/jiraexport',
    install_requires=[
        'sqlalchemy',
        'pymysql', # Pure native python MySQL adapter that SQLalchemy can use
        # 'mysql-connector', # I guess we don't need this any more
    ],
    entry_points={
        "console_scripts": [
            "jiraexport=jiraexport.jiraexport:main",
        ]
    },
    packages=find_packages(),
    include_package_data=True,
    package_data={
        'jiraexport': ['jiraexport/VERSION'],
    },
)
