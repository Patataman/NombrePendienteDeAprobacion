# -*- coding: utf-8 -*-

# Módulos
import pygame, sys, random
from pygame.locals import *
# Constantes
MUSIC = 1
RES = 0%3
RESOLUTION = [(640,480), (800,600), (1024,768)]
WIDTH = RESOLUTION[RES][0]
HEIGHT = RESOLUTION[RES][1]


# Funciones
# ---------------------------------------------------------------------
def load_image(filename, transparent=False):
	''' Intenta abrir la imagen dada por la ruta "filename" '''
	try: image = pygame.image.load(filename)
	#Si falla, sale el error
	except pygame.error, message:
		raise SystemExit, message
	''' Convierte la imagen a una de tipo de pygame'''
	image = image.convert()
	''' Si la imagen tiene transparencia, toma como transparencia el pixel superior izquierdo'''
	if transparent:
		color = image.get_at((0,0))
		image.set_colorkey(color, RLEACCEL)
	return image

''' Escribir texto '''

def texto(texto, posx, posy, color=(255, 255, 255), size=25):
    fuente = pygame.font.Font("fonts/DroidSans.ttf", size)
    salida = pygame.font.Font.render(fuente, texto, 1, color)
    salida_rect = salida.get_rect()
    salida_rect.centerx = posx
    salida_rect.centery = posy
    return salida, salida_rect

# ---------------------------------------------------------------------

def main():
	dir = Director()
	scene = SceneHome(dir)
	dir.change_scene(scene)
	dir.loop()
 
if __name__ == '__main__':
	pygame.init()
	main()
