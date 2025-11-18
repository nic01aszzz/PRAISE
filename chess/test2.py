class chessPiece:
    def __init__(self, color):
        self.color = color
        self.simbolo = None # Lo definirán las clases hija

class Knight(chessPiece):
    def __init__(self, color):
        super().__init__(color)

caballo = Knight(color= "negro")
print(caballo.color)