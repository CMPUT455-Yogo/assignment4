"""
simulation_util.py

Utility functions shared by simulation-based players Go3 and Go4

"""

from gtp_connection import point_to_coord, format_point
import numpy as np
import sys

def byPercentage(pair):
    return pair[1]

def percentage(wins, numSimulations):
    return float(wins) / float(numSimulations)

def writeMoves(board, moves, count, numSimulations):
    """
    Write simulation results for each move.
    """
    gtp_moves = []
    for i in range(len(moves)):
        move_string = "Pass"
        if moves[i] != None:
            x, y = point_to_coord(moves[i], board.size)
            move_string = format_point((x, y))
        gtp_moves.append((move_string, 
                          percentage(count[i], numSimulations)))
    sys.stderr.write("win rates: {}\n".format(sorted(gtp_moves,
                     key = byPercentage, reverse = True)))
    sys.stderr.flush()

def select_best_move(board, moves, moveWins):
    """
    Move select after the search.
    """
    max_child = np.argmax(moveWins)
    return moves[max_child]
