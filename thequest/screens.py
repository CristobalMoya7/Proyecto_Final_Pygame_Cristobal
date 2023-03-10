import os
import random
import pygame as pg

from . import ANCHO_P, ALTO_P, COLOR_TEXTO, COLOR_TEXTO2, FPS, MARGEN_INFERIOR_TEXTOS, MAX_METEO_1, MAX_METEO_2, MAX_METEO_M_1, MAX_METEO_M_2, MIN_METEO_1, MIN_METEO_2, MIN_METEO_M_1, MIN_METEO_M_2, MUSICA_FADE_OUT, PUNTOS_1, PUNTOS_2, PUNTOS_M_1, PUNTOS_M_2, PUNTOS_M_DR, PUNTOS_PARTIDA, RUTA

from .objects import Explosion, Meteorito, MeteoritoMediano, Nave, Planeta
from .records import GestorBD, InputBox


class Pantalla:
    "Clase base de la pantalla de la que heredan el resto"

    def __init__(self, pantalla: pg.Surface):

        self.pantalla = pantalla
        self.reloj = pg.time.Clock()

    def bucle_principal(self):
        pass


class PantallaPrincipal(Pantalla):
    "Clase que controla la pantalla principal"

    def __init__(self, pantalla: pg.Surface):
        super().__init__(pantalla)

        font_file = os.path.join("resources", "fonts",
                                 "light_sans_serif_7.ttf")
        font_file2 = os.path.join("resources", "fonts",
                                  "game_sans_serif_7.ttf")
        self.tipo_titulo = pg.font.Font(font_file, 100)
        self.tipo_historia = pg.font.Font(font_file2, 30)
        self.tipo_info = pg.font.Font(font_file2, 20)

    def bucle_principal(self):
        salir = False
        while not salir:
            for event in pg.event.get():
                if event.type == pg.KEYDOWN and event.key == pg.K_h:
                    salir = True
                if event.type == pg.QUIT:
                    pg.quit()
            self.pintar_fondo()
            self.pintar_texto_titulo()
            self.pintar_texto_instrucciones()
            self.pintar_texto_historia()
            pg.display.flip()

    def pintar_fondo(self):
        self.fondo = pg.image.load(os.path.join(
            "resources", "images", "fondo_intro.jpg"))
        self.pantalla.blit(self.fondo, (0, 0))

    def pintar_texto_historia(self):
        mensaje = 'Pulsa "H" para conocer la historia del juego'
        texto = self.tipo_historia.render(mensaje, True, COLOR_TEXTO2)
        ancho_texto = texto.get_width()
        pos_x = (ANCHO_P - ancho_texto)/2
        pos_y = ALTO_P - MARGEN_INFERIOR_TEXTOS
        self.pantalla.blit(texto, (pos_x, pos_y))

    def pintar_texto_instrucciones(self):

        posiciones = [275, 350, 400, 450, 500, 550]
        mensajes = ["Como jugar:", "1. Pulsa ARRIBA/ABAJO para mover la nave.",
                    "2. Esquiva los meteoritos para ganar puntos.",
                    "3. Tienes 3 vidas.",
                    "4. Pierdes vidas si chocas con los meteoritos.",
                    "5. Aguanta el tiempo suficiente para aterrizar en el planeta."]

        pos_x = ANCHO_P//5
        conta_posiciones = 0

        for mensaje in mensajes:
            texto_render = self.tipo_info.render(
                (mensaje), True, COLOR_TEXTO)
            self.pantalla.blit(
                texto_render, (pos_x, posiciones[conta_posiciones]))
            conta_posiciones += 1

    def pintar_texto_titulo(self):
        mensaje = "THE QUEST"
        texto = self.tipo_titulo.render(mensaje, True, COLOR_TEXTO2)
        ancho_texto = texto.get_width()
        pos_x = (ANCHO_P - ancho_texto)/2
        pos_y = ALTO_P/8
        self.pantalla.blit(texto, (pos_x, pos_y))


