import unittest
from ChessVar import ChessPiece, KingPiece, QueenPiece, RookPiece, KnightPiece, BishopPiece, PawnPiece, ChessVar

class TestClass(unittest.TestCase):
    """Contains unit tests"""

    def test_1(self):
        """Contains Unit Tests for Initialization"""
        game_board = [ ['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r'],
                       ['p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'],
                       [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                       [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                       [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                       [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                       ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],
                       ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R'] ]

        new_chess_game = ChessVar()
        self.assertEqual(new_chess_game.get_board(), game_board)
        self.assertEqual(new_chess_game.get_game_state(), "UNFINISHED")
        self.assertEqual(new_chess_game.get_turn(), "WHITE")

    def test_2(self):
        """Contains Unit Tests for various games"""
        # ReadMe instructions & Test Stalemate / Unfinished
        game1 = ChessVar()
        game1_board = [['r', 'n', 'b', 'B', 'k', 'b', 'n', 'r'], ['p', 'p', 'p', 'p', ' ', 'p', ' ', 'p'], [' ', ' ', ' ', ' ', 'p', ' ', ' ', ' '], [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], [' ', ' ', ' ', 'P', ' ', ' ', ' ', ' '], [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], ['P', 'P', 'P', ' ', 'P', 'P', 'P', 'P'], ['R', 'N', ' ', 'Q', 'K', 'B', 'N', 'R']]
        game1.make_move('d2', 'd4')
        game1.make_move('g7', 'g5')
        game1.make_move('c1', 'g5')
        game1.make_move('e7', 'e6')
        game1.make_move('g5', 'd8')
        self.assertEqual(game1.get_game_state(), "UNFINISHED")
        self.assertEqual(game1.get_turn(), "BLACK")
        self.assertEqual(game1.get_board(), game1_board)

        # Fool's Mate & Test Black Win
        game2 = ChessVar()
        game2_board = [['r', 'n', 'b', ' ', 'k', 'b', 'n', 'r'], ['p', 'p', 'p', 'p', ' ', 'p', 'p', 'p'], [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], [' ', ' ', ' ', ' ', 'p', ' ', ' ', ' '], [' ', ' ', ' ', ' ', ' ', ' ', 'P', ' '], ['P', ' ', ' ', ' ', ' ', 'P', ' ', ' '], [' ', 'P', 'P', 'P', 'P', ' ', ' ', 'P'], ['R', 'N', 'B', 'Q', 'q', 'B', 'N', 'R']]
        game2.make_move('f2', 'f3')
        game2.make_move('e7', 'e5')
        game2.make_move('g2', 'g4')
        game2.make_move('d8', 'h4')
        game2.make_move('a2', 'a3')
        game2.make_move('h4', 'e1')
        self.assertEqual(game2.get_game_state(), "BLACK_WON")
        self.assertEqual(game2.get_turn(), "BLACK")
        self.assertEqual(game2.get_board(), game2_board)
        # Test to make sure pieces can't move when game is over.
        self.assertEqual(game2.make_move('a7', 'a6'), False)

        # Move to center / King of the Hill Victory & Test White Win
        game3 = ChessVar()
        game3_board = [['r', 'n', 'b', 'q', ' ', 'b', 'n', 'r'], ['p', 'p', 'p', 'p', 'p', ' ', 'p', 'p'], [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], [' ', ' ', ' ', ' ', ' ', 'k', ' ', ' '], [' ', ' ', ' ', 'K', ' ', ' ', ' ', ' '], [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], ['P', 'P', 'P', 'P', ' ', 'P', 'P', 'P'], ['R', 'N', 'B', 'Q', ' ', 'B', 'N', 'R']]
        game3.make_move('e2', 'e4')
        game3.make_move('f7', 'f5')
        game3.make_move('e4', 'f5')
        game3.make_move('e8', 'f7')
        game3.make_move('e1', 'e2')
        game3.make_move('f7', 'f6')
        game3.make_move('e2', 'e3')
        game3.make_move('f6', 'f5')
        game3.make_move('e3', 'd4')
        self.assertEqual(game3.get_game_state(), "WHITE_WON")
        self.assertEqual(game3.get_turn(), "WHITE")
        self.assertEqual(game3.get_board(), game3_board)

        # Testing for Knights
        game4 = ChessVar()
        game4_board = [['r', 'n', 'b', 'q', 'k', 'b', ' ', 'r'], ['p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'], [' ', ' ', ' ', ' ', ' ', 'n', ' ', ' '], [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], [' ', ' ', 'N', ' ', ' ', ' ', ' ', ' '], ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'], ['R', ' ', 'B', 'Q', 'K', 'B', 'N', 'R']]
        game4.make_move('b1', 'c3')
        game4.make_move('g8', 'f6')
        self.assertEqual(game4.get_game_state(), "UNFINISHED")
        self.assertEqual(game4.get_turn(), "WHITE")
        self.assertEqual(game4.get_board(), game4_board)

        # Random Chess.com Game I found
        # Designed to be a stress test, I believe that every type of piece is moved and captured in this game.
        # Thankfully neither player moves their king into the center, since that would trigger the alternative victory condition.
        # The last two moves I created since checkmate doesn't exist in this program.
        # It was hard to find a real chess game that didn't involve castling
        game5 = ChessVar()
        game5_board = [['r', ' ', 'b', ' ', 'r', ' ', ' ', ' '], ['p', 'p', ' ', 'Q', ' ', ' ', ' ', ' '], ['n', ' ', ' ', 'p', ' ', ' ', ' ', 'p'], [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], ['b', ' ', ' ', 'P', ' ', ' ', ' ', ' '], ['P', ' ', 'P', 'K', ' ', ' ', 'P', ' '], [' ', 'R', ' ', ' ', ' ', 'B', ' ', ' ']]

        game5.make_move('e2', 'e4')
        game5.make_move('e7', 'e5')
        game5.make_move('f2', 'f4')
        game5.make_move('e5', 'f4')
        game5.make_move('g1', 'f3')
        game5.make_move('g7', 'g5')
        game5.make_move('h2', 'h4')
        game5.make_move('g5', 'g4')
        game5.make_move('f3', 'e5')
        game5.make_move('g8', 'f6')
        game5.make_move('e5', 'g4')
        game5.make_move('f6', 'e4')
        game5.make_move('d2', 'd3')
        game5.make_move('e4', 'g3')
        game5.make_move('c1', 'f4')
        game5.make_move('g3', 'h1')
        game5.make_move('d1', 'e2')
        game5.make_move('d8', 'e7')
        game5.make_move('g4', 'f6')
        game5.make_move('e8', 'd8')
        game5.make_move('f4', 'c7')
        game5.make_move('d8', 'c7')
        game5.make_move('f6', 'd5')
        game5.make_move('c7', 'd8')
        game5.make_move('d5', 'e7')
        game5.make_move('f8', 'e7')
        game5.make_move('e2', 'g4')
        game5.make_move('d7', 'd6')
        game5.make_move('g4', 'f4')
        game5.make_move('h8', 'g8')
        game5.make_move('f4', 'f7')
        game5.make_move('e7', 'h4')
        game5.make_move('e1', 'd2')
        game5.make_move('g8', 'e8')
        game5.make_move('b1', 'a3')
        game5.make_move('b8', 'a6')
        game5.make_move('f7', 'h5')
        game5.make_move('h4', 'f6')
        game5.make_move('h5', 'h1')
        game5.make_move('f6', 'b2')
        game5.make_move('h1', 'h4')
        game5.make_move('d8', 'd7')
        game5.make_move('a1', 'b1')
        game5.make_move('b2', 'a3')
        game5.make_move('h4', 'a4')
        # Checkmate
        game5.make_move('h7', 'h6')
        game5.make_move('a4', 'd7')

        self.assertEqual(game5.get_game_state(), "WHITE_WON")
        self.assertEqual(game5.get_turn(), "WHITE")
        self.assertEqual(game5.get_board(), game5_board)