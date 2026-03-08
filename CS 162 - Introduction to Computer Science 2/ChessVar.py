# Author: Lucca Truitt
# GitHub username: LuccaTruitt
# Date: 3/10/2025
# Description: Simulates a game of King of the Hill Chess

class ChessPiece:
    """Creates a ChessPiece class that holds various information"""

    def __init__(self, board_position, piece_color):
        """Create a ChessPiece object with board_position, and piece_color"""
        self._board_position = board_position
        self._piece_color = piece_color

    def get_board_position(self):
        """Returns the board position of a piece"""
        return self._board_position

    def set_board_position(self, str_input):
        """Sets the board position of a piece"""
        self._board_position = str_input

    def get_piece_color(self):
        """Returns the color of a piece"""
        return self._piece_color

class KingPiece(ChessPiece):
    """Creates a KingPiece class that holds various information"""

    def __init__(self, board_position, piece_color):
        """Create a KingPiece object"""
        super().__init__(board_position, piece_color)

    def get_piece_type(self):
        """Returns this piece's type"""
        return 'KING'

    def check_piece_move(self, move_from, move_to, board):
        """Checks to see if a King could move from move_from to move_to"""
        # The King can move 1 tile in any direction
        horizontal_distance = abs(ord(move_from[0]) - ord(move_to[0]))
        vertical_distance = abs(int(move_from[1]) - int(move_to[1]))

        # We can assume that both distances can't equal zero, that is checked before this function is called
        if (horizontal_distance > 1) or (vertical_distance > 1):
            return False
        else:
            return True

