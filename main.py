# -*- coding: utf-8 -*-

# Módulos
from classes.Scene import SceneHome
from classes.Director import Director
import pygame
from pygame.locals import *
# ---------------------------------------------------------------------

def main():
	dir = Director()
	scene = SceneHome(dir)
	dir.change_scene(scene)
	dir.loop()
 
if __name__ == '__main__':
	pygame.init()
	main()
