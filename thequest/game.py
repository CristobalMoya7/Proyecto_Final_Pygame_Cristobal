import pygame as pg
import os
from . import ALTO_P, ANCHO_P
from .screens import PantallaPrincipal

class Quest:
    def __init__(self):
        pg.init()
        self.display = pg.display.set_mode((ANCHO_P, ALTO_P))
        icono_juego = pg.image.load(os.path.join(
            "resources", "images", "icono_planeta.png"))
        pg.display.set_icon(icono_juego)
        pg.display.set_caption("THE QUEST")
        pg.mixer.init()
    
        