class QueenPiece(ChessPiece):
    """Creates a QueenPiece class that holds various information"""

    def __init__(self, board_position, piece_color):
        """Create a QueenPiece object"""
        super().__init__(board_position, piece_color)

    def get_piece_type(self):
        """Returns this piece's type"""
        return 'QUEEN'

    def check_piece_move(self, move_from, move_to, board):
        """Checks to see if a Queen could move from move_from to move_to"""
        # The Queen can move like a Bishop and Rook combined.
        horizontal_distance = abs(ord(move_from[0]) - ord(move_to[0]))
        vertical_distance = abs(int(move_from[1]) - int(move_to[1]))

        # We can assume that both distances can't equal zero, that is checked before this function is called
        if ((horizontal_distance > 0) and (vertical_distance > 0)) and (horizontal_distance != vertical_distance):
            return False

        going_down       = False
        going_up         = False
        going_left       = False
        going_right      = False
        going_up_left    = False
        going_up_right   = False
        going_down_left  = False
        going_down_right = False
        current_position = [move_from[0], int(move_from[1])]

        # Rook Style Movement Direction Checks
        if (horizontal_distance == 0) or (vertical_distance == 0):
            # Going up/down
            if move_from[0] == move_to[0]:
                # Going down
                if move_from[1] > move_to[1]:
                    going_down = True
                else:
                    going_up = True

            # Going left/right
            else:
                # Going left
                if move_from[0] > move_to[0]:
                    going_left = True
                # Going right
                else:
                    going_right = True

        # Bishop Style Movement Direction Checks
        else:
            # Going up to the right
            if (move_to[0] > move_from[0]) and (move_to[1] > move_from[1]):
                going_up_right = True

            # Going up to the left
            elif (move_to[0] < move_from[0]) and (move_to[1] > move_from[1]):
                going_up_left = True

            # Going down to the right
            elif (move_to[0] > move_from[0]) and (move_to[1] < move_from[1]):
                going_down_right = True

            # Going down to the left
            else:
                going_down_left = True

        # Function to test if the queen can move down to 'move_to' legally
        if going_down:
            current_position[1] -= 1  # Decrement Number
            while (str(current_position[0]) + str(current_position[1])) != move_to:
                if board.find_piece_at_position(str(current_position[0]) + str(current_position[1])):
                    return False
                current_position[1] -= 1  # Decrement Number
            return True  # Don't need to check the move_to position because we can assume move_to is a valid spot depending on the player's turn.

        # Function to test if the queen can move up to 'move_to' legally
        elif going_up:
            current_position[1] += 1  # Increment Number
            while (str(current_position[0]) + str(current_position[1])) != move_to:
                if board.find_piece_at_position(str(current_position[0]) + str(current_position[1])):
                    return False
                current_position[1] += 1  # Increment Number
            return True  # Don't need to check the move_to position because we can assume move_to is a valid spot depending on the player's turn.

        # Function to test if the queen can move left to 'move_to' legally
        elif going_left:
            # Decrement Letter
            temp_num = ord(current_position[0]) - 1
            current_position[0] = chr(temp_num)
            while (str(current_position[0]) + str(current_position[1])) != move_to:
                if board.find_piece_at_position(str(current_position[0]) + str(current_position[1])):
                    return False
                # Decrement Letter
                temp_num = ord(current_position[0]) - 1
                current_position[0] = chr(temp_num)
            return True  # Don't need to check the move_to position because we can assume move_to is a valid spot depending on the player's turn.

        # Function to test if the queen can move right to 'move_to' legally
        elif going_right:
            # Increment Letter
            temp_num = ord(current_position[0]) + 1
            current_position[0] = chr(temp_num)
            while (str(current_position[0]) + str(current_position[1])) != move_to:
                if board.find_piece_at_position(str(current_position[0]) + str(current_position[1])):
                    return False
                # Increment Letter
                temp_num = ord(current_position[0]) + 1
                current_position[0] = chr(temp_num)
            return True  # Don't need to check the move_to position because we can assume move_to is a valid spot depending on the player's turn.

        # Function to test if the queen can move up to the right to 'move_to' legally
        elif going_up_right:
            # Increment Number
            current_position[1] += 1

            # Increment Letter
            temp_num = ord(current_position[0]) + 1
            current_position[0] = chr(temp_num)

            while (str(current_position[0]) + str(current_position[1])) != move_to:
                if board.find_piece_at_position(str(current_position[0]) + str(current_position[1])):
                    return False
                # Increment Number
                current_position[1] += 1

                # Increment Letter
                temp_num = ord(current_position[0]) + 1
                current_position[0] = chr(temp_num)
            return True

        # Function to test if the queen can move up to the left 'move_to' legally
        elif going_up_left:
            # Increment Number
            current_position[1] += 1

            # Decrement Letter
            temp_num = ord(current_position[0]) - 1
            current_position[0] = chr(temp_num)

            while (str(current_position[0]) + str(current_position[1])) != move_to:
                if board.find_piece_at_position(str(current_position[0]) + str(current_position[1])):
                    return False
                # Increment Number
                current_position[1] += 1

                # Decrement Letter
                temp_num = ord(current_position[0]) - 1
                current_position[0] = chr(temp_num)
            return True

        # Function to test if the queen can move down to the right to 'move_to' legally
        elif going_down_right:
            # Decrement Number
            current_position[1] -= 1

            # Increment Letter
            temp_num = ord(current_position[0]) + 1
            current_position[0] = chr(temp_num)

            while (str(current_position[0]) + str(current_position[1])) != move_to:
                if board.find_piece_at_position(str(current_position[0]) + str(current_position[1])):
                    return False
                # Decrement Number
                current_position[1] -= 1

                # Increment Letter
                temp_num = ord(current_position[0]) + 1
                current_position[0] = chr(temp_num)
            return True

        # Function to test if the queen can move down to the left to 'move_to' legally
        else:
            # Decrement Number
            current_position[1] -= 1

            # Decrement Letter
            temp_num = ord(current_position[0]) - 1
            current_position[0] = chr(temp_num)

            while (str(current_position[0]) + str(current_position[1])) != move_to:
                if board.find_piece_at_position(str(current_position[0]) + str(current_position[1])):
                    return False
                # Decrement Number
                current_position[1] -= 1

                # Decrement Letter
                temp_num = ord(current_position[0]) - 1
                current_position[0] = chr(temp_num)
            return True

