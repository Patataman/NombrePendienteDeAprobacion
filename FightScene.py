#!/usr/bin/env python
# -*- coding: utf-8 -*-
 
# Módulos
import sys, pygame, math
from pygame.locals import *
from classes.Scene import SceneHome
from classes.Director import Director
from classes.Player import Player
from classes.Functions import *


 
# Constantes
WIDTH = 1024
HEIGHT = 768
	
    
# ---------------------------------------------------------------------
 
def main():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("FightSene")
    background_image, background_image_rect = load_image('assets/images/misc/fondo.jpg')
 	# Se inicializan los personajes y avatares
    player1 = Player("pepi")
    player2 = Player("pepo")
    avatar1Rect = player1.avatar.get_rect()
    avatar1Rect.centerx = 41
    avatar1Rect.centery = 40
    avatar2Rect = player2.avatar.get_rect()
    avatar2Rect.centerx = 983
    avatar2Rect.centery = 40
    
    clock = pygame.time.Clock()
    couldown = 60 # tiempo de combate
    time2 = 0

    # Barras de vida
    hudP1 = pygame.Rect(60, 40, 400, 10)
    hudP2 = pygame.Rect(564, 40, 400, 10)

    while True:
        time = clock.tick(1)
        keys = pygame.key.get_pressed()
        for eventos in pygame.event.get():
            if eventos.type == QUIT:
                sys.exit(0)
 

        #actualizar vida y tiempo
        if keys[K_a]:
            player1.getHurt(5)
        elif keys[K_d]:
            player1.getHurt(12)
        elif keys[K_j]:
            player2.getHurt(5)
        elif keys[K_l]:
            player2.getHurt(12)

        # Cambiar estado    
        elif keys[K_v]:
            player1.state = "idle"
        elif keys[K_b]:
            player1.state = "avanzar"    


        hudP1.width = player1.health*4
        hudP2.width = player2.health*4
        hudP2.left = 564+(400-player2.health*4)
        time2 += time

        # Pintamos
        #screen.fill((0,0,0))
	screen.blit(background_image, (0, 0))
        timeCD, time_rect = texto(str(couldown - int(math.floor(time2/1000))), 512, 45)


        screen.blit(timeCD, time_rect)
        pygame.draw.rect(screen,(255,255,255),hudP1)
        pygame.draw.rect(screen,(255,255,255),hudP2)
        screen.blit(player1.avatar, avatar1Rect)
        screen.blit(player2.avatar, avatar2Rect)
        # Actualizamos y pintamos personaje
        player1.update()
        screen.blit(player1.sprites[player1.state][player1.current_hframe], (200, 200)) 

        pygame.display.flip()
    return 0
 
if __name__ == '__main__':
    pygame.init()
    main()
