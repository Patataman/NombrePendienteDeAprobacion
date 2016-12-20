# NombrePendienteDeAprobacion

Proyecto de @guluc3m desarrollado por @Patataman y @SeindElBardo.

Este repositorio contiene un juego (muy modesto, todo sea dicho) de lucha en 2D para dos jugadores.
El juego se encuentra totalmente desarrollado en Python, haciendo uso de la librería [Pygame] (http://pygame.org).

El juego se compone de 3 pantallas:
- Inicio
- Selección de personajes:
- Juego

# Controles
Los controles para cada jugador son:
- Moverse hacia la izquierda: A para el jugador 1, Flecha izquierda para el jugador 2.
- Moverse hacia la derecha: D para el jugador 1, Flecha derecha para el jugador 2.
- Moverse hacia abajo: S para el jugador 1, Flecha abajo para el jugador 2.
- Salta: W para el jugador 1, Flecha arriba para el jugador 2.
- Selección de personaje: Barra espaciadora para el jugador 1 y Enter para el jugador 2-

El juego se compone de las siguientes carpetas
- Raiz
 - Assets
 - Classes

# Raiz
  Archivo *main.py* es el que hay que ejecutar para abrir el juego.
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