class RookPiece(ChessPiece):
    """Creates a RookPiece class that holds various information"""

    def __init__(self, board_position, piece_color):
        """Create a RookPiece object"""
        super().__init__(board_position, piece_color)

    def get_piece_type(self):
        """Returns this piece's type"""
        return 'ROOK'

    def check_piece_move(self, move_from, move_to, board):
        """Checks to see if a Rook could move from move_from to move_to"""
        # The Rook can move any number of tile horizontally or vertically
        horizontal_distance = abs(ord(move_from[0]) - ord(move_to[0]))
        vertical_distance = abs(int(move_from[1]) - int(move_to[1]))

        # We can assume that both distances can't equal zero, that is checked before this function is called
        if (horizontal_distance > 0) and (vertical_distance > 0):
            return False

        # Bool Vars to be used below
        going_down  = False
        going_up    = False
        going_left  = False
        going_right = False
        current_position = [move_from[0], int(move_from[1])]

        # Going up/down
        if move_from[0] == move_to[0]:
            # Going down
            if move_from[1] > move_to[1]:
                going_down = True
            else:
                going_up = True

        # Going left/right
        else:
            # Going left
            if move_from[0] > move_to[0]:
                going_left = True
            # Going right
            else:
                going_right = True

        # Function to test if the rook can move down to 'move_to' legally
        if going_down:
            current_position[1] -= 1 # Decrement Number
            while (str(current_position[0]) + str(current_position[1])) != move_to:
                if board.find_piece_at_position(str(current_position[0]) + str(current_position[1])):
                    return False
                current_position[1] -= 1 # Decrement Number
            return True # Don't need to check the move_to position because we can assume move_to is a valid spot depending on the player's turn.

        # Function to test if the rook can move up to 'move_to' legally
        elif going_up:
            current_position[1] += 1 # Increment Number
            while (str(current_position[0]) + str(current_position[1])) != move_to:
                if board.find_piece_at_position(str(current_position[0]) + str(current_position[1])):
                    return False
                current_position[1] += 1 # Increment Number
            return True # Don't need to check the move_to position because we can assume move_to is a valid spot depending on the player's turn.

        # Function to test if the rook can move left to 'move_to' legally
        elif going_left:
            # Decrement Letter
            temp_num = ord(current_position[0]) - 1
            current_position[0] = chr(temp_num)
            while (str(current_position[0]) + str(current_position[1])) != move_to:
                if board.find_piece_at_position(str(current_position[0]) + str(current_position[1])):
                    return False
                # Decrement Letter
                temp_num = ord(current_position[0]) - 1
                current_position[0] = chr(temp_num)
            return True # Don't need to check the move_to position because we can assume move_to is a valid spot depending on the player's turn.

        # Function to test if the rook can move right to 'move_to' legally
        else:
            # Increment Letter
            temp_num = ord(current_position[0]) + 1
            current_position[0] = chr(temp_num)
            while (str(current_position[0]) + str(current_position[1])) != move_to:
                if board.find_piece_at_position(str(current_position[0]) + str(current_position[1])):
                    return False
                # Increment Letter
                temp_num = ord(current_position[0]) + 1
                current_position[0] = chr(temp_num)
            return True # Don't need to check the move_to position because we can assume move_to is a valid spot depending on the player's turn.

class KnightPiece(ChessPiece):
    """Creates a KnightPiece class that holds various information"""

    def __init__(self, board_position, piece_color):
        """Create a KnightPiece object"""
        super().__init__(board_position, piece_color)

    def get_piece_type(self):
        """Returns this piece's type"""
        return 'KNIGHT'

    def check_piece_move(self, move_from, move_to, board):
        """Checks to see if a Knight could move from move_from to move_to"""
        # A knight movement should be horizontal 2, vertical 1 or vertical 2, horizontal 1 (Using absolute values)
        horizontal_distance = abs(ord(move_from[0]) - ord(move_to[0]))
        vertical_distance = abs(int(move_from[1]) - int(move_to[1]))

        if not (((horizontal_distance == 2) and (vertical_distance == 1)) or ((horizontal_distance == 1) and (vertical_distance == 2))):
            return False

        # With a knight,  direction or if there are any pieces inbetween move_from and move_to doesn't matter, knights can jump over any pieces
        return True

