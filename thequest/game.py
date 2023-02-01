import pygame as pg

from . import ALTO_P, ANCHO_P
from thequest.screens import Pantalla, PantallaPrincipal, PantallaJuego


class Quest:
    def __init__(self):
        print("Arranca el juego")
        pg.init()
        self.display = pg.display.set_mode((ANCHO_P, ALTO_P))
        pg.display.set_caption("THE QUEST")
        pg.mixer.init()
        self.pantallas = [
            Pantalla(self.display),
            PantallaPrincipal(self.display),
            PantallaJuego(self.display)]

    def jugar(self):
        for pantalla in self.pantallas:
            pantalla.bucle_principal()