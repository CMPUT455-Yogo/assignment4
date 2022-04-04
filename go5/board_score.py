"""
board_score.py
Implements functions to:
- compute the final score on a Go board
- determine the winner.
"""

import numpy as np
from board_util import where1d, BORDER, BLACK, WHITE

def score_board(board, komi):
    """ Score board from Black's point of view """
    score = -komi
    counted = np.full(board.maxpoint, False, dtype=bool)
    for point in range(board.maxpoint):
            color = board.get_color(point)
            if color == BORDER or (point in counted):
                continue
            if color == BLACK:
                score += 1
            elif color == WHITE:
                score -= 1
            else:
                black_flag = False
                white_flag = False
                empty_points = where1d(board.connected_component(point))
                for p in empty_points:
                    counted[p] = True 
                    # TODO faster to boolean-or the whole array
                    if board.find_neighbor_of_color(p, BLACK):
                        black_flag = True
                    if board.find_neighbor_of_color(p, WHITE):
                        white_flag = True
                    if black_flag and white_flag:
                        break
                if black_flag and not white_flag:
                    score += len(empty_points)
                if white_flag and not black_flag:
                    score -= len(empty_points)
    return score

def winner(board, komi):
    score = score_board(board, komi)
    if score > 0:
        return BLACK
    elif score < 0:
        return WHITE
    else:
        return None
