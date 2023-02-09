# Juego The Quest creado por Cristobal Moya Lorente

- Programa hecho en python con el framework pygame, con motor de base de datos SQLite

## En su entorno de python ejecutar el comando

1º Iniciar el comando:
```
pip clone https://github.com/CristobalMoya7/Proyecto_Final_Pygame_Cristobal.git
```
2º Una vez clonado, ponemos el siguiente comando para crear el entorno
```
python -m venv env
```
3º Una vez creado el entorno debemos activarlo:
```
Windows: .\env\Scripts\activate
Mac/Linux: ./env/bin/activate
```
4º Debemos instalar los requirements, para ello ponemos:
```
pip install -r requirenments.txt
```
5º En caso de querer crear una base de datos propia podemos hacerlo creando una base de datos en SQLITE
con los datos añadidos en data/records_create.sql

6º Para iniciar el juego debemos tener el entorno activado, una vez con todo lo anterior realiazado,
vamos al archivo main e iniciamos el programa.

7º En caso de querer cambiar el numero de vidas simplemente cambialo desde el archivo __init__.py