class PantallaHistoria(Pantalla): # Historia

    def __init__(self, pantalla: pg.Surface):
        super().__init__(pantalla)

        font_file = os.path.join("resources", "fonts",
                                 "light_sans_serif_7.ttf")
        font_file2 = os.path.join("resources", "fonts",
                                  "game_sans_serif_7.ttf")
        self.tipo_titulo = pg.font.Font(font_file, 75)
        self.tipo_juego = pg.font.Font(font_file2, 30)
        self.tipo_info = pg.font.Font(font_file2, 25)

    def bucle_principal(self):
        salir = False

        while not salir:
            for event in pg.event.get():
                if event.type == pg.KEYDOWN and event.key == pg.K_RETURN:
                    salir = True
                if event.type == pg.QUIT:
                    pg.quit()
            self.pintar_fondo()
            self.pintar_texto_historia()
            self.pintar_texto_partida()
            pg.display.flip()

    def pintar_fondo(self):
        self.fondo = pg.image.load(os.path.join(
            "resources", "images", "fondo_intro.jpg"))
        self.pantalla.blit(self.fondo, (0, 0))

    def pintar_texto_historia(self):
        # Pinta el texto del a??o
        anio = "2045"
        texto = self.tipo_titulo.render(anio, True, COLOR_TEXTO2)
        ancho_texto = texto.get_width()
        pos_x = (ANCHO_P - ancho_texto)//2
        pos_y = ALTO_P/6
        self.pantalla.blit(texto, (pos_x, pos_y))

        # Pinta el texto de la historia
        posiciones = [300, 350, 400, 475, 525]
        mensajes = ["A??o 2034, la tierra ha sido destruida debido a la contaminacion.",
                    "Los unicos supervivientes viajan en una nave espacial,",
                    "en busca de un nuevo planeta habitable.",
                    "Sobrevive a los grandes peligros del espacio ",
                    "para poder salvar a la raza humana."]

        pos_x = ANCHO_P - 900
        conta_posiciones = 0

        for mensaje in mensajes:
            texto_render = self.tipo_info.render(
                (mensaje), True, COLOR_TEXTO)
            self.pantalla.blit(
                texto_render, (pos_x, posiciones[conta_posiciones]))
            conta_posiciones += 1

    def pintar_texto_partida(self):
        mensaje = 'Pulsa "INTRO" para comenzar la partida'
        texto = self.tipo_juego.render(mensaje, True, COLOR_TEXTO2)
        ancho_texto = texto.get_width()
        pos_x = (ANCHO_P - ancho_texto)//2
        pos_y = ALTO_P - MARGEN_INFERIOR_TEXTOS
        self.pantalla.blit(texto, (pos_x, pos_y))


