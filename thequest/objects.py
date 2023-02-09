import os
import random

import pygame as pg
from pygame.sprite import Sprite

from . import ANCHO_P, ALTO_P, COLOR_TEXTO2, FPS, MARGEN_LATERAL, POS_PLANETA, PUNTOS_PARTIDA


class Nave(Sprite): # Objeto nave

    def __init__(self):
        super().__init__()
        self.image = pg.image.load(os.path.join(
            "resources", "images", "spaceship.png"))
        self.rect = self.image.get_rect()
        self.rect.y = ALTO_P/2
        self.rect.x = MARGEN_LATERAL
        self.angulo = 0
        self.velocidad_mover = 5
        self.velocidad_aterrizar = 1

        # Conjunto de flags que controlan el comportamiento de la nave
        self.nave_escondida = False
        self.nave_aterrizando = False
        self.rotacion = False
        self.fin_rotacion = False

    def esconder_nave(self): # Posicion nave
        self.tiempo_renacer = pg.time.get_ticks()/1000
        self.nave_escondida = True
        self.rect.centery = -1000
        self.rect.x = -1000

    def aterrizar_nave(self, aterrizando, pantalla): # Aterrizaje
        self.nave_aterrizando = aterrizando
        if aterrizando:
            self.rect.x += self.velocidad_aterrizar
            if self.rect.y > (ALTO_P - self.rect.height)/2:
                self.rect.y -= self.velocidad_aterrizar
            else:
                self.rect.y += self.velocidad_aterrizar

            if self.rect.x > ANCHO_P/2 + 45:
                self.rect.x = ANCHO_P/2 + 45
                self.rect.centery = ALTO_P/2
                self.rotacion = True

                if self.angulo == 180:
                    self.rotacion = False
                    self.fin_rotacion = True
                    img_rotada2 = pg.transform.rotate(self.image, 180)
                    rect_rotado2 = img_rotada2.get_rect(
                        center=self.rect.center)
                    pantalla.blit(img_rotada2, rect_rotado2)

                if self.rotacion:
                    self.angulo += 2
                    img_rotada = pg.transform.rotate(self.image, self.angulo)
                    rect_rotado = img_rotada.get_rect(center=self.rect.center)
                    pantalla.blit(img_rotada, rect_rotado)

            else:
                pantalla.blit(self.image, self.rect)

    def mover_nave(self, aterrizando): # Mover nave
        tecla_mov = pg.key.get_pressed()
        if not aterrizando:
            if tecla_mov[pg.K_UP]:
                self.rect.y -= self.velocidad_mover
                if self.rect.top < 0:
                    self.rect.y = 0
            if tecla_mov[pg.K_DOWN]:
                self.rect.y += self.velocidad_mover
                if self.rect.bottom > ALTO_P:
                    self.rect.bottom = ALTO_P

    def update(self): # Aparicion nave tras muerte

        self.mover_nave(self.nave_aterrizando)

        # Esta parte del código permite devolver la nave a su punto original pasado un tiempo
        # tras perder una vida
        if self.nave_escondida and pg.time.get_ticks()/1000 - self.tiempo_renacer > 2:
            self.nave_escondida = False
            self.rect.centery = ALTO_P/2
            self.rect.x = MARGEN_LATERAL


class Meteorito(Sprite): # Meteorito grande
    puntuacion = PUNTOS_PARTIDA

    def __init__(self, puntuacion):
        super().__init__()
        self.puntos = puntuacion
        self.w = 128
        self.h = 128
        self.image = pg.Surface((self.w, self.h), pg.SRCALPHA)
        self.plantilla_imagenes = pg.image.load(os.path.join(
            "resources", "images", "asteroids.png"))
        self.rect = self.image.get_rect()
        self.rect.x = ANCHO_P - self.rect.width
        self.rect.y = random.randrange(ALTO_P-self.rect.height)
        self.velocidad_x = random.randint(3, 5)

        # Código para almacenar los frames del sprite sheet en una lista
        self.imagenes = []
        self.contador = 0
        self.tiempo_animacion = FPS // 4
        self.momento_actual = 0
        self.filas = 4
        self.columnas = 8
        self.cargarFrames(self.plantilla_imagenes, self.filas, self.columnas)

    def cargarFrames(self, sprite_sheet, no_fila, no_columna): # Preparar animacion
        for fila in range(no_fila):
            y = fila * self.h
            for columna in range(no_columna):
                x = columna * self.w
                image = pg.Surface((self.w, self.h), pg.SRCALPHA)
                image.blit(sprite_sheet, (0, 0), (x, y, self.w, self.h))
                self.imagenes.append(image)

                self.imagenes_cargadas = 0
                self.imagenes_cargadas = len(self.imagenes)
                self.image = self.imagenes[self.contador]

    def update(self):
        # para animar los frames de la imagen del meteorito
        self.momento_actual += self.tiempo_animacion
        if self.momento_actual == FPS:
            self.momento_actual = 0
            self.contador += 1

            if self.contador >= self.imagenes_cargadas:
                self.contador = 0

            self.image = self.imagenes[self.contador]

        # controla la velocidad del meteorito
        self.rect.x -= self.velocidad_x

        # controla que el meteorito no se salga por abajo y por arriba
        if self.rect.bottom == ALTO_P:
            self.rect.y = ALTO_P
        if self.rect.top == 0:
            self.rect.y = 150


