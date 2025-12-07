fen_string = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
fen_parts = fen_string.split()
fen_rows = fen_parts[0].split("/")
for i, j in enumerate(fen_rows):
    print(i,j)