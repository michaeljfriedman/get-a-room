#!/bin/bash
# configure.sh
# Author: Michael Friedman
#
# Script to automate installation of dependencies and other configuration of
# your environment for this project.

# Check for help command
usage="Usage: ./configure.sh MODE
       ./configure.sh --help"

help_message="This script automates installation of dependencies and other configuration
of your environment for the project.

Pass one of the following values for MODE:
  all         Runs the full setup
  db          Only initializes/configures/updates the database
  python      Only installs Python dependencies

Options
  --help      Displays this message"

if [ $# -eq 1 ] && [ "$1" == "--help" ]; then
  echo "$usage"
  echo
  echo "$help_message"
  exit
fi

# Validate usage
if [ $# -ne 1 ]; then
  echo "$usage"
  exit
fi

mode=$1
if ! ([ "$mode" == "all" ] || [ "$mode" == "db" ] || [ "$mode" == "python" ]); then
  echo "$usage"
  exit
fi

#-------------------------------------------------------------------------------

# Shortcuts for displaying a message. Pass message as arg
function start {
  echo "----- Begin: $1 -----"
}

function finish {
  echo "----- Done: $1 -----"
  sleep 1
}

# Setup Python environment
if [ "$mode" == "all" ] || [ "$mode" == "python" ]; then
  start "Setting up Python environment"

  # Setup virtual environment
  if [ ! -d "venv" ]; then
    virtualenv venv
  fi
  source venv/bin/activate

  # Download dependencies
  pip install Django==1.10.6

  deactivate
  finish "Setting up Python environment"
fi

# Setup database
if [ "$mode" == "all" ] || [ "$mode" == "db" ]; then
  start "Setting up database"
  source venv/bin/activate

  cd get_a_room
  python setup_database.py -p
  cd ..

  deactivate
  finish "Setting up database"
fi