class BishopPiece(ChessPiece):
    """Creates a BishopPiece class that holds various information"""

    def __init__(self, board_position, piece_color):
        """Create a BishopPiece object"""
        super().__init__(board_position, piece_color)

    def get_piece_type(self):
        """Returns this piece's type"""
        return 'BISHOP'

    def check_piece_move(self, move_from, move_to, board):
        """Checks to see if a Bishop could move from move_from to move_to"""
        # The Bishop can move any number of tiles in any diagonal direction
        horizontal_distance = abs(ord(move_from[0]) - ord(move_to[0]))
        vertical_distance = abs(int(move_from[1]) - int(move_to[1]))

        # We can assume that both distances can't equal zero, that is checked before this function is called
        if horizontal_distance != vertical_distance: # Both distances are already absolute values and should always equal each other in a bishops move
            return False

        # Bool Vars to be used below
        going_up_left    = False
        going_up_right   = False
        going_down_left  = False
        going_down_right = False
        current_position = [move_from[0], int(move_from[1])]

        # Going up to the right
        if (move_to[0] > move_from[0]) and (move_to[1] > move_from[1]):
            going_up_right = True

        # Going up to the left
        elif (move_to[0] < move_from[0]) and (move_to[1] > move_from[1]):
            going_up_left = True

        # Going down to the right
        elif (move_to[0] > move_from[0]) and (move_to[1] < move_from[1]):
            going_down_right = True

        # Going down to the left
        else:
            going_down_left = True

        # Function to test if the bishop can move up to the right to 'move_to' legally
        if going_up_right:
            # Increment Number
            current_position[1] += 1

            # Increment Letter
            temp_num = ord(current_position[0]) + 1
            current_position[0] = chr(temp_num)

            while (str(current_position[0]) + str(current_position[1])) != move_to:
                if board.find_piece_at_position(str(current_position[0]) + str(current_position[1])):
                    return False
                # Increment Number
                current_position[1] += 1

                # Increment Letter
                temp_num = ord(current_position[0]) + 1
                current_position[0] = chr(temp_num)
            return True

        # Function to test if the bishop can move up to the left 'move_to' legally
        elif going_up_left:
            # Increment Number
            current_position[1] += 1

            # Decrement Letter
            temp_num = ord(current_position[0]) - 1
            current_position[0] = chr(temp_num)

            while (str(current_position[0]) + str(current_position[1])) != move_to:
                if board.find_piece_at_position(str(current_position[0]) + str(current_position[1])):
                    return False
                # Increment Number
                current_position[1] += 1

                # Decrement Letter
                temp_num = ord(current_position[0]) - 1
                current_position[0] = chr(temp_num)
            return True

        # Function to test if the bishop can move down to the right to 'move_to' legally
        elif going_down_right:
            # Decrement Number
            current_position[1] -= 1

            # Increment Letter
            temp_num = ord(current_position[0]) + 1
            current_position[0] = chr(temp_num)

            while (str(current_position[0]) + str(current_position[1])) != move_to:
                if board.find_piece_at_position(str(current_position[0]) + str(current_position[1])):
                    return False
                # Decrement Number
                current_position[1] -= 1

                # Increment Letter
                temp_num = ord(current_position[0]) + 1
                current_position[0] = chr(temp_num)
            return True

        # Function to test if the bishop can move down to the left to 'move_to' legally
        else:
            # Decrement Number
            current_position[1] -= 1

            # Decrement Letter
            temp_num = ord(current_position[0]) - 1
            current_position[0] = chr(temp_num)

            while (str(current_position[0]) + str(current_position[1])) != move_to:
                if board.find_piece_at_position(str(current_position[0]) + str(current_position[1])):
                    return False
                # Decrement Number
                current_position[1] -= 1

                # Decrement Letter
                temp_num = ord(current_position[0]) - 1
                current_position[0] = chr(temp_num)
            return True

