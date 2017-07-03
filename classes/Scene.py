# -*- coding: utf-8 -*-

import pygame, sys, math, copy, time
from .Director import Director
from .Functions import *
from .Player import *
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
 
    def on_update(self, time):
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
        self.iniciar, self.iniciar_rect = texto('Character selection', WIDTH/2, HEIGHT/2, 40)
        self.titulo, self.titulo_rect = texto('Title', WIDTH/2, HEIGHT/4, 75, (255,255,255))

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
        screen.fill((0, 0, 0))
        screen.blit(self.titulo, self.titulo_rect)
        screen.blit(self.flecha, self.flecha_rect)
        screen.blit(self.iniciar, self.iniciar_rect)


class ScenePanel(Scene):
    """Escena de selección de personajes"""

    def __init__(self, director):
        Scene.__init__(self, director)
        pygame.display.set_caption("Character selection")
        self.select1, self.select2 = 0, 0

        import json

        pjs = json.load(open('classes/characters.json'))

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
        self.marco1 = load_image("assets/images/misc/select1.png")
        self.marco2 = load_image("assets/images/misc/select2.png")
        self.marcoComun = load_image("assets/images/misc/select12.png")

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
                scene = SceneFight(self.director, self.prev1, self.prev2)
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
        screen.fill((0, 0, 0))
        screen.blit(self.atras, self.atras_rect)
        screen.blit(self.sig, self.sig_rect)
        screen.blit(self.nomb1, self.nomb1_rect)
        screen.blit(self.nomb2, self.nomb2_rect)
        self.dibujarPanel(screen)

        screen.blit(pygame.transform.scale(self.prev1.sprites[0][self.prev1.state] \
                                        [self.prev1.current_hframe//4+self.prev1.orientacion],
                                        (int(self.prev1.sprites[0][self.prev1.state][self.prev1.current_hframe//4+self.prev1.orientacion].get_width()/4*3),int(self.prev1.sprites[0][self.prev1.state][self.prev1.current_hframe//4+self.prev1.orientacion].get_height()/4*3))),
                                        (self.prev1.x, self.prev1.y))
        if self.prev1.name == self.prev2.name:
            screen.blit(pygame.transform.scale(self.prev2.sprites[1][self.prev2.state] \
                                        [self.prev2.current_hframe//4+self.prev2.orientacion],
                                        (int(self.prev2.sprites[1][self.prev2.state][self.prev2.current_hframe//4+self.prev2.orientacion].get_width()/4*3),int(self.prev2.sprites[1][self.prev2.state][self.prev2.current_hframe//4+self.prev2.orientacion].get_height()/4*3))),
                                        (self.prev2.x, self.prev2.y))
        else:
            screen.blit(pygame.transform.scale(self.prev2.sprites[0][self.prev2.state] \
                                        [self.prev2.current_hframe//4+self.prev2.orientacion],
                                        (int(self.prev2.sprites[0][self.prev2.state][self.prev2.current_hframe//4+self.prev2.orientacion].get_width()/4*3),int(self.prev2.sprites[0][self.prev2.state][self.prev2.current_hframe//4+self.prev2.orientacion].get_height()/4*3))),
                                        (self.prev2.x, self.prev2.y))

    def dibujarPanel(self,screen):
        fila = 0
        column = 0
        for i in self.panel:
            if column == 4:
                column = 0
                fila += 1
            tmp_avatar_rect = i.avatar[0].get_rect()
            tmp_avatar_rect.centerx = WIDTH/3 + 110*column
            tmp_avatar_rect.centery = HEIGHT/4 + 110*fila
            screen.blit(i.avatar[0], tmp_avatar_rect)
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

        self.director = director

        #Carga de fondo e imagenes varias
        self.backgroundPause = load_image('assets/images/misc/fondoSemiNegro.png')
        self.backgroundPause_rect = self.backgroundPause.get_rect()

        self.background = load_image('assets/images/misc/fondo.jpg')
        self.background_rect = self.background.get_rect()

        #Texto del menú de pausa
        self.pause, self.pause_rect = texto('PAUSA', WIDTH/2, HEIGHT/4, 80)
        self.selectPj, self.selectPj_rect = texto('Back to Character selection (F1)', WIDTH/2, HEIGHT/2, 40)
        self.reanudar, self.reanudar_rect = texto('Resume (ESC)', WIDTH/2, HEIGHT/2+100, 40)

        #Texto del menú de fin de partida
        self.end1, self.end1_rect = texto('Player 1 wins!', WIDTH/2, HEIGHT/4, 80)
        self.end2, self.end2_rect = texto('Player 2 wins!', WIDTH/2, HEIGHT/4, 80)
        self.rematch, self.rematch_rect = texto('Revenge! (F2)', WIDTH/2, HEIGHT/2+100,40)

        # Se inicializan los personajes y avatares
        self.player1 = copy.copy(player1)
        self.player1.x = 75
        self.player2 = copy.copy(player2)
        self.player2.x = 800

        self.avatar1Rect = self.player1.avatar[0].get_rect()
        self.avatar1Rect.centerx = 53
        self.avatar1Rect.centery = 52

        self.avatar2Rect = self.player2.avatar[0].get_rect()
        self.avatar2Rect.centerx = 971
        self.avatar2Rect.centery = 52

        self.nomb1, self.nomb1_rect = texto(self.player1.name, 150, 20)
        self.nomb2, self.nomb2_rect = texto(self.player2.name, WIDTH-150, 20)
        self.nomb1_rect.centerx = self.nomb1.get_width() + self.player1.avatar[0].get_width()
        self.nomb2_rect.centerx = WIDTH - self.nomb2.get_width() - self.player2.avatar[0].get_width()
        
        self.countdown = 93 # tiempo de combate
        self.time2 = 0

        # Barras de vida
        self.hudP1 = pygame.Rect(99, 52, 400, 10)
        self.hudP2 = pygame.Rect(522, 52, 400, 10)

        # Variable control para menus y cosas de esas (0 false, 1 true)
        self.inMenu = 1

    def on_update(self, time):
        if self.inMenu == 0 or self.inMenu == 1:
            self.calcularOrientacion()
            
            self.hudP1.width = self.player1.health*4
            self.hudP2.width = self.player2.health*4
            self.hudP2.left = 522+(400-self.player2.health*4)
            self.time2 += time
            self.player1.update()
            self.player2.update()
            # Idle
            keys = pygame.key.get_pressed()
            if not (keys[K_a] or keys[K_d] or self.player1.cdAction or self.player1.cdSalto):
                self.player1.state = "idle"
            if not (keys[K_LEFT] or keys[K_RIGHT] or self.player2.cdAction or self.player2.cdSalto):
                self.player2.state = "idle"
            if self.player1.health == 0 or self.player2.health == 0 or int(math.floor(self.time2/1000)) == self.countdown:
                self.inMenu = 3

    def on_event(self, time, event):
        keys = pygame.key.get_pressed()
        #if pygame.KEYDOWN:
        #Si se está pausado
        if self.inMenu != 2 and self.inMenu != 3:
            # Se selecciona escape para el menú
            if keys[K_ESCAPE] and self.inMenu == 0:
                self.inMenu = 2

            # Controles Player1
            ## Ir derecha
            if keys[K_d] and (not self.player1.cdAction):
                if self.player1.orientacion == 0:
                    if not pygame.sprite.collide_mask(self.player1, self.player2):
                        self.player1.avanzar(time)
                    else:
                        self.player1.avanzar(0)
                else:
                    self.player1.defender(time)
            ## Ir Izquierda
            if keys[K_a] and (not self.player1.cdAction):
                if self.player1.orientacion == 4:
                    if not pygame.sprite.collide_mask(self.player1, self.player2):
                        self.player1.avanzar(time)
                    else:
                        self.player1.avanzar(0)
                else:
                    self.player1.defender(time)
            ## Saltar                
            if keys[K_w] and (not self.player1.cdAction and not self.player1.cdSalto):
                self.player1.saltar()

            if keys[K_w] and keys[K_d]:
                if self.player1.orientacion == 0:
                    self.player1.avanzar(time)
                else:
                    self.player1.defender(time)

            if keys[K_w] and keys[K_a]:
                if self.player1.orientacion == 4:
                    self.player1.avanzar(time)
                else:
                    self.player1.defender(time)

            if self.inMenu == 0:
                ## AtaqueDebil
                if keys[K_j] and not self.player1.cdAction:
                    if self.player1.cdSalto:
                        a=1
                        #self.player1.ataqueSalto()
                    elif not self.player1.cdSalto and keys[K_s]:
                        self.player1.ataqueBajo()
                    else:    
                        self.player1.ataqueDebil(self.player2)
                ## AtaqueFuerte
                if keys[K_k] and not self.player1.cdAction:
                    if self.player1.cdSalto:
                        a=1
                        #self.player1.ataqueSalto()
                    elif not self.player1.cdSalto and keys[K_s]:
                        self.player1.ataqueBajo()
                    else:
                        self.player1.ataqueFuerte(self.player2)                            

            # Controles Player2
            ## Ir derecha
            if keys[K_RIGHT] and (not self.player2.cdAction):
                if self.player2.orientacion == 0:
                    if not pygame.sprite.collide_mask(self.player2, self.player1):
                        self.player2.avanzar(time)
                    else:
                        self.player2.avanzar(0)
                else:
                    self.player2.defender(time)
            ## Ir Izquierda        
            if keys[K_LEFT] and (not self.player2.cdAction):
                if self.player2.orientacion == 4:
                    if not pygame.sprite.collide_mask(self.player2, self.player1):
                        self.player2.avanzar(time)
                    else:
                        self.player2.avanzar(0)
                else:
                    self.player2.defender(time)
            ## Saltar
            if keys[K_UP] and (not self.player2.cdAction and not self.player2.cdSalto):
                self.player2.saltar()

            if keys[K_LEFT] and keys[K_UP]:
                if self.player2.orientacion == 4:
                    self.player2.avanzar(time)
                else:
                    self.player2.defender(time)

            if keys[K_RIGHT] and keys[K_UP]:
                if self.player2.orientacion == 0:
                    self.player2.avanzar(time)
                else:
                    self.player2.defender(time)

            if self.inMenu == 0:
                ## AtaqueDebil
                if keys[K_KP8] and not self.player2.cdAction:
                    if self.player2.cdSalto:
                        a=1
                        #self.player2.ataqueSalto()
                    elif not self.player2.cdSalto and keys[K_DOWN]:
                        self.player2.ataqueBajo()
                    else:    
                        self.player2.ataqueDebil(self.player1)
                ## AtaqueFuerte    
                if keys[K_KP9] and not self.player2.cdAction:
                    if self.player2.cdSalto:
                        a=1
                        #self.player2.ataqueSalto()
                    elif not self.player2.cdSalto and keys[K_DOWN]:
                        self.player2.ataqueBajo()
                    else:
                        self.player2.ataqueFuerte(self.player1)

        #Se está en el menú de pausa
        elif self.inMenu == 2:
            # Se selecciona escape para volver al juego
            if keys[K_ESCAPE]:
                self.inMenu = 0
            if keys[K_F1]:
                scene = ScenePanel(self.director)
                self.director.change_scene(scene)
        #Se acaba el combate
        elif self.inMenu == 3:
            #Se selecciona volver a selección pjs
            if keys[K_F1]:
                scene = ScenePanel(self.director)
                self.director.change_scene(scene)
            #Se selecciona revancha
            if keys[K_F2]:
                self.player1.restart()
                self.player2.restart()
                scene = SceneFight(self.director, self.player1, self.player2)
                self.director.change_scene(scene)

    def on_draw(self, screen):
        screen.fill((0,0,0))
        screen.blit(self.background, self.background_rect)
        timeCD, time_rect = texto(str(self.countdown - int(math.floor(self.time2/1000))), 512, 38)

        #Actualización del tiempo y barras de vida
        screen.blit(timeCD, time_rect)
        pygame.draw.rect(screen,(255,255,255),self.hudP1)
        pygame.draw.rect(screen,(255,255,255),self.hudP2)
        screen.blit(self.player1.avatar[0], self.avatar1Rect)
        if self.player1.name == self.player2.name:
            screen.blit(pygame.transform.flip(self.player2.avatar[1], True, False), self.avatar2Rect)
        else:
            screen.blit(pygame.transform.flip(self.player2.avatar[0], True, False), self.avatar2Rect)
        screen.blit(self.nomb1, self.nomb1_rect)
        screen.blit(self.nomb2, self.nomb2_rect)

        # Actualizamos y pintamos personaje
        screen.blit(pygame.transform.scale(self.player1.sprites[0][self.player1.state] \
                                            [self.player1.current_hframe//4+self.player1.orientacion],
                                            (int(self.player1.sprites[0][self.player1.state][self.player1.current_hframe//4+self.player1.orientacion].get_width()/4*3),int(self.player1.sprites[0][self.player1.state][self.player1.current_hframe//4+self.player1.orientacion].get_height()/4*3))),
                                            (self.player1.x, self.player1.y))
        if self.player1.name == self.player2.name:
            screen.blit(pygame.transform.scale(self.player2.sprites[1][self.player2.state] \
                                        [self.player2.current_hframe//4+self.player2.orientacion],
                                        (int(self.player2.sprites[1][self.player2.state][self.player2.current_hframe//4+self.player2.orientacion].get_width()/4*3),int(self.player2.sprites[1][self.player2.state][self.player2.current_hframe//4+self.player2.orientacion].get_height()/4*3))),
                                        (self.player2.x, self.player2.y))
        else:
            screen.blit(pygame.transform.scale(self.player2.sprites[0][self.player2.state] \
                                        [self.player2.current_hframe//4+self.player2.orientacion],
                                        (int(self.player2.sprites[0][self.player2.state][self.player2.current_hframe//4+self.player2.orientacion].get_width()/4*3),int(self.player2.sprites[0][self.player2.state][self.player2.current_hframe//4+self.player2.orientacion].get_height()/4*3))),
                                        (self.player2.x, self.player2.y))
        #Menus
        if self.inMenu == 1:
            self.cuentaAtras(screen)
        if self.inMenu == 2:
            self.menuPausa(screen)
        if self.inMenu == 3:
            self.menuPausaFin(screen)

    def calcularOrientacion(self):
        if (self.player1.x < self.player2.x): # Están colocados naturalmente
            self.player1.orientacion = 0
            self.player2.orientacion = 4
        else:
            self.player1.orientacion = 4
            self.player2.orientacion = 0

    def cuentaAtras(self, screen):
        countdownList = ["3","2","1","FIGHT!"]
        if self.time2/1000 < 4:
            countdown, countdown_rect = texto(countdownList[int(self.time2/1000)], WIDTH/2, HEIGHT/2, 75)
            screen.blit(countdown, countdown_rect)
        else:
            self.inMenu = 0

    def menuPausa(self, screen):
        screen.blit(pygame.transform.scale(self.backgroundPause,(WIDTH, HEIGHT)), self.backgroundPause_rect)
        screen.blit(self.pause, self.pause_rect)
        screen.blit(self.selectPj, self.selectPj_rect)
        screen.blit(self.reanudar, self.reanudar_rect)

    def menuPausaFin(self, screen):
        screen.blit(pygame.transform.scale(self.backgroundPause,(WIDTH, HEIGHT)), self.backgroundPause_rect)
        if self.player1.health == 0 or self.player2.health > self.player1.health:
            screen.blit(self.end2, self.end2_rect)
        if self.player2.health == 0 or self.player1.health > self.player2.health:
            screen.blit(self.end1, self.end1_rect)
        if self.player2.health == self.player1.health:
            text, text_rect = texto("IT'S A DRAW!", WIDTH/2, HEIGHT/4, 80)
            screen.blit(text, text_rect)
        screen.blit(self.selectPj, self.selectPj_rect)
        screen.blit(self.rematch, self.rematch_rect)
