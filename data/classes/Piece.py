import pygame


class Piece:
    def __init__(self, pos, color, board):
        self.pos = pos
        self.x = pos[0]
        self.y = pos[1]
        self.color = color
        self.has_moved = False

    def move(self, board, square, force=False):
        for i in board.squares:
            i.highlight = False
        output = None
        if square in self.get_valid_moves(board) or force:
            prev_square = board.get_square_from_pos(self.pos)
            self.pos, self.x, self.y = square.pos, square.x, square.y

            prev_square.occupying_piece = None
            square.occupying_piece = self
            board.selected_piece = None
            self.has_moved = True

            # Pawn promotion
            if self.notation == " ":
                if self.y == 0 or self.y == 7:
                    board.promotion_square = square

            # en_passant
            if self.notation == " ":

                if square.en_passant == "white" and self.color == "black":
                    passant_square = board.get_square_from_pos(
                        (self.pos[0], self.pos[1] - 1)
                    )
                    passant_square.occupying_piece = None

                if square.en_passant == "black" and self.color == "white":
                    passant_square = board.get_square_from_pos(
                        (self.pos[0], self.pos[1] + 1)
                    )
                    passant_square.occupying_piece = None
            # clear en_passant squares
            for i in board.squares:
                i.en_passant = None

            # add en_passant squares
            if self.notation == " ":
                distance = abs(prev_square.pos[1] - self.pos[1])
                if distance == 2:
                    if self.color == "white":

                        middle_square = board.get_square_from_pos(
                            (self.pos[0], self.pos[1] + 1)
                        )
                        middle_square.en_passant = "white"

                    if self.color == "black":

                        middle_square = board.get_square_from_pos(
                            (self.pos[0], self.pos[1] - 1)
                        )
                        middle_square.en_passant = "black"
            # Castling
            if self.notation == "K":
                if prev_square.x - self.x == 2:
                    rook = board.get_piece_from_pos((0, self.y))
                    rook.move(board, board.get_square_from_pos((3, self.y)), force=True)
                elif prev_square.x - self.x == -2:
                    rook = board.get_piece_from_pos((7, self.y))
                    rook.move(board, board.get_square_from_pos((5, self.y)), force=True)
            output = True
        else:
            board.selected_piece = None
            output = False
        return output

    # Gets all the available moves
    def get_moves(self, board):
        output = []
        for direction in self.get_possible_moves(board):
            for square in direction:
                if square.occupying_piece is not None:
                    if square.occupying_piece.color == self.color:
                        break
                    else:
                        output.append(square)
                        break
                else:
                    output.append(square)
        return output

    # Checks if the last player does a move that checked our current player
    def get_valid_moves(self, board):
        output = []
        for square in self.get_moves(board):
            if not board.is_in_check(self.color, board_change=[self.pos, square.pos]):
                output.append(square)

        return output

    # True for all pieces except pawn
    def attacking_squares(self, board):
        return self.get_moves(board)

    def change_cord(self, x, y):
        self.pos, self.x, self.y = (x, y), x, y
