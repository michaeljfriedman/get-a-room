# Project Setup

We have automated the setup required for any contributors to the project in a script called configure.{ps1, sh}. This automates installing dependencies, configuring the database, and other configuration.

## Quick Start

If you just need to get the environment set up from scratch for the first time, run the script for your OS. (You will need to have Python 2.7, pip package manager, and virtualenv installed beforehand, though.) For Mac/Linux:

```
./configure.sh all
```

or for Windows (run this in PowerShell):

```
.\configure.ps1 all
```

This will install all dependencies to a Python virtual environment. Make sure to activate it when working on the project with:

```
source venv/bin/activate
```

That's it! You should be all set to work on the project now. Optionally (but *highly* recommended), you can verify that everything is working properly by running the tests. The full test suite is also automated in a script called test.{ps1, sh}:

```
./test.sh
```

or:

```
.\test.ps1
```


## More details about the configure script

We recommend that you do the quick start if you're getting your environment set up for the first time. However, you can also choose to set up only certain components using the same configure script. This is primarily so that you can rerun the script when pulling changes from the repository, e.g. to install new dependencies, without running the entire setup again. (*Note that the examples below are written for Mac/Linux, but there are analogous Windows commands as well.*)

- `./configure.sh all`: Runs the full setup (as in **Quick Start**)
- `./configure.sh python`: Installs only Python packages
- `./configure.sh db`: Only initializes/configures/updates the database
  