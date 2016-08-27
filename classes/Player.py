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
		self.sprites = self.load_sprites("assets/images/sprites/Sprite_" + name + "_ficha.png", 200, 420)
		self.avatar = load_image("assets/images/avatares/"+name+"_avatar.png", False)
		self.state = "idle"
		self.health = 100
		#Hacia donde mira (r -> derecha, l -> izquierda)
		self.orientacion = 'r'
		#Añadir variable vulnerable
		self.vulnerable = True


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

	def load_sprites(self, filename, width, height):
		"""Los sprites de los personajes se cargan desde una imagen donde están todos contenidos y
		después se genera una lista de listas ordenada con cada imagen de la animación"""

		# En una primera instancia vamos a definir que cada frame tiene 420 de alto y 200 de ancho

		ficha = {}

		sprite_ficha = load_image(filename)
		#Descomentar la siguiente linea para probar
		#sprite_ficha = load_image("assets/images/sprites/SpriteMatamePorfavor_ficha.png")
		framePorLinea = 6
		ficha["idle"] = []
		ficha["avanzar"] = []
		ficha["defender"] = []
		ficha["defenderSalto"] = []
		ficha["ataqueDebil"] = []
		ficha["ataqueFuerte"] = []
		ficha["saltar"] = []
		ficha["pegarSalto"] = []
		ficha["golpeBajo"] = []
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
			ficha["pegarSalto"].append(sprite_ficha.subsurface((i*200, height*7, width, height)))
			ficha["golpeBajo"].append(sprite_ficha.subsurface((i*200, height*8, width, height)))
			ficha["recibir"].append(sprite_ficha.subsurface((i*200, height*9, width, height)))
			ficha["Morir"].append(sprite_ficha.subsurface((i*200, height*10, width, height)))

		return ficha

