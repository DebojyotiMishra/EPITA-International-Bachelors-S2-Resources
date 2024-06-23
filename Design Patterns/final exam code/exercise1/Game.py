from typing import List, Union
from Piece import Piece, Position


class Game:
    board: List[List[Piece]]

    def __init__(self, empty: bool = True):
        """Initialize the game

        Args:
            empty (bool, optional): If True, the board will be empty. Otherwise, it will be initialized with the default piece setup. Defaults to True.
        """
        self.board = [[None for _ in range(8)] for _ in range(8)]

        if not empty:
            self.addPiece("♜", "a8")
            self.addPiece("♖", "a1")
            self.addPiece("♞", "b8")
            self.addPiece("♘", "b1")
            self.addPiece("♝", "c8")
            self.addPiece("♗", "c1")
            self.addPiece("♛", "d8")
            self.addPiece("♕", "d1")
            self.addPiece("♚", "e8")
            self.addPiece("♔", "e1")
            self.addPiece("♝", "f8")
            self.addPiece("♗", "f1")
            self.addPiece("♞", "g8")
            self.addPiece("♘", "g1")
            self.addPiece("♜", "h8")
            self.addPiece("♖", "h1")
            self.addPiece("♟", "a7")
            self.addPiece("♙", "a2")
            self.addPiece("♟", "b7")
            self.addPiece("♙", "b2")
            self.addPiece("♟", "c7")
            self.addPiece("♙", "c2")
            self.addPiece("♟", "d7")
            self.addPiece("♙", "d2")
            self.addPiece("♟", "e7")
            self.addPiece("♙", "e2")
            self.addPiece("♟", "f7")
            self.addPiece("♙", "f2")
            self.addPiece("♟", "g7")
            self.addPiece("♙", "g2")
            self.addPiece("♟", "h7")
            self.addPiece("♙", "h2")

    def addPiece(self, symbol: str, pos: str):
        """Add a piece to the board

        Args:
            symbol (str): The symbol of the piece (e.g. '♟' for a black pawn, '♙' for a white pawn, etc.)
            pos (str): The position of the piece (e.g. 'e2')
        """
        p = Piece.from_string(symbol, Position(pos), self)
        self.board[p.pos.x][p.pos.y] = p

    def movePiece(self, start: Union[str, Position], end: Union[str, Position]):
        """Move a piece from start to end

        Args:
            start (Union[str, Position]): The starting position (e.g. 'e2' or Position(4, 1)
            end (Union[str, Position]): The ending position (e.g. 'e4' or Position(4, 3)
        """
        start = Position(start) if isinstance(start, str) else start
        end = Position(end) if isinstance(end, str) else end
        p = self.board[start.x][start.y]
        p.moveTo(end)

    def display(self):
        """Display the board"""
        print("  ", end="")
        for j in range(8):
            print(chr(ord("A") + j), end=" ")
        print()
        for i, row in enumerate(self.board):
            print(i + 1, end=" ")
            for j, p in enumerate(row):
                if p is not None:
                    print(p, end=" ")
                else:
                    print(" ", end=" ")
            print()

    def replacePiece(self, oldPiece: Piece, newPiece: Piece):
        """Replace a piece on the board

        Args:
            oldPiece (Piece): The piece to be replaced
            newPiece (Piece): The new piece
        """
        self.board[oldPiece.pos.x][oldPiece.pos.y] = newPiece
        newPiece.pos = oldPiece.pos
        newPiece.g = self
        oldPiece.pos = None
        oldPiece.g = None