class PantallaJuego(Pantalla): # Primer nivel

    def __init__(self, pantalla: pg.Surface, marcador):
        super().__init__(pantalla)

        # creaci??n de la nave
        self.nave = Nave()

        # creaci??n de los meteoritos de nivel 1
        self.meteoritos = pg.sprite.Group()
        self.crear_meteoritos(MIN_METEO_1, MAX_METEO_1, PUNTOS_1)

        self.meteoritos_m = pg.sprite.Group()
        self.crear_meteoritos_m(MIN_METEO_M_1, MAX_METEO_M_1, PUNTOS_M_1)

        # creaci??n del planeta
        imagen_planeta1 = pg.image.load(os.path.join("resources", "images",
                                                     "planeta1.png"))
        self.planeta = Planeta(imagen_planeta1)

        # creaci??n de las explosiones
        self.explosiones = pg.sprite.Group()

        # creaci??n del marcador de puntos
        self.marcador = marcador

        # carga del sonido de la explosi??n
        self.sonido_explosion = pg.mixer.Sound(os.path.join(
            "resources", "sounds", "sonido_explosion.wav"))

        # carga de la m??sica del juego
        self.musica = pg.mixer.music.load(os.path.join(
            "resources", "sounds", "musica_juego.mp3"))

    def bucle_principal(self): # Control juego

        # Punto para empezar a contar los ticks del juego
        ticks_juego = pg.time.get_ticks()

        # Flags de salida del juego
        salir = False
        game_over = False

        # Flag de la fase de aterrizaje
        aterrizaje = False

        # Reproducci??n de la m??sica del juego (BUCLE!!!)
        pg.mixer.music.play(-1)

        while not salir:
            self.reloj.tick(FPS)

            # para medir el tiempo que transcurre durante la partida
            contador_juego = (pg.time.get_ticks() - ticks_juego)//1000

            # Cerrar juego
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                if self.nave.fin_rotacion:
                    if event.type == pg.KEYDOWN and event.key == pg.K_q:
                        salir = True

            # Para pintar el fondo del nivel
            self.pintar_fondo()

            # Para mover y pintar la nave y mover el planeta cuando la nave aterrice
            self.mover_nave_planeta(aterrizaje)

            # Para pintar objetos que forman parte de la partida
            self.pintar_objetos_partida()

            # Colisi??n de la nave con meteorito, aparece explosion (efecto y sonido) y
            # desaparece la nave. Tambi??n desactiva colisiones durante el aterrizaje
            self.comportamiento_meteoritos(aterrizaje,
                                           MIN_METEO_1, MAX_METEO_1, PUNTOS_1, MIN_METEO_M_1, MAX_METEO_M_2, PUNTOS_M_1)

            # Para pintar el marcador de puntos
            self.marcador.pintar_marcador(self.pantalla)

            # Condici??n que activa el flag de aterrizaje (Tiempo transcurrido)
            if contador_juego == 45:
                aterrizaje = True

            # Condiciones para realizar la finalizaci??n de nivel 1
            if self.nave.fin_rotacion:
                self.pintar_fin_nivel("??NIVEL 1 SUPERADO!")
                self.pintar_nivel_2()

            # Actualizaci??n de todos los elementos que se est??n mostrando en la partida
            pg.display.flip()

            # Para cerrar el juego si se pierden todas las vidas
            if self.marcador.vidas == 0:
                self.pintar_fin_nivel("HAS PERDIDO :(")
                game_over = True
                self.lanzarRecord()
                salir = True

        return game_over

    def crear_meteoritos(self, num_min, num_max, no_puntos): # Meteoritos grandes
        cantidad_meteoritos = random.randrange(num_min, num_max)
        for i in range(cantidad_meteoritos):
            puntos = (i + no_puntos) - i
            meteorito = Meteorito(puntos)
            self.meteoritos.add(meteorito)

    def crear_meteoritos_m(self, num_min, num_max, no_puntos): # Meteoritos medianos
        cantidad_meteoritos_m = random.randrange(num_min, num_max)
        for i in range(cantidad_meteoritos_m):
            puntos_m = (i + no_puntos) - i
            meteorito_m = MeteoritoMediano(puntos_m)
            self.meteoritos_m.add(meteorito_m)

    def comportamiento_meteoritos(self, aterrizar, num_min, num_max, puntos,
                                  num_m_min, num_m_max, puntos_m): # Comportamiento meteoritos
        if not aterrizar:
            colision = pg.sprite.spritecollide(
                self.nave, self.meteoritos, True)
            colision_m = pg.sprite.spritecollide(
                self.nave, self.meteoritos_m, True)

            if colision or colision_m:
                explosion = Explosion(self.nave.rect.center)
                self.explosiones.add(explosion)
                self.nave.esconder_nave()
                self.sonido_explosion.play()
                self.marcador.perder_vida()

            for meteorito in self.meteoritos.sprites():
                if meteorito.rect.right < 0:
                    if not self.nave.nave_escondida:
                        self.marcador.aumentar_puntos(meteorito.puntos)
                    self.meteoritos.remove(meteorito)
            if len(self.meteoritos.sprites()) < 1:
                self.crear_meteoritos(num_min, num_max, puntos)

            for meteorito_m in self.meteoritos_m.sprites():
                if meteorito_m.rect.right < 0:
                    if not self.nave.nave_escondida:
                        self.marcador.aumentar_puntos(meteorito_m.puntos)
                    self.meteoritos_m.remove(meteorito_m)
            if len(self.meteoritos_m.sprites()) < 1:
                self.crear_meteoritos_m(num_m_min, num_m_max, puntos_m)
        else:
            self.meteoritos.clear(self.pantalla, self.pantalla)
            self.meteoritos_m.clear(self.pantalla, self.pantalla)

    def lanzarRecord(self): # Record
        pg.mixer.music.fadeout(MUSICA_FADE_OUT)
        bd = GestorBD(RUTA)
        record_minimo = bd.comprobarRecord()
        if record_minimo == None and self.marcador.valor > 0:
            inputbox = InputBox(self.pantalla)
            nombre = inputbox.recoger_nombre()
            if nombre == "" or len(nombre) < 3:
                nombre = "---"
            bd.guardarRecords(nombre, self.marcador.valor)
        if record_minimo != None and record_minimo < self.marcador.valor:
            if self.marcador.valor > 0:
                inputbox = InputBox(self.pantalla)
                nombre = inputbox.recoger_nombre()
                if nombre == "" or len(nombre) < 3:
                    nombre = "---"
                bd.actualizarRecord(
                    nombre, self.marcador.valor, record_minimo)

    def mover_nave_planeta(self, aterrizar): # Girar nave y aparecer planete
        self.nave.update()
        if not aterrizar:
            self.pantalla.blit(self.nave.image, self.nave.rect)
        else:
            self.pantalla.blit(self.planeta.image, self.planeta.rect)
            self.planeta.mover_planeta(aterrizar)
            self.nave.aterrizar_nave(aterrizar, self.pantalla)

    def pintar_fin_nivel(self, texto): # Fin del nivel
        font_file = os.path.join("resources", "fonts",
                                 "light_sans_serif_7.ttf")
        self.tipografia = pg.font.Font(font_file, 50)
        mensaje = texto
        texto = self.tipografia.render(mensaje, True, COLOR_TEXTO2)
        ancho_texto = texto.get_width()
        pos_x = (ANCHO_P - ancho_texto)/2
        pos_y = texto.get_height()*3
        self.pantalla.blit(texto, (pos_x, pos_y))

    def pintar_nivel_2(self): # Pasar a nivel 2
        font_file = os.path.join("resources", "fonts",
                                 "light_sans_serif_7.ttf")
        self.tipografia = pg.font.Font(font_file, 50)
        mensaje = 'Pulsa "Q" para ir al nivel 2'
        texto = self.tipografia.render(mensaje, True, COLOR_TEXTO2)
        ancho_texto = texto.get_width()
        pos_x = (ANCHO_P - ancho_texto)/2
        pos_y = (ALTO_P - texto.get_height()) - MARGEN_INFERIOR_TEXTOS
        self.pantalla.blit(texto, (pos_x, pos_y))

    def pintar_fondo(self): # Fondo nivel
        self.fondo = pg.image.load(os.path.join(
            "resources", "images", "fondo_nivel.jpg"))
        self.pantalla.blit(self.fondo, (0, 0))

    def pintar_objetos_partida(self): # Actualizar objetos "meteoritos..."
        self.meteoritos.update()
        self.meteoritos.draw(self.pantalla)

        self.meteoritos_m.update()
        self.meteoritos_m.draw(self.pantalla)

        # Para dibujar y actualizar las explosiones
        self.explosiones.update()
        self.explosiones.draw(self.pantalla)


