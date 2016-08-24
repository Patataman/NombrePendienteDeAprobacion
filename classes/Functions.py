# -*- coding: utf-8 -*-

import pygame, sys
from pygame.locals import *

# Funciones
# ---------------------------------------------------------------------
def load_image(filename, transparent=False):
	''' Intenta abrir la imagen dada por la ruta "filename" '''
	try: image = pygame.image.load(filename)
	#Si falla, sale el error
	except pygame.error, message:
		raise SystemExit, message
	''' Convierte la imagen a una de tipo de pygame'''
	''' Si la imagen tiene transparencia, toma como transparencia el pixel superior izquierdo'''
	if transparent:
		image = image.convert_alpha()
		#color = image.get_at((0,0))
		#image.set_colorkey(color, RLEACCEL)
	else:
		image = image.convert()
	return image

''' Escribir texto '''

def load_sprites(filename, width, height):
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


def texto(texto, posx, posy, size=25, color=(255, 255, 255)):
    fuente = pygame.font.Font("assets/fonts/Lato-Regular.ttf", size)
    salida = fuente.render(texto, 1, color)
    salida_rect = salida.get_rect()
    salida_rect.centerx = posx
    salida_rect.centery = posy
    return salida, salida_rect