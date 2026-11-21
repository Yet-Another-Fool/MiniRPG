import pygame
import time
from config import W, H, FPS, MAP_GROUND_FILE_PATH, MAP_DECORS_FILE_PATH, MAP_OBJECTS_PATH, CAMERA_SPEED


class Game:
    pass


from .world import World
from .rendering import Rendering
#from .player import Player
#from .entity import EntityHandler


class Game:
    def __init__(self):
        self.playing = True

        self.w, self.h = W, H
        self.screen = pygame.display.set_mode((self.w, self.h))

        self.fps = FPS
        self.camera_speed = int(CAMERA_SPEED * (1000 / FPS))

        self.clock = pygame.time.Clock()
        self.delta = 0

        self.world = World(self, MAP_GROUND_FILE_PATH, MAP_DECORS_FILE_PATH, MAP_OBJECTS_PATH)
        self.rendering = Rendering(self)
        
        self.player_id = 'player 0'
        self.change_wait = 0

    def get_player(self):
        return self.world.entities[self.player_id]

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                return

        keys = pygame.key.get_pressed()

        if keys[pygame.K_ESCAPE]:
            self.playing = False
            return
        
        if keys[pygame.K_d]:
            #self.player.accelerate(dx=1)
            self.world.entities[self.player_id].accelerate(self.delta, dx=1)
        if keys[pygame.K_q]:
            #self.player.accelerate(dx=-1)
            self.world.entities[self.player_id].accelerate(self.delta, dx=-1)
        if keys[pygame.K_s]:
            #self.player.accelerate(dy=1)
            self.world.entities[self.player_id].accelerate(self.delta, dy=1)
        if keys[pygame.K_z]:
            #self.player.accelerate(dy=-1)
            self.world.entities[self.player_id].accelerate(self.delta, dy=-1)

        # if keys[pygame.K_RIGHT]:
        #     self.rendering.change_offset(dx=-self.camera_speed)
        # if keys[pygame.K_LEFT]:
        #     self.rendering.change_offset(dx=self.camera_speed)
        # if keys[pygame.K_DOWN]:
        #     self.rendering.change_offset(dy=-self.camera_speed)
        # if keys[pygame.K_UP]:
        #     self.rendering.change_offset(dy=self.camera_speed)
        # 
        # doesnt work anymore, because we center the camera each frame

        if keys[pygame.K_c] and self.change_wait >= 30:
            self.player_id = self.world.get_new_player_id(self.player_id)
            self.change_wait = 0
        # a bit stupid but with this we can control another entity :)

    def loop(self):
        while self.playing:
            # logique jeu
            
            # boucle évènements
            self.check_events()

            # calcul de la physique (mouvement hitbox, interaction decors...)
            self.world.compute_movements()
            self.world.entities[self.player_id].compute_animation()

            # affichage
            self.rendering.render()
            pygame.display.update()

            # délai
            self.delta = self.clock.tick(self.fps)
            self.camera_speed = int(CAMERA_SPEED * self.delta)
            #print(self.delta)
            #print(self.camera_speed)

            if self.change_wait < 30:
                self.change_wait += 1

# les TODO ont étés déplacés dans 'documentation/todo.md'.