class PantallaJuego2(PantallaJuego): # Segundo nivel

    def __init__(self, pantalla: pg.Surface, marcador):
        super().__init__(pantalla, marcador)

        # creaci??n de los meteoritos de nivel 2
        self.meteoritos = pg.sprite.Group()
        self.crear_meteoritos(MIN_METEO_2, MAX_METEO_2, PUNTOS_2)

        self.meteoritos_m = pg.sprite.Group()
        self.crear_meteoritos_m(MIN_METEO_M_2, MAX_METEO_M_2, PUNTOS_M_2)

        # creaci??n del planeta
        imagen_planeta2 = pg.image.load(os.path.join("resources", "images",
                                                     "planeta2.png"))
        self.planeta = Planeta(imagen_planeta2)

    def bucle_principal(self):

        # Punto para empezar a contar los ticks del juego
        ticks_juego = pg.time.get_ticks()

        # Flags de salida del juego
        salir = False
        game_over = False

        # Flag de la fase de aterrizaje
        aterrizaje = False

        # Reproducci??n de la m??sica del juego (en bucle)
        pg.mixer.music.play(-1)

        while not salir:
            self.reloj.tick(FPS)

            # para medir el tiempo que transcurre durante la partida
            contador_juego = (pg.time.get_ticks() - ticks_juego)//1000

            # Condici??n para pygame si pulsamos la X de la ventana
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()

            # Para pintar el fondo del nivel
            self.pintar_fondo()

            # Para mover y pintar la nave y mover el planeta cuando la nave aterrice
            self.mover_nave_planeta(aterrizaje)

            # Para pintar los elementos de la partida
            self.pintar_objetos_partida()

            # Colisi??n de la nave con meteorito, aparece explosion (efecto y sonido) y
            # desaparece la nave. Tambi??n desactiva colisiones durante el aterrizaje
            self.comportamiento_meteoritos(aterrizaje,
                                           MIN_METEO_2, MAX_METEO_2, PUNTOS_2, MIN_METEO_M_2, MAX_METEO_M_2, PUNTOS_M_2)

            # Para pintar el marcador de puntos
            self.marcador.pintar_marcador(self.pantalla)

            # Condici??n que activa el flag de aterrizaje (Tiempo transcurrido)
            if contador_juego == 90:
                aterrizaje = True

            # Condiciones para realizar la finalizaci??n de nivel 2
            if self.nave.fin_rotacion:
                self.pintar_fin_nivel("??ENHORABUENA! HAS GANADO")

            if contador_juego == 105:
                self.lanzarRecord()
                salir = True

            # Actualizaci??n de todos los elementos que se est??n mostrando en la partida
            pg.display.flip()

            # Para cerrar el juego si se pierden todas las vidas
            if self.marcador.vidas == 0:
                self.pintar_fin_nivel("HAS PERDIDO :(")
                game_over = True
                self.lanzarRecord()
                salir = True

        return game_over