class PawnPiece(ChessPiece):
    """Creates a PawnPiece class that holds various information"""

    def __init__(self, board_position, piece_color):
        """Create a PawnPiece object"""
        super().__init__(board_position, piece_color)

    def get_piece_type(self):
        """Returns this piece's type"""
        return 'PAWN'

    def check_piece_move(self, move_from, move_to, board):
        """Checks to see if a Pawn could move from move_from to move_to"""
        # A pawn's rules are the most complicated (not that complicated, but still)
        # If the pawn is in its starting position, it can move two forward, otherwise it can only move one
        # A pawn can only go forward, unless capturing, which it can ONLY do to piece to the left and right upper sides of it.
        horizontal_distance = abs(ord(move_from[0]) - ord(move_to[0]))
        vertical_distance = int(move_from[1]) - int(move_to[1]) # Negative means it's whites move, positive means it's black's move

        pawn_in_spawn = False

        # Check if the pawn is capturing
        if not board.find_piece_at_position(move_to):
            pawn_is_capturing = False
        else:
            pawn_is_capturing = True

        current_position = [move_from[0], int(move_from[1])]

        # If White's Turn
        if board.get_turn() == 'WHITE':
            # Check if the pawn is 'in spawn'
            if self.get_board_position() in ('a2', 'b2', 'c2', 'd2', 'e2', 'f2', 'g2', 'h2'):
                pawn_in_spawn = True

            if pawn_is_capturing and (horizontal_distance == 1) and (vertical_distance == -1):
                return True

            if pawn_in_spawn and not ((vertical_distance == -1) or (vertical_distance == -2)):
                return False

            if (pawn_in_spawn == False) and vertical_distance != -1:
                return False

            if vertical_distance == -2:
                current_position[1] += 1  # Increment Number
                if board.find_piece_at_position(str(current_position[0]) + str(current_position[1])):
                    return False
                current_position[1] += 1  # Increment Number
                if board.find_piece_at_position(str(current_position[0]) + str(current_position[1])):
                    return False
            else:
                current_position[1] += 1  # Increment Number
                if board.find_piece_at_position(str(current_position[0]) + str(current_position[1])):
                    return False

        # If Black's Turn
        else:
            # Check if the pawn is 'in spawn'
            if self.get_board_position() in ('a7', 'b7', 'c7', 'd7', 'e7', 'f7', 'g7', 'h7'):
                pawn_in_spawn = True

            if pawn_is_capturing and (horizontal_distance == 1) and (vertical_distance == 1):
                return True

            if pawn_in_spawn and not ((vertical_distance == 1) or (vertical_distance == 2)):
                return False

            if (pawn_in_spawn == False) and vertical_distance != 1:
                return False

            if vertical_distance == 2:
                current_position[1] -= 1  # Increment Number
                if board.find_piece_at_position(str(current_position[0]) + str(current_position[1])):
                    return False
                current_position[1] -= 1  # Increment Number
                if board.find_piece_at_position(str(current_position[0]) + str(current_position[1])):
                    return False
            else:
                current_position[1] -= 1  # Increment Number
                if board.find_piece_at_position(str(current_position[0]) + str(current_position[1])):
                    return False

        return True

