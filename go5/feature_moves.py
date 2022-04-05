"""
feature_moves.py
Move generation based on simple features.
"""

from board_score import winner
from board_util import GoBoardUtil, PASS
from feature import Features_weight
from feature import Feature
from pattern_util import PatternUtil
import numpy as np
import random



class FeatureMoves(object):
    @staticmethod
    def generate_moves(board):

        assert len(Features_weight) != 0
        moves = []
        gamma_sum = 0.0
        empty_points = board.get_empty_points()
        color = board.current_player
        probs = np.zeros(board.maxpoint)
        all_board_features = Feature.find_all_features(board)
        for move in empty_points:
            if board.is_legal(move, color) and not board.is_eye(move, color):
                moves.append(move)
                probs[move] = Feature.compute_move_gamma(
                    Features_weight, all_board_features[move]
                )
                gamma_sum += probs[move]
        if len(moves) != 0:
            assert gamma_sum != 0.0
            for m in moves:
                probs[m] = probs[m] / gamma_sum
        return moves, probs

    @staticmethod
    def generate_move(board):
        moves, probs = FeatureMoves.generate_moves(board)
        if len(moves) == 0:
            return None
        return np.random.choice(board.maxpoint, 1, p=probs)[0]

    @staticmethod
    def generate_move_with_feature_based_probs_max(board):
        """Used for UI"""
        moves, probs = FeatureMoves.generate_moves(board)
        move_prob_tuple = []
        for m in moves:
            move_prob_tuple.append((m, probs[m]))
        return sorted(move_prob_tuple, key=lambda i: i[1], reverse=True)[0][0]

    # @staticmethod
    # def playGame(board, color, **kwargs):
    #     """
    #     Run a simulation game according to give parameters.
    #     """
        
    #     # simulation_policy = kwargs.pop("random_simulation", "random")
    #     use_pattern = kwargs.pop("use_pattern", True)
    #     if kwargs:
    #         raise TypeError("Unexpected **kwargs: %r" % kwargs)
    #     nuPasses = 0
    #     # for _ in range(limit):
    #     while True:
    #         color = board.current_player
    #         # if simulation_policy == "random":
    #         #     move = GoBoardUtil.generate_random_move(board, color)
    #         # elif simulation_policy == "rulebased":
    #         #     move = PatternUtil.generate_pattern_move(
    #         #         board, use_pattern
    #         #     )
    #         # else:
    #         #     assert simulation_policy == "prob"
    #         move = FeatureMoves.generate_pattern_move(board, color)
    #         board.play_move(move, color)
    #         if move is None:
    #             break
                
    #     # get winner
    #     winner = GoBoardUtil.opponent(color)
    #     return winner



    @staticmethod
    def playGame(board, color, **kwargs):
        """
        Run a simulation game.
        """
        while True:
            color = board.current_player
            # if self.random_simulation:
            #     move = GoBoardUtil.generate_random_move(board, color, True)
            # else:
            move = FeatureMoves.generate_pattern_move(board, color)
            if move == None:
                break
            board.play_move(move, color)
        return GoBoardUtil.opponent(color)

    @staticmethod
    def generate_pattern_move(board, color):
        moves, probabilities = FeatureMoves.computeProbabilities(board, color)
        if len(moves) == 0:
            return None
        m = np.random.choice(moves, p=probabilities)
        return m

    @staticmethod
    def computeProbabilities(board, color):
        emptyPoints = board.get_empty_points()
        moves = []
        weights = []
        probabilities = []
        sum = 0
        for p in emptyPoints:
            if board.is_legal(p, color):
                moves.append(p)
        if not moves:
            return [], []
        # if self.random_simulation:
        #     return moves, [1/len(moves)] * len(moves)
        for move in moves:
            weight = FeatureMoves.computeWeight(board, move)
            sum += weight
            weights.append(weight)
        for i in range(len(moves)):
            probabilities.append(weights[i] / sum)
        return moves, probabilities

    @staticmethod
    def computeWeight(board, move):
        neighbors = [move + board.NS - 1, move + board.NS, move + board.NS + 1, move - 1, move + 1, move - board.NS - 1, move - board.NS, move - board.NS + 1]
        s = 0
        for i in range(len(neighbors)):
            s += board.board[neighbors[i]] * 4**i
        # weights = FeatureMoves.get_weights()
        w = weights[s]
        return w

    @staticmethod
    def get_weights():
        f = open("go5/weights.txt", "r")
        content = f.read().split("\n")
        weights = {}
        for i in range(len(content) - 1):
                item = content[i].split()
                weights[int(item[0])] = float(item[1])
        return weights

weights = FeatureMoves.get_weights()