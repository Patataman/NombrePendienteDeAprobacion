# -*- coding: utf-8 -*-

import sys, os
from pygame import image, error, font
#from pygame.locals import *

# Funciones
# ---------------------------------------------------------------------
def load_image(filename):
    ''' Intenta abrir la imagen dada por la ruta "filename" '''
    #Intenta cargar la imagen
    try: 
        imageFile = image.load(resource_path(filename))
    #Si falla, sale el error
    except error:
        raise ImportError
    return imageFile

''' Escribir texto '''
def texto(texto, posx, posy, size=25, color=(255, 255, 255)):
    fuente = font.Font(resource_path("assets/fonts/Lato-Regular.ttf"), size)
    salida = fuente.render(texto, 1, color)
    salida_rect = salida.get_rect()
    salida_rect.centerx = posx
    salida_rect.centery = posy
    return salida, salida_rect

def resource_path(relative):
    return os.path.join(
        os.environ.get(
            "LD_LIBRARY_PATH",
            os.path.abspath(".")
        ),
        relative)

def debugGamepad():
    # For each joystick:
    for i in range(pygame.joystick.get_count()):
        joystick = pygame.joystick.Joystick(i)
        joystick.init()
    
        print("Joystick {}".format(i))
    
        # Get the name from the OS for the controller/joystick
        name = joystick.get_name()
        print("Joystick name: {}".format(name))
        
        # Usually axis run in pairs, up/down for one, and left/right for
        # the other.
        axes = joystick.get_numaxes()
        print("Number of axes: {}".format(axes))
        
        for i in range( axes ):
            axis = joystick.get_axis( i )
            print("Axis {} value: {:>6.3f}".format(i, axis))
            
        buttons = joystick.get_numbuttons()
        print("Number of buttons: {}".format(buttons))

        for i in range( buttons ):
            button = joystick.get_button( i )
            print("Button {:>2} value: {}".format(i,button))
            
        # Hat switch. All or nothing for direction, not like joysticks.
        # Value comes back in an array.
        hats = joystick.get_numhats()
        print("Number of hats: {}".format(hats))

        for i in range( hats ):
            hat = joystick.get_hat( i )
            print("Hat {} value: {}".format(i, str(hat)))