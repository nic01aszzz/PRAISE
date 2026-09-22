import sys
import time
import pygame
from renderers import IRenderer
import os

class ConsoleRenderer(IRenderer):
    def __init__(self):
        self.environment_statebuffer = {}

    def observe(self, statebuffer):
        self.environment_statebuffer = statebuffer
    
    def render(self):
        state = self.environment_statebuffer.get_state()
        if state:
            #posibles states: tablero, game_info, status, turn_color, en_passant
            board = state["tablero"]
            filas = ['8', '7', '6', '5', '4', '3', '2', '1']
            columnas = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']

            for fila in filas:
                #para que se vea 1 | P P P P etc
                fila_visual = f"{fila} |" 
                for col in columnas:
                    clave = col + fila
                    pieza = board.get(clave)

                    if pieza is None:
                        fila_visual += ". "
                    else:
                        if type(pieza).__name__ == "Knight":
                            nombre = type(pieza).__name__[1]
                        else:
                            nombre = type(pieza).__name__[0] 
                
                        if pieza.color == "black":
                            nombre = nombre.lower()
                        else:
                            nombre = nombre.upper()
                        fila_visual += nombre + " "
                print(fila_visual + f"| {fila}")
                
            print("  -----------------")
            print("   a b c d e f g h\n")

class PygameRenderer(IRenderer):
    # Se añade action_queue al constructor
    def __init__(self, action_queue=None, window_size=640):
        pygame.init()
        self.width = window_size
        self.height = window_size
        self.sq_size = self.width // 8
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("ChessWorld - Pygame Renderer")
        
        self.statebuffer = None
        self.action_queue = action_queue
        
        # Colores
        self.light_color = (240, 217, 181)
        self.dark_color = (181, 136, 99)
        self.highlight_color = (255, 0, 0) # Celeste para resaltar selección

        # Cadenas para conversión directa de coordenadas
        self.cols = 'abcdefgh'
        self.rows = '87654321' # Invertido, el índice 0 es la fila 8
        
        # Guardará el primer clic del usuario
        self.origen_seleccionado = None

        self.piece_images = {}
        self.cargar_imagenes()

    def cargar_imagenes(self):
        piezas = ['Pawn', 'Knight', 'Bishop', 'Rook', 'Queen', 'King']
        colores = ['white', 'black']
        carpeta_actual = os.path.dirname(os.path.abspath(__file__))
        ruta_carpeta = os.path.join(carpeta_actual, "assets")
        
        for color in colores:
            for pieza in piezas:
                nombre_archivo = f"{color}_{pieza}.png"
                ruta_completa = os.path.join(ruta_carpeta, nombre_archivo)
                
                try:
                    # Cargar la imagen
                    imagen = pygame.image.load(ruta_completa)
                    # Escalarla al tamaño de la casilla usando smoothscale para mejor calidad
                    imagen_escalada = pygame.transform.smoothscale(imagen, (self.sq_size, self.sq_size))
                    # Guardarla en el diccionario usando la tupla (tipo, color) como llave
                    self.piece_images[(pieza, color)] = imagen_escalada
                except FileNotFoundError:
                    print(f"Advertencia: No se encontró la imagen {ruta_completa}")
                    self.piece_images[(pieza, color)] = None

    def observe(self, statebuffer):
        self.statebuffer = statebuffer

    def render(self):
        if self.statebuffer is None:
            return

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                if self.action_queue:
                    self.action_queue.put(("exit", "exit"))
                pygame.quit()
                sys.exit()
                
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and self.action_queue: # Clic izquierdo
                    x, y = pygame.mouse.get_pos()
                    col_idx = x // self.sq_size
                    row_idx = y // self.sq_size
                    
                    if 0 <= col_idx <= 7 and 0 <= row_idx <= 7:
                        casilla_clickeada = self.cols[col_idx] + self.rows[row_idx]
                        
                        if self.origen_seleccionado is None:
                            self.origen_seleccionado = casilla_clickeada
                        else:
                            destino = casilla_clickeada
                            # Si hace clic en la misma casilla, deselecciona
                            if self.origen_seleccionado == destino:
                                self.origen_seleccionado = None
                            else:
                                # Envía a la cola la tupla con el origen y destino
                                self.action_queue.put((self.origen_seleccionado, destino))
                                self.origen_seleccionado = None

        state = self.statebuffer.get_state()
        if not state:
            return

        tablero = state.get("tablero", {})

        for r in range(8):
            for c in range(8):
                color = self.light_color if (r + c) % 2 == 0 else self.dark_color
                rect = pygame.Rect(c * self.sq_size, r * self.sq_size, self.sq_size, self.sq_size)
                pygame.draw.rect(self.screen, color, rect)

        if self.origen_seleccionado:
            c = self.cols.index(self.origen_seleccionado[0])
            r = self.rows.index(self.origen_seleccionado[1])
            rect_sel = pygame.Rect(c * self.sq_size, r * self.sq_size, self.sq_size, self.sq_size)
            pygame.draw.rect(self.screen, self.highlight_color, rect_sel)

        for pos, piece in tablero.items():
            if piece is not None:
                c = self.cols.index(pos[0])
                r = self.rows.index(pos[1])
                
                piece_type = type(piece).__name__
                piece_color = piece.color
                imagen = self.piece_images.get((piece_type, piece_color))
                
                if imagen:
                    self.screen.blit(imagen, (c * self.sq_size, r * self.sq_size))

        if self.origen_seleccionado:
            c = self.cols.index(self.origen_seleccionado[0])
            r = self.rows.index(self.origen_seleccionado[1])
            rect_borde = pygame.Rect(c * self.sq_size, r * self.sq_size, self.sq_size, self.sq_size)
            pygame.draw.rect(self.screen, (255, 0, 0), rect_borde, width=4)

        pygame.display.flip()