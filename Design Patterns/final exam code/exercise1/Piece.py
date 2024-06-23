from dataclasses import dataclass
from typing import List, Union
from abc import ABC, abstractmethod

@dataclass
class Position:
    x: int
    y: int

    def __init__(self, s: str = None):
        self.x = 0
        self.y = 0
        if s is not None:
            self.y = ord(s[0]) - ord('a')
            self.x = int(s[1]) - 1


@dataclass
class Piece(ABC):
    """Abstract class for a chess piece"""

    color: str
    pos: Position
    g: 'Game' = None

    @abstractmethod
    def getValidMoves(self) -> List[Position]:
        # This function will not be used
        return []

    @abstractmethod
    def moveTo(self, target: Position):
        """ Move the piece to a new position"""
        self.g.board[self.pos.x][self.pos.y] = None
        self.pos = target
        self.g.board[self.pos.x][self.pos.y] = self

    @staticmethod
    def from_string(symbol: str, pos: Position = None, g: 'Game' = None) -> 'Piece':
        """Create a piece from a string symbol"""
        if symbol == '♟': return Pawn('black', pos, g)
        elif symbol == '♙': return Pawn('white', pos, g)
        elif symbol == '♜': return Rook('black', pos, g)
        elif symbol == '♖': return Rook('white', pos, g)
        elif symbol == '♞': return Knight('black', pos, g)
        elif symbol == '♘': return Knight('white', pos, g)
        elif symbol == '♝': return Bishop('black', pos, g)
        elif symbol == '♗': return Bishop('white', pos, g)
        elif symbol == '♛': return Queen('black', pos, g)
        elif symbol == '♕': return Queen('white', pos, g)
        elif symbol == '♚': return King('black', pos, g)
        elif symbol == '♔': return King('white', pos, g)
        return None

@dataclass
class Pawn(Piece):
    def getValidMoves(self) -> List[Position]:
        return super().getValidMoves()
    
    def moveTo(self, target: Position):
        super().moveTo(target)

    def __str__(self):
        return '♟' if self.color == 'black' else '♙'

@dataclass
class Rook(Piece):
    def getValidMoves(self) -> List[Position]:
        return super().getValidMoves()
    
    def moveTo(self, target: Position):
        super().moveTo(target)
        if (self.color == 'white' and target.y == 7) or (self.color == 'black' and target.y == 0):
            while True:
                promotion = input("Promote to Q (Queen), R (Rook), B (Bishop), or N (Knight)? ").upper()
                if promotion in ['Q', 'R', 'B', 'N']:
                    if promotion == 'Q':
                        self.game.replacePiece(self, Queen(self.color, target, self.game))
                    elif promotion == 'R':
                        self.game.replacePiece(self, Rook(self.color, target, self.game))
                    elif promotion == 'B':
                        self.game.replacePiece(self, Bishop(self.color, target, self.game))
                    elif promotion == 'N':
                        self.game.replacePiece(self, Knight(self.color, target, self.game))
                    break

    def __str__(self):
        return '♜' if self.color == 'black' else '♖'

@dataclass
class Queen(Piece):
    def getValidMoves(self) -> List[Position]:
        return super().getValidMoves()
    
    def moveTo(self, target: Position):
        super().moveTo(target)

    def __str__(self):
        return '♛' if self.color == 'black' else '♕'

@dataclass
class Bishop(Piece):
    def getValidMoves(self) -> List[Position]:
        return super().getValidMoves()
    
    def moveTo(self, target: Position):
        super().moveTo(target)

    def __str__(self):
        return '♝' if self.color == 'black' else '♗'

@dataclass
class Knight(Piece):
    def getValidMoves(self) -> List[Position]:
        return super().getValidMoves()
    
    def moveTo(self, target: Position):
        super().moveTo(target)

    def __str__(self):
        return '♞' if self.color == 'black' else '♘'

@dataclass
class King(Piece):
    def getValidMoves(self) -> List[Position]:
        return super().getValidMoves()
    
    def moveTo(self, target: Position):
        super().moveTo(target)

    def __str__(self):
        return '♚' if self.color == 'black' else '♔'