class ChessVar:
    """Creates a ChessVar class that holds various information"""

    def __init__(self):
        """Creates a ChessVar object with no variable needing to be passed in"""
        self._game_board = [ ['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r'],
                             ['p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'],
                             [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                             [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                             [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                             [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                             ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],
                             ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R'] ]
        self._game_state = int(0)
        self._turn = 'WHITE'
        self._pieces = (
            PawnPiece('a2', 'WHITE'), PawnPiece('b2', 'WHITE'), PawnPiece('c2', 'WHITE'), PawnPiece('d2', 'WHITE'),
            PawnPiece('e2', 'WHITE'), PawnPiece('f2', 'WHITE'), PawnPiece('g2', 'WHITE'), PawnPiece('h2', 'WHITE'),
            RookPiece('a1', 'WHITE'), KnightPiece('b1', 'WHITE'), BishopPiece('c1', 'WHITE'), QueenPiece('d1', 'WHITE'),
            KingPiece('e1', 'WHITE'), BishopPiece('f1', 'WHITE'), KnightPiece('g1', 'WHITE'), RookPiece('h1', 'WHITE'),

            PawnPiece('a7', 'BLACK'), PawnPiece('b7', 'BLACK'), PawnPiece('c7', 'BLACK'), PawnPiece('d7', 'BLACK'),
            PawnPiece('e7', 'BLACK'), PawnPiece('f7', 'BLACK'), PawnPiece('g7', 'BLACK'), PawnPiece('h7', 'BLACK'),
            RookPiece('a8', 'BLACK'), KnightPiece('b8', 'BLACK'), BishopPiece('c8', 'BLACK'), QueenPiece('d8', 'BLACK'),
            KingPiece('e8', 'BLACK'), BishopPiece('f8', 'BLACK'), KnightPiece('g8', 'BLACK'), RookPiece('h8', 'BLACK')
        )

    def get_game_state(self):
        """Returns the game state"""
        if self._game_state == 0:
            return "UNFINISHED"
        elif self._game_state == 1:
            return "WHITE_WON"
        elif self._game_state == 2:
            return "BLACK_WON"
        else:
            return self._game_state, "No Game State (error)"

    def get_board(self):
        """Returns the entire game board"""
        # Doesn't look very good when you print(class.get_board()), print_board is used for cleanly printing the board to the screen
        return self._game_board

    def get_turn(self):
        """Returns which players turn it is"""
        return self._turn

    def print_board(self):
        """Prints the entire game board to the screen, row by row."""
        print(self._game_board[0])
        print(self._game_board[1])
        print(self._game_board[2])
        print(self._game_board[3])
        print(self._game_board[4])
        print(self._game_board[5])
        print(self._game_board[6])
        print(self._game_board[7])

    def find_piece_at_position(self, position):
        """Finds if a piece is located at input position, if not, return false, if true, return the piece object"""
        for item in self._pieces:
            if item.get_board_position() == position:
                return item

        return False

    def change_turn(self):
        """Changes self._turn to the other player's turn"""
        if self._turn == 'WHITE':
            self._turn = 'BLACK'

        else:
            self._turn = 'WHITE'

        return

    def check_legality(self, move_from, move_to):
        """Called by make_move, checks if the given move is legal"""
        # Check if the game is over
        if self.get_game_state() != "UNFINISHED":
            return False

        # Check if inputs have correct length
        if (len(move_from) != 2) or (len(move_to) != 2):
            return False

        # Check if move_from and move_to are the same
        if move_from == move_to:
            return False

        # Check if input number is between 1 and 8
        if not (('1' <= move_from[1] <= '8') and ('1' <= move_to[1] <= '8')):
            return False

        # Check if input letter is between a and h
        if not (('a' <= move_from[0] <= 'h') and ('a' <= move_to[0] <= 'h')):
            return False

        if self._turn == "WHITE":
            # If white's turn, check if white has a piece in move_from position
            if (self.find_piece_at_position(move_from) == False) or self.find_piece_at_position(move_from).get_piece_color() == "BLACK":
                return False
            # If white's turn, check if white has a piece in move_to position
            elif (self.find_piece_at_position(move_to) != False) and self.find_piece_at_position(move_to).get_piece_color() == "WHITE":
                return False


        elif self._turn == "BLACK":
            # If black's turn, check if black has a piece in move_from position
            if (self.find_piece_at_position(move_from) == False) or self.find_piece_at_position(move_from).get_piece_color() == "WHITE":
                return False
            # If black's turm, check if black has a piece in move_to position
            elif (self.find_piece_at_position(move_to) != False) and self.find_piece_at_position(move_to).get_piece_color() == "BLACK":
                return False

        # Check if move is illegal
        if not self.find_piece_at_position(move_from).check_piece_move(move_from, move_to, self):
            return False

        return True

    def make_move(self, move_from, move_to):
        """Moves a piece from position move_from to position move_to"""
        ##########################
        # Check Legality Section #
        ##########################
        # If the following check fails, we can assume that the given move is legal
        if not self.check_legality(move_from, move_to):
            return False


        #####################
        # Make Move Section #
        #####################
        # For easy reference later
        first_piece = self.find_piece_at_position(move_from)

        #  offset for 'a' in ascii and -1 for array offset (start at 0)
        horizontal_val_from = ord(move_from[0]) - 96 - 1
        horizontal_val_to = ord(move_to[0]) - 96 - 1
        # If we input a1, we want to be looking at line 1 (row 7 in array)
        vertical_val_from = abs(int(move_from[1]) - 8)
        vertical_val_to = abs(int(move_to[1]) - 8)

        # Check if we are capturing
        if self.find_piece_at_position(move_to):
            # If we are, vaporize the piece being captured
            self.find_piece_at_position(move_to).set_board_position(' ')

        # Move piece being moved to new position, then make the old position empty
        first_piece.set_board_position(move_to)
        self._game_board[vertical_val_from][horizontal_val_from] = ' '

        # Following if-else block is used to update the visual game board with the correct letter
        # If it's white's piece
        if first_piece.get_piece_color() == 'WHITE':
            if first_piece.get_piece_type() == 'PAWN':
                self._game_board[vertical_val_to][horizontal_val_to] = 'P'

            elif first_piece.get_piece_type() == 'ROOK':
                self._game_board[vertical_val_to][horizontal_val_to] = 'R'

            elif first_piece.get_piece_type() == 'BISHOP':
                self._game_board[vertical_val_to][horizontal_val_to] = 'B'

            elif first_piece.get_piece_type() == 'KNIGHT':
                self._game_board[vertical_val_to][horizontal_val_to] = 'N'

            elif first_piece.get_piece_type() == 'QUEEN':
                self._game_board[vertical_val_to][horizontal_val_to] = 'Q'

            else:
                self._game_board[vertical_val_to][horizontal_val_to] = 'K'

        # If it's black's piece
        else:
            if first_piece.get_piece_type() == 'PAWN':
                self._game_board[vertical_val_to][horizontal_val_to] = 'p'

            elif first_piece.get_piece_type() == 'ROOK':
                self._game_board[vertical_val_to][horizontal_val_to] = 'r'

            elif first_piece.get_piece_type() == 'BISHOP':
                self._game_board[vertical_val_to][horizontal_val_to] = 'b'

            elif first_piece.get_piece_type() == 'KNIGHT':
                self._game_board[vertical_val_to][horizontal_val_to] = 'n'

            elif first_piece.get_piece_type() == 'QUEEN':
                self._game_board[vertical_val_to][horizontal_val_to] = 'q'

            else:
                self._game_board[vertical_val_to][horizontal_val_to] = 'k'


        #############################
        # update game state section #
        #############################
        white_king_alive = False
        black_king_alive = False

        for item in self._pieces:
            if (item.get_piece_type() == 'KING') and (item.get_board_position() != ' '):
                if item.get_piece_color() == 'WHITE':
                    white_king_alive = True
                else:
                    black_king_alive = True

        if not white_king_alive:
            self._game_state = 2 # Black Won
            return True

        if not black_king_alive:
            self._game_state = 1 # White Won
            return True

        # The following 4 if statements check if there is a king piece in the center
        if self.find_piece_at_position('d4'):
            if self.find_piece_at_position('d4').get_piece_type() == 'KING':
                if self.find_piece_at_position('d4').get_piece_color() == 'WHITE':
                    self._game_state = 1  # White Won
                else:
                    self._game_state = 2  # Black Won
                return True

        if self.find_piece_at_position('e4'):
            if self.find_piece_at_position('e4').get_piece_type() == 'KING':
                if self.find_piece_at_position('e4').get_piece_color() == 'WHITE':
                    self._game_state = 1  # White Won
                else:
                    self._game_state = 2  # Black Won
                return True

        if self.find_piece_at_position('d5'):
            if self.find_piece_at_position('d5').get_piece_type() == 'KING':
                if self.find_piece_at_position('d5').get_piece_color() == 'WHITE':
                    self._game_state = 1  # White Won
                else:
                    self._game_state = 2  # Black Won
                return True

        if self.find_piece_at_position('e5'):
            if self.find_piece_at_position('e5').get_piece_type() == 'KING':
                if self.find_piece_at_position('e5').get_piece_color() == 'WHITE':
                    self._game_state = 1  # White Won
                else:
                    self._game_state = 2  # Black Won
                return True


        #######################
        # update turn section #
        #######################
        # If any of the return True statements in the game state section are true, this line would not trigger and the turn wouldn't change (not that would really matter since the game is over)
        self.change_turn()
        
        # return true
        # This return happens when the move was made successfully and game is still ongoing
        return True

def main():
    return

if __name__ == '__main__':
    main()