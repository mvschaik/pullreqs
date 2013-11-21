pullreqs
========

Fetch all open pull requests from Github


Installation
------------

1. Create a Github personal access token on https://github.com/settings/applications
2. Put the token in the GITHUB\_TOKEN variable in your environment, f.i. by 
   adding `export GITHUB_TOKEN='your\_token\_here'` to ~/.bashrc
3. Checkout pullreqs from github and install deps by running `pip install -r dependencies.txt`
4. Put pullreqs.py in your path


Usage
-----

Run `pullreqs.py` to get a list of open PR's for all your repositories.

Run `pullreqs.py <organization>` to get a list of open PR's for all the repositories of an organization.

TODO
----
* Only show PR's for repositories you watch
* Make installer/setup.py and publish to the cheeseshop
