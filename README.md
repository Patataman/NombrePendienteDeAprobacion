# NombrePendienteDeAprobacion

Proyecto de @guluc3m desarrollado por @patataman y @seind.

Este repositorio contiene un juego (muy modesto, todo sea dicho) de lucha en 2D.
El juego se encuentra totalmente desarrollado en Python, haciendo uso de la librería [Pygame] (http://pygame.org).

El juego se compone de las siguientes carpetas
- Raiz 
 - Assets
 - Classes

# Raiz
  Archivo *main.py* que es el que hay que ejecutar para abrir el juego.
# Assets
  Contiene archivos tales como imágenes, sonidos, sprites de personajes...
# Classes
  Contiene los .py que componen el juego.
  - *Functions.py*: Contiene funciones genéricas tales como cargar imágenes o crear un texto. 
  - *personajes.json*: Contiene el listado de personajes incluidos en el juego. Contiene: Nombre del personaje, ruta del avatar del personaje y ruta de la hoja de sprites.
  - *Director.py*: Junto con Scene.py permite realizar cambios de escenas en el juego.
  - *Scene.py*: Contiene todas las distintas escenas de las que se compone el juego (Inicio, Panel y Combate).
  - *Player.py*: Contiene la representación de los personajes, atributos y métodos.

#Sprites (WIP)
Los sprites de los personajes están divididos en 2 mitades, una para cada orientación posible. Dado que realizar sprites es un trabajo costoso y para simplificar se componen sólo de 4 imágenes cada acción posible. *Está pendiente definir la organización de las hojas para cada acción de los personajes*

#Personajes (WIP)
Para definir un personaje es necesario tener su hoja de sprites. Además para mostrarlo correctamente hay que definir un nombre de personaje y una imagen de avatar.

