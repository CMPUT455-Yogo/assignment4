#!/usr/bin/python3
# /usr/bin/python3
# Set the path to your python3 above

from gtp_connection import GtpConnection
from board_util import GoBoardUtil
from board import GoBoard
import numpy as np
from simulation_util import writeMoves, select_best_move
from ucb import runUcb
#################################################
'''
This is a uniform random NoGo player served as the starter code
for your (possibly) stronger player. Good luck!
'''
class NoGo:
    def __init__(self):
        """
        NoGo player that selects moves randomly from the set of legal moves.

        Parameters
        ----------
        name : str
            name of the player (used by the GTP interface).
        version : float
            version number (used by the GTP interface).
        """
        self.name = "Go0"
        self.version = 1.0
        self.use_ucb = True
        self.random_simulation = True
        self.use_pattern = not self.random_simulation
        self.weights = self.get_weights()
        self.limit = 100000000
        self.sim = 8


    # def get_move(self, board, color):
    #     return GoBoardUtil.generate_random_move(board, color, 
    #                                             use_eye_filter=False)

    def get_weights(self):
        f = open("./assignment3/weights.txt", "r")
        content = f.read().split("\n")
        weights = {}
        for i in range(len(content) - 1):
                item = content[i].split()
                weights[int(item[0])] = float(item[1])
        return weights

    def computeProbabilities(self, board, color):
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
        if self.random_simulation:
            return moves, [1/len(moves)] * len(moves)
        for move in moves:
            weight = self.computeWeight(board, move)
            sum += weight
            weights.append(weight)
        for i in range(len(moves)):
            probabilities.append(weights[i] / sum)
        return moves, probabilities

    def computeWeight(self, board, move):
        neighbors = [move + board.NS - 1, move + board.NS, move + board.NS + 1, move - 1, move + 1, move - board.NS - 1, move - board.NS, move - board.NS + 1]
        s = 0
        for i in range(len(neighbors)):
            s += board.board[neighbors[i]] * 4**i
        w = self.weights[s]
        return w

    def generate_pattern_move(self, board, color):
        moves, probabilities = self.computeProbabilities(board, color)
        if len(moves) == 0:
            return None
        m = np.random.choice(moves, p=probabilities)
        return m

    def simulate(self, board, move, toplay):
        """
        Run a simulated game for a given move.
        """
        cboard = board.copy()
        cboard.play_move(move, toplay)
        opp = GoBoardUtil.opponent(toplay)
        return self.playGame(cboard, opp)

    def simulateMove(self, board, move, toplay):
        """
        Run simulations for a given move.
        """
        wins = 0
        for _ in range(self.sim):
            result = self.simulate(board, move, toplay)
            if result == toplay:
                wins += 1
        return wins

    def get_move(self, board, color):
        """
        Run one-ply MC simulations to get a move to play.
        """
        cboard = board.copy()
        emptyPoints = board.get_empty_points()
        moves = []
        for p in emptyPoints:
            if board.is_legal(p, color):
                moves.append(p)
        if not moves:
            return None
        # moves.append(None)
        if self.use_ucb:
            C = 0.4  # sqrt(2) is safe, this is more aggressive
            best = runUcb(self, cboard, C, moves, color)
            return best
        else:
            moveWins = []
            for move in moves:
                wins = self.simulateMove(cboard, move, color)
                moveWins.append(wins)
            writeMoves(cboard, moves, moveWins, self.sim)
            return select_best_move(board, moves, moveWins)

    def playGame(self, board, color):
        """
        Run a simulation game.
        """
        for _ in range(self.limit):
            color = board.current_player
            if self.random_simulation:
                move = GoBoardUtil.generate_random_move(board, color)
            else:
                move = self.generate_pattern_move(board, color)
            if move == None:
                break
            board.play_move(move, color)
        return GoBoardUtil.opponent(color)
        
def run():
    """
    start the gtp connection and wait for commands.
    """
    board = GoBoard(7)
    con = GtpConnection(NoGo(), board)
    con.start_connection()

if __name__ == "__main__":
    run()
