#!/bin/bash
# script to run Go5
# Can be run from any directory, see
# http://stackoverflow.com/questions/59895/can-a-bash-script-tell-what-directory-its-stored-in
# Forwards all command line arguments, see
# http://stackoverflow.com/questions/3190818/pass-all-arguments-from-bash-script-to-another-command

DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )
python3 $DIR/Go5.py "$@"
