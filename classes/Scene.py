# -*- coding: utf-8 -*-

from Director import Director
from Functions import *
from Player import *
import pygame, sys, math, copy, time
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

        self.flecha = load_image("assets/images/misc/flecha.png")
        #self.flecha = pygame.transform.scale(self.flecha, (self.iniciar.get_width()/4*3,self.iniciar.get_height()/4*3+10))
        self.flecha_rect = self.flecha.get_rect()
        self.flecha_rect.centerx = WIDTH/2 - self.iniciar.get_width()/4*3 - 50
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

        import json

        pjs = json.load(open('classes/personajes.json'))

        #Lista de objetos personajes (siendo cada posición un tipo de personaje)
        #El panel se sitúa en el medio de la pantalla y
        # a los lados la vista previa del pj
        self.panel = []
        for pj in pjs:
            tmp_pj = Player(pj)
            self.panel.append(tmp_pj)
        
        self.charac1, self.charac2 = self.panel[0], self.panel[0]
        self.prev1, self.prev2 = copy.copy(self.panel[0]), copy.copy(self.panel[0])
        self.nomb1, self.nomb1_rect = texto(self.prev1.name, 150, 100, 35)
        self.nomb2, self.nomb2_rect = texto(self.prev2.name, WIDTH-150, 100, 35)
        self.prev1.orientacion = 0
        self.prev2.orientacion = 4
        self.prev1.x = 75
        self.prev2.x = 800
        self.marco1 = load_image("assets/images/misc/select1.png", True)
        self.marco2 = load_image("assets/images/misc/select2.png", True)
        self.marcoComun = load_image("assets/images/misc/select12.png", True)

        self.atras, self.atras_rect = texto('Back F1', 100, HEIGHT-100, 40)
        self.sig, self.sig_rect = texto('Figth! F2', WIDTH-100 , HEIGHT-100, 40)

        # +1 porque si hay 3 personajes significa que son 0 filas. Pero en realidad es 1
        self.max_filas = math.floor(len(self.panel)/4)+1

        #Carga la musica
        # loop = -1 -> Loop infinito
        self.background_music = pygame.mixer.Sound("assets/sounds/341362__sirkoto51__anime-encounter-loop-1.wav")
        self.background_music.play(-1)
        self.select_music = pygame.mixer.Sound("assets/sounds/173327__soundnimja__blip-2.wav")
        #Pone la música a funcionar

    def on_update(self, time):
        #O algo asi
        self.prev1.update()
        self.prev2.update()

    def on_event(self, time, event):
        #Al pulsar una tecla...
        keys = pygame.key.get_pressed()
        if pygame.KEYDOWN:
            #Se selecciona atrás
            if keys[K_F1]:
                scene = SceneHome(self.director)
                self.background_music.stop()
                self.director.change_scene(scene)
            #Se selecciona luchar
            if keys[K_F2]:
                scene = SceneFight(self.director, self.charac1, self.charac2)
                self.director.change_scene(scene)
                self.background_music.stop()
                pygame.mixer.Sound("assets/sounds/58773__syna-max__anime-shing.wav").play()
            #Se selecciona un luchador
            if keys[K_SPACE]:
                #Se guarda el pj seleccionado y se actualiza la vista previa
                self.charac1 = self.panel[self.select1]
                self.prev1 = copy.copy(self.panel[self.select1])
                self.prev1.orientacion = 0
                self.prev1.x = 75
                self.nomb1, self.nomb1_rect = texto(self.prev1.name, 150, 100, 35)
            if keys[K_RETURN]:
                #Se guarda el pj seleccionado y se actualiza la vista previa
                self.charac2 = self.panel[self.select2]
                self.prev2 = self.panel[self.select2]
                self.prev2.orientacion = 4
                self.prev2.x = 800
                self.nomb2, self.nomb2_rect = texto(self.prev2.name, WIDTH-150, 100, 35)
            if keys[K_w]:
                if self.select1/4 != 0:
                    self.select1 -= 4
                    self.charac1 = self.panel[self.select1]
                    self.select_music.play()
            if keys[K_UP]:
                if self.select2/4 != 0:
                    self.select2 -= 4
                    self.charac2 = self.panel[self.select2]
                    self.select_music.play()
            if keys[K_a]:
                if self.select1 % 4 != 0:
                    self.select1 -= 1
                    self.charac1 = self.panel[self.select1]
                    self.select_music.play()
            if keys[K_LEFT]:
                if self.select2 % 4 != 0:
                    self.select2 -= 1
                    self.charac2 = self.panel[self.select2]
                    self.select_music.play()
            if keys[K_s]:
                if self.select1/4+1 != self.max_filas and self.select1+4 < len(self.panel):
                    self.select1 += 4
                    self.charac1 = self.panel[self.select1]
                    self.select_music.play()
            if keys[K_DOWN]:
                if self.select2/4+1 != self.max_filas and self.select2+4 < len(self.panel):
                    self.select2 += 4
                    self.charac2 = self.panel[self.select2]
                    self.select_music.play()
            if keys[K_d]:
                if self.select1 % 4 != 3 and self.select1 != len(self.panel)-1:
                    self.select1 += 1
                    self.charac1 = self.panel[self.select1]
                    self.select_music.play()
            if keys[K_RIGHT]:
                if self.select2 % 4 != 3 and self.select2 != len(self.panel)-1:
                    self.select2 += 1
                    self.charac2 = self.panel[self.select2]
                    self.select_music.play()

    def on_draw(self, screen):
        screen.fill((0,0,0))
        screen.blit(self.atras, self.atras_rect)
        screen.blit(self.sig, self.sig_rect)
        screen.blit(self.nomb1, self.nomb1_rect)
        screen.blit(self.nomb2, self.nomb2_rect)
        self.dibujarPanel(screen)

        screen.blit(pygame.transform.scale(self.prev1.sprites[self.prev1.state] \
                                        [self.prev1.current_hframe+self.prev1.orientacion], \
                                        (self.prev1.sprites[self.prev1.state][self.prev1.current_hframe+self.prev1.orientacion].get_width()/4*3,self.prev1.sprites[self.prev1.state][self.prev1.current_hframe+self.prev1.orientacion].get_height()/4*3)), \
                                        (self.prev1.x, self.prev1.y))
        screen.blit(pygame.transform.scale(self.prev2.sprites[self.prev2.state] \
                                        [self.prev2.current_hframe+self.prev2.orientacion], \
                                        (self.prev2.sprites[self.prev2.state][self.prev2.current_hframe+self.prev2.orientacion].get_width()/4*3,self.prev2.sprites[self.prev2.state][self.prev2.current_hframe+self.prev2.orientacion].get_height()/4*3)), \
                                        (self.prev2.x, self.prev2.y))

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
            #Mismo personaje por los dos
            if self.charac1 == self.charac2 and self.charac1 == i:
                marco_rect = self.marcoComun.get_rect()
                marco_rect.centerx = WIDTH/3 + 110*column
                marco_rect.centery = HEIGHT/4 - 5 + 110*fila
                screen.blit(self.marcoComun, marco_rect)
            #Personaje de jugador 1
            elif self.charac1 == i:
                marco_rect1 = self.marco1.get_rect()
                marco_rect1.centerx = WIDTH/3 + 110*column
                marco_rect1.centery = HEIGHT/4 - 5 + 110*fila
                screen.blit(self.marco1, marco_rect1)
            #Personaje de jugador 2
            elif self.charac2 == i:
                marco_rect2 = self.marco2.get_rect()
                marco_rect2.centerx = WIDTH/3 + 110*column
                marco_rect2.centery = HEIGHT/4 - 5 + 110*fila
                screen.blit(self.marco2, marco_rect2)

            column += 1

