import os
import pygame as pg
import sqlite3

from . import ANCHO_P, ALTO_P, COLOR_CAJA_INPUT, COLOR_TEXTO_INPUT


class GestorBD: # Base de datos

    def __init__(self, ruta):
        self.ruta = ruta

    def obtenerRecords(self): # Consultar records BASE DE DATOS
        
        consulta = "SELECT * FROM records ORDER BY puntos DESC LIMIT 10"

        # 1- Conectar con la base de datos
        conexion = sqlite3.connect(self.ruta)

        # 2- Generar el cursor de la consulta
        cursor = conexion.cursor()

        # 3- Pasar la consulta a SQL y ejecutar
        cursor.execute(consulta)

        records = []
        nombres_columnas = []

        for desc_columna in cursor.description:
            nombres_columnas.append(desc_columna[0])

        datos = cursor.fetchall()
        for dato in datos:
            record = {}
            indice = 0
            for nombre in nombres_columnas:
                record[nombre] = dato[indice]
                indice += 1
            records.append(record)

        conexion.close()
        return records

    def comprobarRecord(self): # Comprobar valor minimo de records añadidos
        lista_records = []
        records = self.obtenerRecords()
        # Se eliminan las claves innecesarias para la comprobación
        for record in records:
            record.pop('id')
            record.pop('nombre')
            for value in record.values():
                lista_records.append(value)
        # Aquí se comprueba si el registro está vacío o está ya completo (TOP 10)
        if len(lista_records) == 0 or len(lista_records) < 10:
            pass
        # Aquí se extrae la puntuación mínima y se devuelve
        else:
            valor_minimo = min(lista_records)
            return valor_minimo

    def actualizarRecord(self, nombre, puntos, puntos_minimos): # Actualizar records si esta lleno
        consulta = "UPDATE records SET nombre = (?), puntos = (?)  WHERE puntos = (?)"
        conexion = sqlite3.connect(self.ruta)
        cursor = conexion.cursor()
        cursor.execute(consulta, (nombre, puntos, puntos_minimos))
        conexion.commit()
        conexion.close()

    def guardarRecords(self, nombre, puntos): # Guardar nuevo records
        consulta = "INSERT INTO records (nombre,puntos) VALUES (?,?)"
        conexion = sqlite3.connect(self.ruta)
        cursor = conexion.cursor()
        cursor.execute(consulta, (nombre, puntos))
        conexion.commit()
        conexion.close()


class InputBox:
    
    def __init__(self, pantalla: pg.Surface):
        font_file = os.path.join(
            "resources", "fonts", "game_sans_serif_7.ttf")
        self.tipografia = pg.font.Font(font_file, 20)
        self.texto = ""
        self.color_fondo = COLOR_CAJA_INPUT
        self.color_texto = COLOR_TEXTO_INPUT
        self.pantalla = pantalla
        self.espacio = 30
        self.pintar_elementos_fijos()

    def recoger_nombre(self):
        salir = False
        while not salir:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_BACKSPACE and len(self.texto) > 0:
                        self.texto = self.texto[:-1]
                    elif event.key == pg.K_RETURN:
                        salir = True
                    else:
                        self.texto += event.unicode
                if event.type == pg.KEYDOWN and len(self.texto) > 2:
                    self.texto = self.texto[:3]
            self.pintar()
            pg.display.flip()
        return self.texto.upper()

    def pintar(self):
        pg.draw.rect(self.pantalla, self.color_fondo, self.fondo)
        self.pantalla.blit(self.titulo, (self.x_titulo, self.y_titulo))

        superficie_texto = self.tipografia.render(
            self.texto, True, self.color_texto, self.color_fondo)
        pos_x = self.x_titulo
        pos_y = self.y_titulo + self.titulo.get_height()
        self.pantalla.blit(superficie_texto, (pos_x, pos_y))

    def pintar_elementos_fijos(self):

        self.titulo = self.tipografia.render(
            "GUAU NUEVO RECORD!!! INSERTA TUS INICIALES (3) - (PULSA 'INTRO' PARA TERMINAR)", True, self.color_texto, self.color_fondo)
        self.x_titulo = (ANCHO_P-self.titulo.get_width())//2
        self.y_titulo = (ALTO_P-self.titulo.get_height())//3

        x_fondo = self.x_titulo - self.espacio
        y_fondo = self.y_titulo - self.espacio
        w_fondo = self.titulo.get_width() + self.espacio * 3
        h_fondo = self.titulo.get_height() * 2 + self.espacio * 2
        self.fondo = pg.Rect(x_fondo, y_fondo, w_fondo, h_fondo)