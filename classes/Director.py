# -*- coding: utf-8 -*-

import pygame
from pygame.locals import *
import os
from .Functions import load_image

class Director:
	"""Representa el objeto principal del juego.

	El objeto Director mantiene en funcionamiento el juego, se
	encarga de actualizar, dibuja y propagar eventos.

	Tiene que utilizar este objeto en conjunto con objetos
	derivados de Scene."""

	def __init__(self):
		self.screen = pygame.display.set_mode([1024,768], pygame.RESIZABLE)
		#Poner el iconito a la ventana
		pygame.display.set_icon(load_image("assets"+os.sep+"images"+os.sep+"misc"+os.sep+"icon32.png"))
		pygame.display.set_caption("NombrePendienteDeAprobacion")
		self.scene = None
		self.quit_flag = False
		self.clock = pygame.time.Clock()
		pygame.joystick.init()

	def loop(self):
		"Pone en funcionamiento el juego."

		'''Establece el número de teclas que cuenta por segundo.
			pygame.key.set_repeat(10,200)
		   Introduce un delay de 10ms para reconocer la tecla
		   y la siguiente la reconoce a las 200ms'''
		pygame.key.set_repeat(10, 200)
		while not self.quit_flag:
			time = self.clock.tick(24)

			# Eventos de Salida
			events = pygame.event.get()
			for event in events:
				if event.type == pygame.QUIT:
					self.quit()

				# detecta eventos
				self.scene.on_event(time, event)
			# actualiza la escena
			self.scene.on_update(time)

			# dibuja la pantalla
			self.scene.on_draw(self.screen)
			pygame.display.flip()

	def change_scene(self, scene):
		"Altera la escena actual."
		self.scene = scene

	def quit(self):
		pygame.joystick.quit()
		self.quit_flag = True