class SceneFight(Scene):

    def __init__(self, director, player1, player2):
        screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("FightSene")
        # Se inicializan los personajes y avatares
        self.player1 = copy.copy(player1)
        self.player1.x = 75
        self.player2 = copy.copy(player2)
        self.player2.x = 800

        self.avatar1Rect = self.player1.avatar.get_rect()
        self.avatar1Rect.centerx = 53
        self.avatar1Rect.centery = 52

        self.avatar2Rect = self.player2.avatar.get_rect()
        self.avatar2Rect.centerx = 971
        self.avatar2Rect.centery = 52

        self.nomb1, self.nomb1_rect = texto(self.player1.name, 150, 20)
        self.nomb2, self.nomb2_rect = texto(self.player2.name, WIDTH-150, 20)
        self.nomb1_rect.centerx = self.nomb1.get_width() + self.player1.avatar.get_width()
        self.nomb2_rect.centerx = WIDTH - self.nomb2.get_width() - self.player2.avatar.get_width()
        
        self.countdown = 60 # tiempo de combate
        self.time2 = 0

        # Barras de vida
        self.hudP1 = pygame.Rect(99, 52, 400, 10)
        self.hudP2 = pygame.Rect(522, 52, 400, 10)

    def on_update(self, time):
        self.calcularOrientacion()
        self.hudP1.width = self.player1.health*4
        self.hudP2.width = self.player2.health*4
        self.hudP2.left = 522+(400-self.player2.health*4)
        self.time2 += time
        self.player1.update()
        self.player2.update()

    def on_event(self, time, event):
        keys = pygame.key.get_pressed()
        if pygame.KEYDOWN:
            if keys[K_2]:
                self.player1.getHurt(5)
            if keys[K_3]:
                self.player1.getHurt(12)
            if keys[K_j]:
                self.player2.getHurt(5)
            if keys[K_k]:
                self.player2.getHurt(12)
            if keys[K_d]:
                if self.player1.orientacion == 0:
                    self.player1.avanzar()
                else:
                    self.player1.defender()
            if keys[K_a]:
                if self.player1.orientacion == 4:
                    self.player1.avanzar()
                else:
                    self.player1.defender()
            if keys[K_LEFT]:
                if self.player2.orientacion == 4:
                    self.player2.avanzar()
                else:
                    self.player2.defender()
            if keys[K_RIGHT]:
                if self.player2.orientacion == 0:
                    self.player2.avanzar()
                else:
                    self.player2.defender()

            if keys[K_RIGHT]:
                self.player2.state = "avanzar"
            if (keys[K_j]==0 and keys[K_k]==0 and keys[K_d]==0 and keys[K_a]==0
                    and keys[K_s]==0 and self.player1.state != "jump"):
                self.player1.state = "idle"
            if (keys[K_LEFT]==0 and keys[K_RIGHT]==0 and keys[K_DOWN]==0 and keys[K_2]==0
                    and keys[K_3]==0 and self.player2.state != "jump"):
                self.player2.state = "idle"

    def on_draw(self, screen):
        screen.fill((0,0,0))
        timeCD, time_rect = texto(str(self.countdown - int(math.floor(self.time2/1000))), 512, 38)

        screen.blit(timeCD, time_rect)
        pygame.draw.rect(screen,(255,255,255),self.hudP1)
        pygame.draw.rect(screen,(255,255,255),self.hudP2)
        screen.blit(self.player1.avatar, self.avatar1Rect)
        screen.blit(pygame.transform.flip(self.player2.avatar, True, False), self.avatar2Rect)
        screen.blit(self.nomb1, self.nomb1_rect)
        screen.blit(self.nomb2, self.nomb2_rect)
        # Actualizamos y pintamos personaje
        #screen.blit(pygame.transform.flip(self.player1.sprites[self.player1.state][self.player1.current_hframe], False, False), (200, 200))
        #screen.blit(pygame.transform.flip(self.player2.sprites[self.player2.state][self.player2.current_hframe], True, False), (600, 200))
        screen.blit(pygame.transform.scale(self.player1.sprites[self.player1.state] \
            [self.player1.current_hframe+self.player1.orientacion], \
            (self.player1.sprites[self.player1.state][self.player1.current_hframe+self.player1.orientacion].get_width()/4*3,self.player1.sprites[self.player1.state][self.player1.current_hframe+self.player1.orientacion].get_height()/4*3)), \
            (self.player1.x, self.player1.y))
        screen.blit(pygame.transform.scale(self.player2.sprites[self.player2.state] \
            [self.player2.current_hframe+self.player2.orientacion], \
            (self.player2.sprites[self.player2.state][self.player2.current_hframe+self.player2.orientacion].get_width()/4*3,self.player2.sprites[self.player2.state][self.player2.current_hframe+self.player2.orientacion].get_height()/4*3)), \
            (self.player2.x, self.player2.y))

    def calcularOrientacion(self):
        if (self.player1.x < self.player2.x): # Están colocados naturalmente
            self.player1.orientacion = 0
            self.player2.orientacion = 4
        else:
            self.player1.orientacion = 4
            self.player2.orientacion = 0