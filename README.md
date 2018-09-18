# 476webserviceapi
web service api using flask and http basic authentication

# For virtual environment to be able to run custom commands
# More info here http://click.pocoo.org/5/quickstart/
# Only need to do once
# 1. Install virtualenv
  $ pip install virtualenv
# 2. Create virtual environment
  $ virtualenv venv

# Needs to run for each virtual environment (each instance of terminal)
# Enter virtual env
  $ . venv/bin/activate
# Set virtual env flask app
  $ export FLASK_APP=api.py
# Start app
  $ flask run
# Leave virtual environment
  $ deactivate
