class chessPiece:
    def __init__(self, color):
        self.color = color
        self.simbolo = None 

class Pawn(chessPiece):
    def __init__(self, color):
        super().__init__(color)

    def legal_moves(self):  #
        pass

class Queen(chessPiece):
    def __init__(self, color):
        super().__init__(color)

    def legal_moves(self):  #
        pass

class Rook(chessPiece):
    def __init__(self, color):
        super().__init__(color)

    def legal_moves(self):  #
        pass

class Knight(chessPiece):
    def __init__(self, color):
        super().__init__(color)

    def legal_moves(self):  #
        pass


class Bishop(chessPiece):
    def __init__(self, color):
        super().__init__(color)

    def legal_moves(self):  #
        pass

class King(chessPiece):
    def __init__(self, color):
        super().__init__(color)

    def legal_moves(self):
        pass
    def checkmate(self):
        if ...:
           return True # gg
