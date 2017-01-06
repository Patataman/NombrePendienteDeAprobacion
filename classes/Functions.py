# -*- coding: utf-8 -*-

import sys
from pygame import image, error, font
#from pygame.locals import *

# Funciones
# ---------------------------------------------------------------------
def load_image(filename):
    ''' Intenta abrir la imagen dada por la ruta "filename" '''
    #Intenta cargar la imagen
    try: 
        imageFile = image.load(filename)
    #Si falla, sale el error
    except error as message:
        raise sys.exc_info()
    return imageFile

''' Escribir texto '''
def texto(texto, posx, posy, size=25, color=(255, 255, 255)):
    fuente = font.Font("assets/fonts/Lato-Regular.ttf", size)
    salida = fuente.render(texto, 1, color)
    salida_rect = salida.get_rect()
    salida_rect.centerx = posx
    salida_rect.centery = posy
    return salida, salida_rect