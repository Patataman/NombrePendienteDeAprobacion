# -*- coding: utf-8 -*-

from Director import Director
from Functions import *
from Player import *
import pygame, sys, math, copy
from pygame.locals import *
#import Personajes

HEIGHT = 768
WIDTH = 1024

class Scene:
    """Representa un escena abstracta del videojuego.
 
    Una escena es una parte visible del juego, como una pantalla
    de presentación o menú de opciones. Tiene que crear un objeto
    derivado de esta clase para crear una escena utilizable."""
 
    def __init__(self, director):
        self.director = director
 
    def on_update(self):
        "Actualización lógica que se llama automáticamente desde el director."
        raise NotImplemented("Tiene que implementar el método on_update.")
 
    def on_event(self, event):
        "Se llama cuando llega un evento especifico al bucle."
        raise NotImplemented("Tiene que implementar el método on_event.")
 
    def on_draw(self, screen):
        "Se llama cuando se quiere dibujar la pantalla."
        raise NotImplemented("Tiene que implementar el método on_draw.")

class SceneHome(Scene):
    """Escena inicial del juego, esta es la primera que se carga cuando inicia"""

    def __init__(self, director):
        Scene.__init__(self, director)

        #Altura: Segundo cuarto
        self.iniciar, self.iniciar_rect = texto('Seleccion de personajes', WIDTH/2, HEIGHT/2, 40)
        self.titulo, self.titulo_rect = texto('Titulo o imagen o yuqse', WIDTH/2, HEIGHT/4, 75, (255,255,255))

        self.flecha = load_image("assets/images/flecha.png")
        #self.flecha = pygame.transform.scale(self.flecha, (self.iniciar.get_width()/2,self.iniciar.get_height()/2+10))
        self.flecha_rect = self.flecha.get_rect()
        self.flecha_rect.centerx = WIDTH/2 - self.iniciar.get_width()/2 - 50
        self.flecha_rect.centery = HEIGHT/2


        #Carga la musica
        #pygame.mixer.music.load("assets/music/title_theme.mp3")
        #Pone la música a funcionar
        # loop = -1 -> Loop infinito
        #pygame.mixer.music.play(-1)

    def on_update(self, time):
        pass

    def on_event(self, time, event):
        #Al pulsar una tecla...
        keys = pygame.key.get_pressed()
        if pygame.KEYDOWN:
            if keys[K_RETURN]:
                scene = ScenePanel(self.director)
                self.director.change_scene(scene)

    def on_draw(self, screen):
        screen.fill((0,0,0))
        screen.blit(self.titulo, self.titulo_rect)
        screen.blit(self.flecha, self.flecha_rect)
        screen.blit(self.iniciar, self.iniciar_rect)

