# -*- coding: utf-8 -*-

from pygame import sprite
from .Functions import *

FRAMES = 12

class Player(sprite.Sprite):
    """Representa cada personaje del juego durante la partida.

    El objeto Player contiene todos los datos comunes a todos
    los personajes y que se inicializan según el personaje
    escogido, como la vida, la lista de animaciones o el banco
    de sonidos.

    Este objeto se debe inicializar después de terminar la
    selección de personajes con los datos del personaje escogido."""

    def __init__(self, jsonObject):
        sprite.Sprite.__init__(self)
        self.name = jsonObject['nombre']
        self.sprites = [self.load_sprites(jsonObject['sprites'], 200, 420),
                        self.load_sprites(jsonObject['spritesAlt'], 200, 420)]
        self.avatar = [load_image(jsonObject['avatar']),
                        load_image(jsonObject['avatarAlt'])]
        self.restart()

    def restart(self):
        #Reiniciar atributos del personaje
        self.state = "idle"
        self.health = 100
        # Hacia donde mira (0 -> derecha, 4 -> izquierda)
        self.current_hframe = 0 # Lo necesitaremos para hacer el ciclo de animación
        self.orientacion = 0
        self.x = 75         #X inicial
        self.y = 250        #Y inicial
        self.vulnerable = False
        self.golpeando = False
        # Tanto el salto como cualquier acción dura varias iteraciones, por lo que se debe de tener en cuenta
        # para mantener el flujo correctamente y evitar solapamiento.
        self.cdSalto = 0
        self.cdAction = 0
        self.ataque = 0
        # Atributos necesario para calcular colisiones entre sprites
        self.image = None 
        self.rect = None

    # Actions
    def avanzar(self, time):
        """El avance del personaje está definido por su orientación y límitado por su posición o estado.
        No podrá salirse de los límites del escenario.
        No podrá avanzar si está ejecutando otra acción que no sea salto.
        """
        espacio = 0.5
        #Cuando se salta, el desplazamiento es mayor
        if self.state == "saltar":
            espacio = 1
        if self.state != 'saltar':
            self.state = "avanzar"
        self.vulnerable = True
        if self.orientacion == 0: # Avanzamos hacia la derecha
            if self.x <= 850: # No estamos en los límites del escenario
                self.x += time*espacio
        else:
            if self.x >= 25: # No estamos en los límites del escenario
                self.x -= time*espacio

    def defender(self, time):
        """Durante la defensa el personaje será invulnerable a cualquier ataque 
        y además avanzará hacia atrás. No podrá salirse de los límites del escenario.
        No podrá avanzar si está ejecutando otra acción que no sea salto.       
        """
        
        espacio = 0.5
        #Cuando se salta, el desplazamiento es mayor
        if self.state == "saltar":
            espacio = 1
        if self.state != 'saltar':
            self.state = "defender"
        self.vulnerable = False
        if self.orientacion == 0: # Avanzamos hacia la derecha
            if self.x >= 25: # No estamos en los límites del escenario
                self.x -= time*espacio
        else:
            if self.x <= 850: # No estamos en los límites del escenario
                self.x += time*espacio

    def ataqueDebil(self, playerObjective):
        """El ataque débil se caracteriza por ser más flojo pero más rápido. Esto en nuestro juego se traduce
        en que el daño será menor pero la cd del golpe también.
        Durante el ataque no se podrá efectuar ninguna acción.
        """

        self.state = "ataqueDebil"
        self.vulnerable = True
        self.golpeando = True
        if self.ataque != 2:
            self.ataque += 1
            self.cdAction = 5
        else:
            self.ataque = 0
            self.cdAction = 10
            if sprite.collide_mask(self, playerObjective):
                playerObjective.getHurt(5)

    def ataqueFuerte(self, playerObjective):
        """El ataque fuerte se caracteriza por inflingir mayor daño pero requerir más tiempo de ejecución.
        Durante el ataque no se podrá efectuar ninguna acción.
        """

        self.state = "ataqueFuerte"
        self.vulnerable = True
        self.golpeando = True
        self.cdAction = 20
        if sprite.collide_mask(self, playerObjective):
            playerObjective.getHurt(12)

    def saltar(self):
        """El personaje podrá saltar, la altura del salto viene determinada por la altura de los personajes,
        todos los personajes deben poder saltar 1,3 veces su altura, de forma que sea posible superar al
        otro personaje y caer en el lado opuesto del escenario, obligando a cambiar la orientación de los
        sprites.
        Mientras se está en el aire las maniobras son reducidas, por lo que durante esta acción la función
        actualizar devuelve un entero que representa la duración del salto. Mientras este número sea positivo,
        el personaje estará en el aire, pudiendo sólo realizar las acciones "defenderSalto", "avanzarSalto"
        y "ataqueSalto".
        Cuando el valor devuelto sea 0, el personaje habrá vuelto al suelo y en la función principal se
        recalculará la orientación de ambos personajes ya que existe la posibilidad de que hayan cambiado
        su ubicación relativa en el escenario.
        Durante un salto la dirección de avanzar o retroceder (orientación) será la misma hasta que el
        personaje termine el salto.
        El movimiento vertical descrito utiliza la fórmula del MRU

        La variable time se utiliza para el movimiento. Igual que en avanzar y defender

        e = 1/2 * a * t² + Vo * t + Eo
        """

        self.state = "saltar"
        self.vulnerable = True
        self.cdSalto = 120 # Hay que apañar la formula de movimiento en salto


    def ataqueSalto(self):
        """Durante un salto, si el jugador pulsa alguno de los botones de ataque, el personaje pasará
        ejecutar un golpe aereo que durara hasta el final del salto, no podrá realizar ninguna otra
        acción durante el salto, sin embargo podrá modificar la posición horizontalmente desplazandose
        según la dirección pulsada
        """

        self.state = "ataqueSalto"
        self.vulnerable = True
        self.golpeando = True
        self.cdAction = self.cdSalto

    def ataqueBajo(self):
        """El golpe bajo no se diferencia en nada del golpe flojo"""

        self.state = "ataqueBajo"
        self.vulnerable = True
        self.golpeando = True
        self.cdAction = 5

    def getHurt(self, dmg):
        """Cuando un personaje recibe daño, este se resta de sus puntos de vida actuales. En caso de estos
        lleguen a 0 o menos, el personaje habrá sido debilitado, perdiendo el enfrentamiento.
        Cuando el personaje es debilitado, la función devuelve 0, en caso contrario, 1.
        """
        if self.vulnerable:     #Si el personaje es vulnerable recibe daño
            self.health -= dmg
        if self.health < 1:
            self.health = 0
            return 0    # El personaje ha sido debilitado
        else:
            return 1    # El personaje sigue vivo

    def update(self):
        ##### Se calculan los atributos necesarios para las colisiones. Da igual si es 0 o 1, ya que sólo varía el color
        self.image = self.sprites[0][self.state][self.current_hframe//4+self.orientacion]
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)
        #####

        # Actualizamos frames
        self.current_hframe += 1
        if self.current_hframe == FRAMES:
            self.current_hframe = 0

        # Actualizamos posición si estamos en un salto
        # e = 1/2 * a * t² + Vo * t + Eo
        if self.state == "saltar" and self.cdSalto > 0:
            if self.cdSalto > 60:
                self.y -= 1/2 * 1 * 1 + 0 * 1 + 50
            else:
                self.y += 1/2 * 1 * 1 + 0 * 1 + 50
            self.cdSalto -= 10
            if self.cdSalto <= 0:
                self.state = "idle"
        if self.cdSalto < 0:
            self.cdSalto = 0
        self.cdAction -= 2
        if self.cdAction < 0:
            self.cdAction = 0
        return self.cdSalto 

    def load_sprites(self, filename, width, height):
        """Los sprites de los personajes se cargan desde una imagen donde están todos contenidos y
        después se genera una lista de listas ordenada con cada imagen de la animación"""

        # En una primera instancia vamos a definir que cada frame tiene 420 de alto y 200 de ancho

        ficha = {}

        sprite_ficha = load_image(filename)
        #Descomentar la siguiente linea para probar
        #sprite_ficha = load_image("assets/images/sprites/Sprite_chachiWachi_ficha.png")
        framePorLinea = 8
        ficha["idle"] = []
        ficha["avanzar"] = []
        ficha["defender"] = []
        ficha["defenderSalto"] = []
        ficha["ataqueDebil"] = []
        ficha["ataqueFuerte"] = []
        ficha["saltar"] = []
        ficha["ataqueSalto"] = []
        ficha["ataqueBajo"] = []
        ficha["recibir"] = []
        ficha["Morir"] = []
        for i in range(framePorLinea):
            ficha["idle"].append(sprite_ficha.subsurface((i*200, height*0, width, height)))
            ficha["avanzar"].append(sprite_ficha.subsurface((i*200, height*1, width, height)))
            ficha["defender"].append(sprite_ficha.subsurface((i*200, height*2, width, height)))
            ficha["defenderSalto"].append(sprite_ficha.subsurface((i*200, height*3, width, height)))
            ficha["ataqueDebil"].append(sprite_ficha.subsurface((i*200, height*4, width, height)))
            ficha["ataqueFuerte"].append(sprite_ficha.subsurface((i*200, height*5, width, height)))
            ficha["saltar"].append(sprite_ficha.subsurface((i*200, height*6, width, height)))
            ficha["ataqueSalto"].append(sprite_ficha.subsurface((i*200, height*7, width, height)))
            ficha["ataqueBajo"].append(sprite_ficha.subsurface((i*200, height*8, width, height)))
            ficha["recibir"].append(sprite_ficha.subsurface((i*200, height*9, width, height)))
            ficha["Morir"].append(sprite_ficha.subsurface((i*200, height*10, width, height)))

        return ficha

