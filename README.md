# get-a-room
Princeton University study room/space recommendation app

## Git conventions
### Branches
- `master`: Stable "production-level" branch. Commits are merged into here from the `dev` branch. This branch contains releases/milestones of the app, and should be *fully* tested and working.
- `dev`: Development branch. Contains commit history as we progress to each release/milestone. Commits are merged into `dev` from topic branches, so code should be *mostly* tested and working by the time it is merged here. (It still may have small bugs, though.)
- Topic branches: Branches out of `dev` for bug fixes, features, etc. Should be individually tested before merging back to `dev`. Name these branches with a few short words describing the branch, e.g. `database-setup`.

## Code conventions
### General
- Indentation: Indent with *spaces*, indent size of 4.
- Line endings: Unix-style `\n`.

### Python-specific
- Strings: Use single quotes.
- Header comments (at file-level and function-level): Standard Python style. Immediately inside the function/class, enclosed in triple quotes, with newlines between triple quotes.

## Dependencies
For contributers, installation of dependencies and other set-up is automated by running a script in the root of the project: `setup`. When a new dependency installation or set-up is required, this script is updated accordingly to automate it. See the script for details.

## Contributers
- Michael J. Friedman
- Rachana Balasubramanian