class PantallaRecords(Pantalla): # Pantalla records

    def __init__(self, pantalla: pg.Surface):
        super().__init__(pantalla)
        self.musica = pg.mixer.music.load(os.path.join(
            "resources", "sounds", "musica_records.mp3"))
        self.bd = GestorBD(RUTA)
        self.records = []
        font_file = os.path.join("resources", "fonts", "game_sans_serif_7.ttf")
        self.tipografia = pg.font.Font(font_file, 25)
        self.tipo_titulos = pg.font.Font(font_file, 30)
        self.tipo_reiniciar = pg.font.Font(font_file, 30)

        # Para almacenar los valores de NOMBRE y PUNTOS en listas independientes
        # para poder ser renderizados
        self.nombres_record = []
        self.nombres_render = []
        self.puntos_record = []
        self.puntos_render = []

    def bucle_principal(self):
        salir = False
        pg.mixer.music.play(-1)
        self.cargar_datos()

        # Renderizado de cada una de las listas de NOMBRE y PUNTOS
        for nombre in self.nombres_record:
            texto_renderizar = self.tipografia.render(str(nombre),
                                                      True, COLOR_TEXTO2)
            self.nombres_render.append(texto_renderizar)

        for punto in self.puntos_record:
            texto_renderizar2 = self.tipografia.render(str(punto),
                                                       True, COLOR_TEXTO)
            self.puntos_render.append(texto_renderizar2)

        # Bucle de funcionamiento del juego
        while not salir:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                if event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
                    pg.mixer.music.stop()
                    salir = True

            # Para pintar el fondo de estrellas de la pantalla
            self.pintar_fondo()

            # Para pintar los nombres y los records en la pantalla
            self.pintar_texto_reiniciar()
            try:
                self.pintar_records(self.nombres_render, self.puntos_render,
                                    texto_renderizar, texto_renderizar2)
            except UnboundLocalError:
                self.pintar_mensaje_error()

            # Recarga de todos los elementos presentes en la pantalla
            pg.display.flip()

    def cargar_datos(self): # Pintar elementos en listas
        self.records = self.bd.obtenerRecords()
        for record in self.records:
            record.pop('id')
            for value in record.values():
                if isinstance(value, str):
                    self.nombres_record.append(value)
                else:
                    self.puntos_record.append(value)

    def pintar_fondo(self): # Fondo records, mismo fondo que intro
        self.fondo = pg.image.load(os.path.join(
            "resources", "images", "fondo_intro.jpg"))
        self.pantalla.blit(self.fondo, (0, 0))

    def pintar_mensaje_error(self):
        mensaje_error = "NO HAY RECORDS REGISTRADOS"
        mensaje_error_render = self.tipo_titulos.render(
            mensaje_error, True, COLOR_TEXTO)
        pos_x_error = (ANCHO_P - mensaje_error_render.get_width())/2
        pos_y_error = (ALTO_P - mensaje_error_render.get_height())/3
        self.pantalla.blit(mensaje_error_render, (pos_x_error, pos_y_error))

    def pintar_texto_reiniciar(self):
        # para pintar el mensaje de volver a jugar
        texto_reiniciar = 'Pulsa "ESPACIO" para jugar de nuevo'
        reiniciar_render = self.tipo_reiniciar.render(
            texto_reiniciar, True, COLOR_TEXTO2)
        ancho_texto = reiniciar_render.get_width()
        pos_x_fin = (ANCHO_P - ancho_texto)/2
        pos_y_fin = ALTO_P - reiniciar_render.get_height() - MARGEN_INFERIOR_TEXTOS
        self.pantalla.blit(
            reiniciar_render, (pos_x_fin, pos_y_fin))

    def pintar_records(self, nombres, puntos, renderizado, renderizado2): # Ver datos records

        # para pintar los t??tulos de los records
        pos_x_titulo = 300
        pos_x_titulo2 = 560
        pos_y_titulo = 100
        titulo_nombre = "NOMBRE"
        titulo_puntos = "PUNTOS"

        nombres_jugador_render = self.tipo_titulos.render(
            titulo_nombre, True, COLOR_TEXTO2)
        self.pantalla.blit(nombres_jugador_render,
                           (pos_x_titulo, pos_y_titulo))

        puntos_jugador_render = self.tipo_titulos.render(
            titulo_puntos, True, COLOR_TEXTO)
        self.pantalla.blit(puntos_jugador_render,
                           (pos_x_titulo2, pos_y_titulo))

        # para pintar los datos de los records
        inicio_linea = 200
        separacion_x = 180

        for i in range(len(nombres)):
            pos_x = (ANCHO_P - renderizado.get_width())//3
            pos_y = i * renderizado.get_height() + inicio_linea
            self.pantalla.blit(nombres[i], (pos_x, pos_y))

        for j in range(len(puntos)):
            pos_x2 = (ANCHO_P - renderizado2.get_width() + separacion_x)//2
            pos_y2 = j * renderizado.get_height() + inicio_linea
            self.pantalla.blit(puntos[j], (pos_x2, pos_y2))