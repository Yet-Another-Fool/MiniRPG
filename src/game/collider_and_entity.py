import pygame
import math
from config import TILE_SIZE, COLLIDERS_STATS, ENTITIES_STATS, MAX_ACCELERATION
from assets_loader import assets
from typing import Literal
from .game import Game
from utils import clamp

class Collider:
    def __init__(self, name: str, starting_position: tuple[int | float, int | float]):
        self.name = name

        self.position = starting_position
        self.position_on_screen = self.position # temporary

        #self.hitbox: pygame.Rect | None = None
        # an hitbox with block coordinates doesnt really work (bugs + pygame.Rect cant have floats), so we'll only use hitboxes on the screen (in pixels instead of coordinates)
        self.hitbox_on_screen: pygame.Rect | None = None
        self.health: int | None = None
        self.defense: int | None = None

        self.load_stats()

    def load_stats(self):
        if self.name in COLLIDERS_STATS.keys():
            stats = COLLIDERS_STATS[self.name]
        else:
            stats = COLLIDERS_STATS['default']

        self.hitbox_on_screen = pygame.Rect(self.position[0], self.position[1], stats['hitbox'][0], stats['hitbox'][1])
        self.health = stats['health']
        self.defense = stats['defense']

    def calc_position_on_screen(self, offset_x, offset_y):
        self.position_on_screen = (self.position[0] * TILE_SIZE + offset_x, self.position[1] * TILE_SIZE + offset_y)
        if self.hitbox_on_screen != None:
            #self.hitbox_on_screen = pygame.Rect(self.position_on_screen[0], self.position_on_screen[1], self.hitbox_on_screen[2], self.hitbox_on_screen[3])
            self.hitbox_on_screen = pygame.Rect(
                self.position_on_screen[0] + ((TILE_SIZE / 2) - (self.hitbox_on_screen[2] / 2)), 
                self.position_on_screen[1] + ((TILE_SIZE / 2) - (self.hitbox_on_screen[3] / 2)), 
                self.hitbox_on_screen[2], 
                self.hitbox_on_screen[3]
            )
            # so that the hitbox is 'centered'

    def check_death(self):
        pass

    #def check_collision(self, other: 'Collider' | 'Entity'):
    def check_collision(self, other):
        if (self.hitbox_on_screen == None) or (other.hitbox_on_screen == None):
            return False
        return self.hitbox_on_screen.colliderect(other.hitbox_on_screen)

    #def calc_position(self, other: 'Collider' | 'Entity'):
    def calc_distance(self, other):
        '''This function returns the distance IN BLOCKS between two Collider (or Entity).'''
        return math.sqrt((other.position[0] - self.position[0]) ** 2 + (other.position[1] - self.position[1]) ** 2)

class Entity(Collider):
    def __init__(self, name: str, starting_position: tuple[int | float, int | float], x_interval: tuple[int, int], y_interval: tuple[int, int]):
        super().__init__(name, starting_position)

        self.min_x: int = x_interval[0]
        self.max_x:int = x_interval[1]
        self.min_y: int = y_interval[0]
        self.max_y: int = y_interval[1]
        # self.max_x = (game.world.blocks_size[0] - 1)
        # self.max_y = (game.world.blocks_size[1] - 1)
        # je ne sais pas pourquoi il faut le '-1', mais sans lui l'entité peut sortir de la map

        self.attack_power: int = 5
        self.speed: int | float = 1
        self.max_acceleration: int | float = self.speed * MAX_ACCELERATION

        self.dx: int = 0
        self.dy: int = 0

        self.load_stats()

    def load_stats(self):
        if self.name in ENTITIES_STATS.keys():
            stats = ENTITIES_STATS[self.name]
        else:
            stats = ENTITIES_STATS['default']

        self.hitbox_on_screen = pygame.Rect(self.position[0] - stats['hitbox'][0], self.position[1] - stats['hitbox'][1], stats['hitbox'][0], stats['hitbox'][1])
        self.health = stats['health']
        self.defense = stats['defense']
        self.attack_power = stats['attack_power']
        self.speed = stats['speed']
        self.max_acceleration = self.speed * MAX_ACCELERATION

    def get_skin(self):
        return f'{self.name}'
    
    def compute_animation(self):
        pass
    
    def accelerate(self, delta, *, dx: int = 0, dy: int = 0):
        self.dx = clamp(self.dx + (dx * self.speed * delta), -self.max_acceleration * delta, self.max_acceleration * delta)
        self.dy = clamp(self.dy + (dy * self.speed * delta), -self.max_acceleration * delta, self.max_acceleration * delta)

    def apply_friction(self, friction, delta):
        if self.dx > 0:
            self.dx -= friction * delta
            if self.dx < 0:
                self.dx = 0
        else:
            self.dx += friction * delta
            if self.dx > 0:
                self.dx = 0

        if self.dy > 0:
            self.dy -= friction * delta
            if self.dy < 0:
                self.dy = 0
        else:
            self.dy += friction * delta
            if self.dy > 0:
                self.dy = 0      

    #def apply_movement(self, others: list['Collider' | 'Entity']):
    def apply_movement(self, others: list, offset_x: int, offset_y: int):
        precision = 2 # because we don't need enormous floats

        current_pos = self.position
        future_pos = (clamp(round(self.position[0] + self.dx, precision), self.min_x, self.max_x), clamp(round(self.position[1] + self.dy, precision), self.min_y, self.max_y))
        
        self.position = future_pos
        self.calc_position_on_screen(offset_x, offset_y)

        for other in others:
            if self.check_collision(other):
                self.position = current_pos
                self.calc_position_on_screen(offset_x, offset_y)
                # if a collision is found, the position and hitbox will revert back to their previous state
                
                distance = self.calc_distance(other)
                # we calculate the distance bewteen the two
                
                # new_future_pos = (clamp(round(self.position[0] + distance, precision), self.min_x, self.max_x), clamp(round(self.position[1] + distance, precision), self.min_y, self.max_y))
                # self.position = new_future_pos
                # self.calc_position_on_screen(offset_x, offset_y)
                # we try to move the two Collider/Entity as close as possible (currently really broken)
                
                return 

        # TODO: how to do when a collision is found but the speed of an entity is too fast ? because there will be a gap. how to remove this gap, how to move the two Collider/Entity as close as possible ?

    def attack(self, other):
        pass