class ScenePanel(Scene):
    """Escena de selección de personajes"""

    def __init__(self, director):
        Scene.__init__(self, director)
        pygame.display.set_caption("Selección de personaje")
        self.select1, self.select2 = 0,0

        nombres = open('classes/personajes','r').read().split('\n')

        #Lista de objetos personajes (siendo cada posición un tipo de personaje)
        self.panel = []
        for nomb in nombres:
            tmp_pj = Player(nomb)
            self.panel.append(tmp_pj)
        
        self.charac1, self.charac2, self.prev1, self.prev2 = self.panel[0],self.panel[0],None,None
        #El panel se sitúa en el medio de la pantalla y
        # a los lados la vista previa del pj

        self.atras, self.atras_rect = texto('Back F1', 100, HEIGHT-100, 40)
        self.sig, self.sig_rect = texto('Figth! F2', WIDTH-100 , HEIGHT-100, 40)

        #Carga la musica
        #pygame.mixer.music.load("assets/music/title_theme.mp3")
        #Pone la música a funcionar
        # loop = -1 -> Loop infinito
        #pygame.mixer.music.play(-1)

    def on_update(self, time):
        #O algo asi
        pass
        #self.prev1.idle()
        #self.prev2.idle()

    def on_event(self, time, event):
        #Al pulsar una tecla...
        keys = pygame.key.get_pressed()
        if pygame.KEYDOWN:
            #Se selecciona atrás
            if keys[K_F1]:
                scene = SceneHome(self.director)
                self.director.change_scene(scene)
            #Se selecciona luchar
            if keys[K_F2]:
                scene = SceneFight(self.director, self.charac1, self.charac2)
                self.director.change_scene(scene)
            if keys[K_RETURN] or keys[K_SPACE]:
                #Se selecciona un luchador
                if keys[K_RETURN]:
                    #Se guarda el pj seleccionado y se actualiza la vista previa
                    self.charac1 = self.panel[self.select1]
                    self.prev1 = self.panel[self.select1]
                if keys[K_SPACE]:
                    #Se guarda el pj seleccionado y se actualiza la vista previa
                    self.charac2 = self.panel[self.select2]
                    self.prev2 = self.panel[self.select2]
                if keys[K_w]:
                    if self.select1 != 0:
                        self.select1 -= 4
                        self.charac1 = self.panel[self.select1]
                        #self.prev1 = self.panel[self.select1].getIdle()
                if keys[K_UP]:
                    if self.select2 != 0:
                        self.select2 -= 4
                        self.charac2 = self.panel[self.select2]
                        #self.prev2 = self.panel[self.select2].getIdle()
                if keys[K_a]:
                    if self.select1 % 4 != 0:
                        self.select1 -= 1
                        self.charac1 = self.panel[self.select1]
                        #self.prev1 = self.panel[self.select1].getIdle()
                    if self.select % 4 == 0:
                        self.select1 += 3
                        self.charac1 = self.panel[self.select1]
                        #self.prev1 = self.panel[self.select1].getIdle()
                if keys[K_LEFT]:
                    if self.select2 % 4 != 0:
                        self.select2 -= 1
                        self.charac2 = self.panel[self.select2]
                        #self.prev2 = self.panel[self.select2].getIdle()
                    if self.select % 4 == 0:
                        self.select1 += 3
                        self.charac1 = self.panel[self.select1]
                        #self.prev1 = self.panel[self.select1].getIdle()
                if keys[K_s]:
                    if self.select1 != self.max_filas:
                        self.select1 += 4
                        self.charac1 = self.panel[self.select1]
                        #self.prev1 = self.panel[self.select1].getIdle()
                if keys[K_DOWN]:
                    if self.select2 != self.max_filas:
                        self.select2 += 4
                        self.charac2 = self.panel[self.select2]
                        #self.prev2 = self.panel[self.select2].getIdle()
                if keys[K_d]:
                    if self.select1 % 4 != 3:
                        self.select1 += 1
                        self.charac1 = self.panel[self.select1]
                        #self.prev1 = self.panel[self.select1].getIdle()
                    if self.select1 % 4 == 3:
                        self.select1 -= 3
                        self.charac1 = self.panel[self.select1]
                        #self.prev1 = self.panel[self.select1].getIdle()
                if keys[K_RIGHT]:
                    if self.select2 % 4 != 3:
                        self.select2 += 2
                        self.charac2 = self.panel[self.select2]
                        #self.prev2 = self.panel[self.select2].getIdle()
                    if self.select2 % 4 == 3:
                        self.select2 -= 3
                        self.charac2 = self.panel[self.select2]
                        #self.prev2 = self.panel[self.select2].getIdle()


    def on_draw(self, screen):
        screen.fill((0,0,0))
        screen.blit(self.atras, self.atras_rect)
        screen.blit(self.sig, self.sig_rect)
        self.dibujarPanel(screen)

    def dibujarPanel(self,screen):
        fila = 0
        column = 0
        for i in self.panel:
            if column == 4:
                column = 0
                fila += 1
            tmp_avatar_rect = i.avatar.get_rect()
            tmp_avatar_rect.centerx = WIDTH/3 + 110*column
            tmp_avatar_rect.centery = HEIGHT/4 + 110*fila
            screen.blit(i.avatar, tmp_avatar_rect)
            column += 1

class SceneFight(Scene):

    def __init__(self, director, player1, player2):
        screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("FightSene")
        # Se inicializan los personajes y avatares
        self.player2 = copy.copy(player2)
        self.player1 = copy.copy(player1)

        self.avatar1Rect = self.player1.avatar.get_rect()
        self.avatar1Rect.centerx = 41
        self.avatar1Rect.centery = 40

        self.avatar2Rect = self.player2.avatar.get_rect()
        self.avatar2Rect.centerx = 983
        self.avatar2Rect.centery = 40
        
        self.countdown = 60 # tiempo de combate
        self.time2 = 0

        # Barras de vida
        self.hudP1 = pygame.Rect(60, 40, 400, 10)
        self.hudP2 = pygame.Rect(564, 40, 400, 10)

    def on_update(self, time):
        self.hudP1.width = self.player1.health*4
        self.hudP2.width = self.player2.health*4
        self.hudP2.left = 564+(400-self.player2.health*4)
        self.time2 += time

    def on_event(self, time, event):
        keys = pygame.key.get_pressed()
        if pygame.KEYDOWN:
            if keys[K_a]:
                self.player1.getHurt(5)
            elif keys[K_d]:
                self.player1.getHurt(12)
            elif keys[K_j]:
                self.player2.getHurt(5)
            elif keys[K_l]:
                self.player2.getHurt(12)

    def on_draw(self, screen):
        screen.fill((0,0,0))
        timeCD, time_rect = texto(str(self.countdown - int(math.floor(self.time2/1000))), 512, 45)

        screen.blit(timeCD, time_rect)
        pygame.draw.rect(screen,(255,255,255),self.hudP1)
        pygame.draw.rect(screen,(255,255,255),self.hudP2)
        screen.blit(self.player1.avatar, self.avatar1Rect)
        screen.blit(self.player2.avatar, self.avatar2Rect)
