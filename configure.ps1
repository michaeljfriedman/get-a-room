# configure.ps1
# Author: Michael Friedman
#
# Script to automate installation of dependencies and other configuration of
# your environment for this project.

# Check for help command
$usage = @"
Usage: .\configure.ps1 MODE
       .\configure.ps1 --help
"@

$help_message = @"
This script automates installation of dependencies and other configuration
of your environment for the project.

Pass one of the following values for MODE:
  all         Runs the full setup
  db          Only initializes/configures/updates the database
  python      Only installs Python dependencies

Options
  --help      Displays this message
"@

if (($args.Length -eq 1) -and ($args[0] -eq "--help")) {
  Write-Output $usage "" $help_message
  exit
}

# Validate usage
if ($args.Length -ne 1) {
  Write-Output $usage
  exit
}

$mode = $args[0]
if (($mode -ne "all") -and ($mode -ne "db") -and ($mode -ne "python")) {
  Write-Output $usage
  exit
}

#------------------------------------------------------------------------------

# Shortcuts for displaying a message. Pass message as arg.
function start_msg {
  $msg = $args[0]
  Write-Output "----- Begin: $msg -----"
}

function finish_msg {
  $msg = $args[0]
  Write-Output "----- Done: $msg -----"
  sleep 1
}

# Setup Python environment
if (($mode -eq "all") -or ($mode -eq "python")) {
  start_msg "Setting up Python environment"

  # Setup virtual environment
  if (-not (Test-Path venv)) {
    virtualenv venv
  }
  .\venv\Scripts\activate.ps1

  # Download dependencies
  pip install Django==1.10.6

  deactivate
  finish_msg "Setting up Python environment"
}

# Setup database
if (($mode -eq "all") -or ($mode -eq "db")) {
  start_msg "Setting up database"
  .\venv\Scripts\activate.ps1

  Set-Location get_a_room
  python setup_database.py -p
  Set-Location ..

  deactivate
  finish_msg "Setting up database"
}
