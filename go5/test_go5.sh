#!/bin/bash

# Script for running Go5 unit and basic functional tests

PROGRAM="go5.sh"
OUTPUTDIR="results_test_go5"
GO0DIR="../go0and1"

gogui-regress $PROGRAM -output $OUTPUTDIR $GO0DIR/test_go_base.tst
gogui-regress $PROGRAM -output $OUTPUTDIR $GO0DIR/test_simple_ko.tst
gogui-regress $PROGRAM -output $OUTPUTDIR $GO0DIR/test_suicide.tst
gogui-regress $PROGRAM -output $OUTPUTDIR test_go5.tst

# To do: add python unit tests for go3 and go4 code

# To do: add python unit tests for mcts code
# TESTS="test_mcts.py test_go5.py"
#  
# for unit_test in $TESTS; do
#     python3 $unit_test
# done
