import pygame

from data.classes.Square import Square
from data.classes.pieces.Rook import Rook
from data.classes.pieces.Bishop import Bishop
from data.classes.pieces.Knight import Knight
from data.classes.pieces.Queen import Queen
from data.classes.pieces.King import King
from data.classes.pieces.Pawn import Pawn


# Game state checker
class Board:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.tile_width = width // 8
        self.tile_height = height // 8
        self.selected_piece = None
        self.turn = "white"
        self.promotion_square = None
        self.middle_pre_pieces = []

        self.config = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bP", "bP", "bP", "bP", "bP", "bP", "bP", "bP"],
            ["", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", ""],
            ["wP", "wP", "wP", "wP", "wP", "wP", "wP", "wP"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"],
        ]

        self.squares = self.generate_squares()

        self.setup_board()

        self.middle_squares = [
            self.get_square_from_pos((3, 3)),
            self.get_square_from_pos((3, 4)),
            self.get_square_from_pos((4, 3)),
            self.get_square_from_pos((4, 4)),
        ]

    def generate_squares(self):
        output = []
        for y in range(8):
            for x in range(8):
                output.append(Square(x, y, self.tile_width, self.tile_height))
        return output

    def get_square_from_pos(self, pos):
        for square in self.squares:
            if (square.x, square.y) == (pos[0], pos[1]):
                return square

    def get_piece_from_pos(self, pos):
        return self.get_square_from_pos(pos).occupying_piece

    def setup_board(self):
        # iterating 2d list
        for y, row in enumerate(self.config):
            for x, piece in enumerate(row):
                if piece != "":
                    square = self.get_square_from_pos((x, y))

                    # lputting piece classes iin squares
                    if piece[1] == "R":
                        square.occupying_piece = Rook(
                            (x, y), "white" if piece[0] == "w" else "black", self
                        )

                    elif piece[1] == "N":
                        square.occupying_piece = Knight(
                            (x, y), "white" if piece[0] == "w" else "black", self
                        )

                    elif piece[1] == "B":
                        square.occupying_piece = Bishop(
                            (x, y), "white" if piece[0] == "w" else "black", self
                        )

                    elif piece[1] == "Q":
                        square.occupying_piece = Queen(
                            (x, y), "white" if piece[0] == "w" else "black", self
                        )

                    elif piece[1] == "K":
                        square.occupying_piece = King(
                            (x, y), "white" if piece[0] == "w" else "black", self
                        )

                    elif piece[1] == "P":
                        square.occupying_piece = Pawn(
                            (x, y), "white" if piece[0] == "w" else "black", self
                        )

    def handle_click(self, mx, my):
        x = mx // self.tile_width
        y = my // self.tile_height
        clicked_square = self.get_square_from_pos((x, y))
        # Select a piece
        if self.promotion_square is None:
            if self.selected_piece is None:
                if clicked_square.occupying_piece is not None:
                    if clicked_square.occupying_piece.color == self.turn:
                        self.selected_piece = clicked_square.occupying_piece

            elif self.selected_piece.move(self, clicked_square):
                self.turn = "white" if self.turn == "black" else "black"
            # Select new piece when a piece is already selected
            elif clicked_square.occupying_piece is not None:
                if clicked_square.occupying_piece.color == self.turn:
                    self.selected_piece = clicked_square.occupying_piece
        # handle promotion
        else:
            if clicked_square.promotion:
                clicked_square.occupying_piece.change_cord(
                    self.promotion_square.occupying_piece.x,
                    self.promotion_square.occupying_piece.y,
                )
                self.promotion_square.occupying_piece = clicked_square.occupying_piece
                for i in range(4):
                    self.middle_squares[i].highlight = False
                    self.middle_squares[i].promotion = False
                    self.middle_squares[i].occupying_piece = self.middle_pre_pieces[i]
                self.promotion_square = None
                self.middle_pre_pieces = []

    def is_in_check(
        self, color, board_change=None
    ):  # board_change = [(x1, y1), (x2, y2)]
        output = False
        king_pos = None

        changing_piece = None
        old_square = None
        new_square = None
        new_square_old_piece = None

        if board_change is not None:
            for square in self.squares:
                if square.pos == board_change[0]:
                    changing_piece = square.occupying_piece
                    old_square = square
                    old_square.occupying_piece = None
            for square in self.squares:
                if square.pos == board_change[1]:
                    new_square = square
                    new_square_old_piece = new_square.occupying_piece
                    new_square.occupying_piece = changing_piece

        pieces = [
            i.occupying_piece for i in self.squares if i.occupying_piece is not None
        ]

        if changing_piece is not None:
            if changing_piece.notation == "K":
                king_pos = new_square.pos
        if king_pos == None:
            for piece in pieces:
                if piece.notation == "K" and piece.color == color:
                    king_pos = piece.pos
        for piece in pieces:
            if piece.color != color:
                for square in piece.attacking_squares(self):
                    if square.pos == king_pos:
                        output = True

        if board_change is not None:
            old_square.occupying_piece = changing_piece
            new_square.occupying_piece = new_square_old_piece

        return output

    def is_in_checkmate(self, color):
        output = False
        for i in self.squares:
            piece = i.occupying_piece
            if piece != None:
                if piece.notation == "K" and piece.color == color:
                    king_square = i
                    king = piece

        if king.get_valid_moves(self) == []:
            if self.is_in_check(color):

                king_square.highlight = True
                output = True

        return output

    def is_in_stalemate(self, color):
        pass

    def draw(self, display):
        # Highlights all the possible moves of a piece
        if self.selected_piece is not None:
            self.get_square_from_pos(self.selected_piece.pos).highlight = True
            for square in self.selected_piece.get_valid_moves(self):
                square.highlight = True

        # Draw select_promotion squares
        if self.promotion_square is not None:
            promotion_piece = self.promotion_square.occupying_piece
            for i in range(4):
                self.middle_squares[i].highlight = True
                self.middle_squares[i].promotion = True
                self.middle_pre_pieces.append(self.middle_squares[i].occupying_piece)

            self.middle_squares[0].occupying_piece = Queen(
                (3, 3), promotion_piece.color, self
            )
            self.middle_squares[1].occupying_piece = Rook(
                (3, 4), promotion_piece.color, self
            )
            self.middle_squares[2].occupying_piece = Knight(
                (4, 3), promotion_piece.color, self
            )
            self.middle_squares[3].occupying_piece = Bishop(
                (4, 4), promotion_piece.color, self
            )

        for square in self.squares:
            square.draw(display)