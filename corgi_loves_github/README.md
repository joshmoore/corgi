GitHub plugin for Corgi
=======================

Reacts to GitHub events like Pull Request creation
and modification.

Requirements
------------

    PyGithub

Installation
------------

1. corgi_loves_github is present in the main repository
   and should be available by default.

2. Register hook

    See sample-subscribe.sh

3. Configure server.cfg

    Add a mapping for each GitHub user to the corresponding Redmine user

    Add Redmine and Jenkins login information

    Add repository to job mapping information
