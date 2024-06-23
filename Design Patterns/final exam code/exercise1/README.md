## Chess: Pawn Promotion

To solve this problem I used the state design pattern.

1. In ```Class Game``` I implemented a ```replacePiece()``` method to replace one piece with another so that it can be used during pawn promotion
    ```bash
    def replacePiece(self, oldPiece: Piece, newPiece: Piece):
        self.board[oldPiece.pos.x][oldPiece.pos.y] = newPiece
        newPiece.pos = oldPiece.pos
        newPiece.g = self
        oldPiece.pos = None
        oldPiece.g = None
    ```


2. In ```Piece.py```, I added more features to the ```moveTo()``` method of the ```Class Pawn```:
    I used an ```if``` statement to check if a pawn was on its last square, and if it was, I asked the user for which piece they would want to promote to.

    ```bash
    promotion = input("Promote to Q (Queen), R (Rook), B (Bishop), or N (Knight)? ").upper()
    ```

    And then, using the ```replacePiece()``` method in the ```Class Game```, I replaced the Pawn with the desired Piece in the final square:

    ```bash
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
    ```