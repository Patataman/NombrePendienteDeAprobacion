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
		self.sprites = load_sprites("assets/images/sprites/" + name + "_ficha.png", 200, 420)
		self.avatar = load_image("assets/images/avatares/"+name+"_avatar.png", False)
		self.state = "idle"
		self.health = 100
		#Hay que añadir estado orientacion
		#Añadir variable vulnerable


		self.current_hframe = 0 # Lo necesitaremos para hacer el ciclo de animación

	def getHurt(self, dmg):
		self.health -= dmg
		if self.health < 1:
			self.health = 0
			return 0	# El personaje ha sido debilitado
		else:
			return 1	# El personaje sigue vivo

	def update(self):
		self.current_hframe += 1
		if self.current_hframe == 3:
			self.current_hframe = 0