class MeteoritoMediano(Meteorito): # Meteorito mediano

    def __init__(self, puntuacion):
        super().__init__(puntuacion)
        self.w = 85
        self.h = 85
        self.velocidad_x = random.randint(4, 6)
        self.plantilla_imagenes = pg.image.load(os.path.join(
            "resources", "images", "asteroids_medium.png"))

        # Para almacenar los frames del sprite sheet del meteorito mediano
        self.imagenes = []
        self.tiempo_animacion = FPS // 3
        self.cargarFrames(self.plantilla_imagenes, self.filas, self.columnas)

class Planeta(Sprite): # Planeta

    def __init__(self, imagen):
        self.image = imagen
        self.rect = self.image.get_rect()
        self.rect.x = POS_PLANETA
        self.rect.y = (ALTO_P-self.image.get_height())/2
        self.velocidad_x = 1

    def mover_planeta(self, nave_aterrizando):
        if nave_aterrizando:
            self.rect.x -= self.velocidad_x
            if self.rect.x < ANCHO_P - self.rect.height:
                self.rect.x = ANCHO_P - self.rect.height


class Explosion(Sprite): # Explosiones nave tras colision

    def __init__(self, centro):
        super().__init__()
        self.w = 100
        self.h = 100
        self.image = pg.Surface((self.w, self.h), pg.SRCALPHA)
        self.rect = self.image.get_rect()
        self.rect.center = centro

        # Almacena las imágenes del sprite sheet y se establecen los atributos de animación
        self.imagenes = []
        self.contador = 0
        self.tiempo_animacion = FPS // 2

        self.act_tiempo = pg.time.get_ticks()
        self.cargarFrames()

    def cargarFrames(self): # Preparar animacion

        sprite_sheet = pg.image.load(os.path.join(
            "resources", "images", "imagen_explosiones.png"))

        for fila in range(6):
            y = fila * self.h
            for columna in range(6):
                x = columna * self.w
                image = pg.Surface((self.w, self.h), pg.SRCALPHA)
                image.blit(sprite_sheet, (0, 0), (x, y, self.w, self.h))
                self.imagenes.append(image)

    def update(self):
        ahora = pg.time.get_ticks()
        if ahora - self.act_tiempo > self.tiempo_animacion:
            self.contador += 1
            self.act_tiempo = ahora

            if self.contador == len(self.imagenes):
                self.kill()

            else:
                self.image = self.imagenes[self.contador]


class Marcador: # Marcador de puntos

    def __init__(self, vidas_iniciales):
        self.valor = 0
        self.vidas = vidas_iniciales
        font_file = os.path.join("resources", "fonts",
                                 "sans_serif_plus_7.ttf")
        self.tipografia = pg.font.Font(font_file, 20)

    def perder_vida(self):
        self.vidas -= 1
        return self.vidas < 1

    def sumar_vida(self):
        self.vidas += 1

    def aumentar_puntos(self, puntos):
        self.valor += puntos

    def pintar_marcador(self, pantalla):
        margen_x_puntos = 600
        margen_x_vidas = 100
        margen_y = 30
        texto_puntos = f"Puntos: {self.valor}"
        texto_vidas = f"Vidas: {self.vidas}"

        render_vidas = self.tipografia.render(
            str(texto_vidas), True, COLOR_TEXTO2)
        render_marcador = self.tipografia.render(
            str(texto_puntos), True, COLOR_TEXTO2)

        pos_x_vidas = render_vidas.get_width() + margen_x_vidas
        pos_y_vidas = ALTO_P - render_vidas.get_height() - margen_y
        pg.surface.Surface.blit(pantalla, render_vidas,
                                (pos_x_vidas, pos_y_vidas))

        pos_x_puntos = render_marcador.get_width() + margen_x_puntos
        pos_y_puntos = ALTO_P - render_marcador.get_height() - margen_y
        pg.surface.Surface.blit(pantalla, render_marcador,
                                (pos_x_puntos, pos_y_puntos))