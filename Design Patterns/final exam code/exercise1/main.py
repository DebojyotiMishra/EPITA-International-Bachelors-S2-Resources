from Game import Game

print('Example 1')
g = Game(empty=False)
g.display()
print()
g.movePiece('e2', 'e4')
g.display()


print("Exemple 2")
g = Game(empty=True)
g.addPiece('♙', 'e2')
g.addPiece('♙', 'f2')
g.display()
print()
g.movePiece('e2', 'e4')
g.display()