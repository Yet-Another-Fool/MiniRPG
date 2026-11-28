import pygame
from config import W, H, FPS, EXPECTED_DELTA, MAP_GROUND_FILE_PATH, MAP_DECORS_FILE_PATH, MAP_OBJECTS_PATH


class Game:
    pass


from .world import World
from .rendering import Rendering


class Game:
    def __init__(self):
        self.playing = True

        self.w, self.h = W, H
        self.screen = pygame.display.set_mode((self.w, self.h))

        self.fps = FPS

        self.clock = pygame.time.Clock()
        self.delta = 0
        self.expected_delta = EXPECTED_DELTA

        self.world = World(self, MAP_GROUND_FILE_PATH, MAP_DECORS_FILE_PATH, MAP_OBJECTS_PATH)
        self.rendering = Rendering(self)
        
        self.player_id = 'player 0'

    def get_player(self):
        return self.world.entities[self.player_id]

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                return

            # the difference between 'pygame.key.get_pressed()' and event.key (if event.type == pygame.KEYDOWN) in 'pygame.event.get()' 
            # seems to be that a key pressed continously will only activate one time.
            # therefore, if we want to have a key that is supposed to be only pressed once, we can check it here.
            # otherwise, for keys that are meant to stay pressed (for example, movement keys), we can check them with 'pygame.key.get_pressed()'. 
            if event.type != pygame.KEYDOWN:
                continue # because we can only check 'event.key' if 'event.type == pygame.KEYDOWN'.
            if event.key == pygame.K_c:
                self.player_id = self.world.get_new_player_id(self.player_id)


        keys = pygame.key.get_pressed()

        if keys[pygame.K_ESCAPE]:
            self.playing = False
            return

        acceleration = [0, 0]
        if keys[pygame.K_d]:
            acceleration[0] += 1
        if keys[pygame.K_q]:
            acceleration[0] -= 1
        if keys[pygame.K_s]:
            acceleration[1] += 1
        if keys[pygame.K_z]:
            acceleration[1] -= 1
        self.world.entities[self.player_id].compute_acceleration(acceleration)

    def loop(self):
        while self.playing:
            # boucle évènements
            self.check_events()

            # logique jeu
            self.world.compute_movements(self.delta)

            # affichage
            self.rendering.render()
            pygame.display.update()

            # délai
            self.delta = self.clock.tick(self.fps) / 1000
            #print(self.delta)

# les TODO ont étés déplacés dans 'documentation/todo.md'.
