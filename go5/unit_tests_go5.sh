#!/bin/bash

# Script for running unit tests for go2

TESTS="test_board.py test_board_util.py"
# TODO test the go2-specific gtp class "test_gtp_connection.py"
 
for unit_test in $TESTS; do
    python3 $unit_test
done
