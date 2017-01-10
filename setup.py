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
        'click', # for making nice command-line utilities
        'sqlalchemy',
        'pymysql', # Pure native python MySQL adapter that SQLalchemy can use
        'progressbar2',
    ],
    entry_points={
        "console_scripts": [
            "jiraexport=jiraexport.cli:main",
        ]
    },
    packages=find_packages(),
    include_package_data=True,
    package_data={
        'jiraexport': ['jiraexport/VERSION'],
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Topic :: System :: Archiving'
      ]
)
