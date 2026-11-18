import pygame
import math
from assets_loader import assets
from config import TILE_SIZE, PLAYER_STARTING_POSITION, PLAYER_SPEED, PLAYER_SKINS_PATH, PLAYER_ANIMATIONS_STATES, PLAYER_ANIMATION_WAIT, PLAYER_INDICATOR_ON_MINIMAP_SIZE, PLAYER_INDICATOR_ON_MINIMAP_COLOR
from .game import Game

class Player:
    def __init__(self, game: Game):
        self.game = game

        self.max_x = (game.world.blocks_size[0] - 1)
        self.max_y = (game.world.blocks_size[1] - 1)
        self.position = (PLAYER_STARTING_POSITION[0] * TILE_SIZE, PLAYER_STARTING_POSITION[1] * TILE_SIZE)
        self.position_on_screen = self.position # temporary
        self.speed = PLAYER_SPEED
        self.dx: int = 0
        self.dy: int = 0

        self.animation_states = PLAYER_ANIMATIONS_STATES
        self.current_direction = 'sud'
        self.current_state = self.animation_states['repos'][0]
        self.animation_wait = 0
        self.animation_max_wait = PLAYER_ANIMATION_WAIT

        self.current_skin: str = f'{PLAYER_SKINS_PATH}/personnage sud {self.current_state}'
        
        self.indicator_on_minimap_size = PLAYER_INDICATOR_ON_MINIMAP_SIZE
        self.indicator_on_minimap_color = PLAYER_INDICATOR_ON_MINIMAP_COLOR

        #self.size = assets.get(self.current_skin).get_size()
        #self.hitbox = pygame.Rect(self.position[0], self.position[1], self.size[0], self.size[1])
        self.hitbox = assets.get(self.current_skin).get_bounding_rect()
        self.hitbox_on_screen = self.hitbox # temporary
        self.size = self.hitbox[2:]
        
        ''' Ideas of possible variables : 
        self.health = 100
        self.inventory = {}
        self.size = TILE_SIZE
        '''

        #self.animation()

    def animation(self):
        if self.dx > 0:
            self.current_direction = 'est'
        elif self.dx < 0:
            self.current_direction = 'ouest'
        if self.dy > 0:
            self.current_direction = 'sud'
        elif self.dy < 0:
            self.current_direction = 'nord'
        
        self.animation_wait += 1
        if self.animation_wait >= self.animation_max_wait:
            self.animation_wait = 0
            if self.dx or self.dy:
                animations_marches = self.animation_states['marche']
                changed = False
                for index, s in enumerate(animations_marches):
                    if self.current_state == s:
                        self.current_state = animations_marches[(index+1) % (len(animations_marches))]
                        changed = True
                        self.dx, self.dy = 0, 0
                        break
                if not changed:
                    self.current_state = animations_marches[0]
            else:
                self.current_state = self.animation_states['repos'][0]

        self.current_skin = f'{PLAYER_SKINS_PATH}/personnage {self.current_direction} {self.current_state}'

    def __clamp(self, n: int | float, a: int | float, b: int | float):
        if n <= a:
            return a
        if n >= b:
            return b
        return n

    def move(self, *, dx: int = 0, dy: int = 0):
        precision = 2
        dx, dy = round(dx * self.speed * self.game.delta, precision), round(dy * self.speed * self.game.delta, precision)
        self.dx, self.dy = dx, dy
        
        future_pos = (self.__clamp(self.position[0] + self.dx, 0, self.max_x), self.__clamp(self.position[1] + self.dy, 0, self.max_y))
        rounded_future_pos = (round(future_pos[0]), round(future_pos[1]))
        
        if rounded_future_pos not in self.game.world.world_storage['objects'].keys():
            self.position = future_pos
            self.hitbox = pygame.Rect(self.position[0] - self.size[0], self.position[1] - self.size[1], self.size[0], self.size[1])
            self.center_camera()

            self.calc_position_on_screen()
        
    def center_camera(self):
        pos = (
            - int((self.position[0] + 0.5) * TILE_SIZE - self.game.w / 2),
            - int((self.position[1] + 0.5) * TILE_SIZE - self.game.h / 2),
        )
        self.game.rendering.set_offset(pos[0], pos[1])

    def calc_position_on_screen(self):
        self.position_on_screen = (self.position[0] * TILE_SIZE + self.game.rendering.offset_x, self.position[1] * TILE_SIZE + self.game.rendering.offset_y)
        #self.hitbox_on_screen = pygame.Rect(self.position_on_screen[0], self.position_on_screen[1], TILE_SIZE, TILE_SIZE)
        self.hitbox_on_screen = pygame.Rect(self.position_on_screen[0] + self.size[0], self.position_on_screen[1] + (TILE_SIZE - self.size[1]), self.size[0], self.size[1])
