# -*- coding: utf-8 -*-

import pygame
from pygame.locals import *
from Functions import *

class Player:
	"""Representa cada personaje del juego durante la partida.

	El objeto Player contiene todos los datos comunes a todos
	los personajes y que se inicializan según el personaje
	escogido, como la vida, la lista de animaciones o el banco
	de sonidos.

	Este objeto se debe inicializar después de terminar la
	selección de personajes con los datos del personaje escogido."""

	def __init__(self, name):
		self.name = name
		self.sprites = load_image("assets/images/sprites/" + name + "_ficha.png", True)
		self.avatar = load_image("assets/images/avatares/"+name+"_avatar.png", False)
		self.state = 0
		self.health = 100

	def getHurt(self, dmg):
		self.health -= dmg
		if self.health < 1:
			self.health = 0
			return 0	# El personaje ha sido debilitado
		else:
			return 1	# El personaje sigue vivo

	#muchas funciones...	