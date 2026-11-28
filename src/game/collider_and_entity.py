import pygame
import math
from config import EXPECTED_DELTA, TILE_SIZE, ENTITIES_AND_COLLIDERS_STATS, HITBOXES_COEFF, MAX_ACCELERATION
from assets_loader import assets
from typing import Literal
from .game import Game
from utils import clamp

class Collider:
    def __init__(self, name: str, asset_filepath: str, starting_position: tuple[int | float, int | float]):
        self.name = name
        self.asset_filepath = asset_filepath

        self.position: pygame.Vector2 = pygame.Vector2(starting_position[0], starting_position[1])
        self.position_on_screen: pygame.Vector2 = self.position # temporary (and wrong until .calc_position_on_screen() is called)
        
        self.surface_position_on_screen: pygame.Vector2 = self.position # temporary (and wrong until .calc_position_on_screen() is called)
        # we need this variable because the position of the collider, its surface and its hitbox can be 3 different things

        self.hitbox_on_screen: pygame.Rect | None = None
        self.health: int | None = None
        self.defense: int | None = None

        self.load_collider_stats()
        self.calc_decalages_on_screen()

    def load_collider_stats(self):
        if self.name in ENTITIES_AND_COLLIDERS_STATS.keys():
            stats = ENTITIES_AND_COLLIDERS_STATS[self.name]
        else:
            stats = ENTITIES_AND_COLLIDERS_STATS['default']

        if 'hitbox' in stats.keys():
            self.hitbox_on_screen = stats['hitbox']
            self.surface_size: tuple[int, int] = assets.get(self.asset_filepath).get_size()
        else:
            self.asset_size: tuple[int, int] = assets.get(self.asset_filepath).get_bounding_rect()[2:]
            # TODO: just replace by a rect, no ?
            self.surface_size: tuple[int, int] = assets.get(self.asset_filepath).get_size()
            self.hitbox_on_screen = pygame.Rect(
                self.position_on_screen[0],
                self.position_on_screen[1],
                self.asset_size[0] * HITBOXES_COEFF[0],
                self.asset_size[1] * HITBOXES_COEFF[1]
            )
        self.health = stats['health']
        self.defense = stats['defense']

    def calc_decalages_on_screen(self):
        self.surface_position_decalage_x = (TILE_SIZE - self.surface_size[0]) / 2
        self.surface_position_decalage_y = (TILE_SIZE - self.surface_size[1]) / 2
        # so that the surface is 'centered', because it can be smaller or bigger than a tile.

        if self.hitbox_on_screen == None:
            return
        
        self.hitbox_decalage_x = (TILE_SIZE - self.hitbox_on_screen[2]) / 2
        self.hitbox_decalage_y = (TILE_SIZE - self.hitbox_on_screen[3]) / 2
        if self.hitbox_on_screen[2] > TILE_SIZE:
            self.hitbox_decalage_x = -(self.hitbox_on_screen[2] - TILE_SIZE) / 2
        if self.hitbox_on_screen[3] > TILE_SIZE:
            self.hitbox_decalage_y = -(self.hitbox_on_screen[3] - TILE_SIZE) / 2
        # so that the hitbox is 'centered' (the center being the center of the tile represented by the position. 
        # for example, with a position of (3, 3) and a hitbox of (2, 2), the hitbox is a 2x2 rectangle starting from (2.5, 2.5) and ending in (4.5, 4.5).)
        # (another example, for a position of (1, 1) and a 1x1 rectangle, is an hitbox going form (0.5, 0.5) to (1.5, 1.5).)
        # i hope i didnt explain too badly :)

    def calc_position_on_screen(self, offset_x, offset_y):
        self.position_on_screen = (self.position[0] * TILE_SIZE + offset_x, self.position[1] * TILE_SIZE + offset_y)
        self.surface_position_on_screen = (self.position_on_screen[0] + self.surface_position_decalage_x, self.position_on_screen[1] + self.surface_position_decalage_y
                )

        if self.hitbox_on_screen == None:
            return
        
        self.hitbox_on_screen = pygame.Rect(
            self.position_on_screen[0] + self.hitbox_decalage_x, 
            self.position_on_screen[1] + self.hitbox_decalage_y, 
            self.hitbox_on_screen[2], 
            self.hitbox_on_screen[3]
        )

    def check_death(self):
        pass

    #def check_collision(self, other: 'Collider' | 'Entity'):
    def check_collision(self, other):
        if (self.hitbox_on_screen == None) or (other.hitbox_on_screen == None):
            return False
        return self.hitbox_on_screen.colliderect(other.hitbox_on_screen)

    def calc_position(self, other: 'Collider | Entity'):
    #def calc_distance(self, other):
        '''This function returns the distance IN BLOCKS between two Collider (or Entity).'''
        return math.sqrt((other.position[0] - self.position[0]) ** 2 + (other.position[1] - self.position[1]) ** 2)

    def calc_distance_squared(self, other):
        '''This function returns the distance IN BLOCKS and SQUARED between two Collider (or Entity).
        It is faster than .calc_distance() because it avoids using math.sqrt().'''
        return (other.position[0] - self.position[0]) ** 2 + (other.position[1] - self.position[1]) ** 2

class Entity(Collider):
    def __init__(self, name: str, asset_filepath: str, starting_position: tuple[int | float, int | float], x_interval: tuple[int, int], y_interval: tuple[int, int]):
        super().__init__(name, asset_filepath, starting_position)

        self.min_x: int = x_interval[0]
        self.max_x:int = x_interval[1]
        self.min_y: int = y_interval[0]
        self.max_y: int = y_interval[1]

        self.attack_power: int = 5
        self.speed: int | float = 1
        self.max_speed: int | float = self.speed * MAX_ACCELERATION

        self.position_vector: pygame.Vector2 = pygame.Vector2(self.position[0], self.position[1])
        self.velocity_vector: pygame.Vector2 = pygame.Vector2(0, 0)

        self.load_entity_stats()

    def load_entity_stats(self):
        if self.name in ENTITIES_AND_COLLIDERS_STATS.keys():
            stats = ENTITIES_AND_COLLIDERS_STATS[self.name]
        else:
            stats = ENTITIES_AND_COLLIDERS_STATS['default']

        self.attack_power = stats['attack_power']
        self.speed = stats['speed']
        self.max_speed = self.speed * MAX_ACCELERATION

    def get_skin(self):
        return self.asset_filepath
    
    def compute_animation(self):
        pass

    def compute_acceleration(self, acceleration: list[int | float]):
        acceleration_direction = pygame.Vector2(acceleration[0], acceleration[1])
        acceleration_direction.project
        if acceleration_direction.length_squared() > 0:
            acceleration_direction = acceleration_direction.normalize()

        acceleration_vector: pygame.Vector2 = acceleration_direction * self.speed

        self.velocity_vector += acceleration_vector
        if self.velocity_vector.length_squared() > 0:
            self.velocity_vector = self.velocity_vector.clamp_magnitude(self.max_speed)
        
    def apply_additive_friction(self, friction, delta):
        if self.velocity_vector.x > 0:
            self.velocity_vector.x -= friction * delta
            if self.velocity_vector.x < 0:
                self.velocity_vector.x = 0
        else:
            self.velocity_vector.x += friction * delta
            if self.velocity_vector.x > 0:
                self.velocity_vector.x = 0

        if self.velocity_vector.y > 0:
            self.velocity_vector.y -= friction * delta
            if self.velocity_vector.y < 0:
                self.velocity_vector.y = 0
        else:
            self.velocity_vector.y += friction * delta
            if self.velocity_vector.y > 0:
                self.velocity_vector.y = 0  

    def apply_multiplicative_friction(self, friction, delta):
        minimum_precision = 10
        # changes the required speed value to start applying friction (the speed needs to be higher than 1/(10**precision)) 
        # higher values = harder to start moving (because friction applied earlier)
        # be careful to not set precision too low, or else the entity just wont be able to move
        # honestly, this value has almost no impact, and can be ignored
        stopping_precision = 0.5
        # changes the required speed value to stop appyling friction and just setting the value to 0 (the speed needs to be lower than 1/(10**precision)) 
        # higher values = takes more time to stop (because the speed value will be small, but not 0)
        # be careful, you need to set it lower than 'minimum_precision', or else friction will not be applied and speed will not be set to 0
        # be careful to not set precision too low, because the entity will be stopped so early that it wont be able to begin moving
        result_precision = 2
        # to prevent numbers too small, floats too big.
        # be careful to set it higher than 'minimum_precision' and 'stopping_precision', or else the numbers wont be able to be small enough

        #TODO: move those precisions into 'config.py'

        # if abs(self.velocity_vector.x) > 1/(10 ** minimum_precision):
        #     self.velocity_vector.x = round(self.velocity_vector.x * (friction ** (delta / EXPECTED_DELTA)), result_precision)
        # if abs(self.velocity_vector.y) > 1/(10 ** minimum_precision):
        #     self.velocity_vector.y = round(self.velocity_vector.y * (friction ** (delta / EXPECTED_DELTA)), result_precision)
        # if self.velocity_vector.length_squared() > (1/(10 ** minimum_precision)) ** 2:
        #     self.velocity_vector = round(self.velocity_vector * (friction ** (delta / EXPECTED_DELTA)), result_precision)
        self.velocity_vector = round(self.velocity_vector * (friction ** (delta / EXPECTED_DELTA)), result_precision)
        # temporary
        # TODO: fix this :)

        if abs(self.velocity_vector.x) < 1/(10 ** stopping_precision):
            self.velocity_vector.x = 0
        if abs(self.velocity_vector.y) < 1/(10 ** stopping_precision):
            self.velocity_vector.y = 0
        # if self.velocity_vector.magnitude() < 1/(10 ** stopping_precision):
        #     self.velocity_vector.x, self.velocity_vector.y = 0, 0
        
        # TODO: do not round the velocity to avoid bugs, only round it when we use it or when we print it

    def apply_movement(self, delta: float, others: list[Collider], offset_x: int, offset_y: int):
        precision = 2 # because we don't need enormous floats

        movement: pygame.Vector2 = self.velocity_vector * delta

        def _apply(pos):
            self.position = pos
            self.calc_position_on_screen(offset_x, offset_y)
            # 'teleport' to the next position

        current_pos = self.position.copy()
        future_pos = pygame.Vector2(clamp(round(self.position.x + movement.x, precision), self.min_x, self.max_x), clamp(round(self.position.y + movement.y, precision), self.min_y, self.max_y))
        _apply(future_pos)
        
        if self.hitbox_on_screen == None:
            return

        for other in others:
            if self.check_collision(other):
                _apply(current_pos)
                # if a collision is found, revert back to the previous state, no movement applied
                return
        return

        # TODO: how to do when a collision is found but the speed of an entity is too fast ? because there will be a gap. how to remove this gap, how to move the two Collider/Entity as close as possible ?

    def apply_movement_v2(self, delta: float, others: list[Collider], offset_x: int, offset_y: int): # needs '.compute_acceleration()' te be called beforehand
        # maybe try using https://research.ncl.ac.uk/game/mastersdegree/gametechnologies/physicstutorials/4collisiondetection/Physics%20-%20Collision%20Detection.pdf
        # or https://courses.cs.duke.edu/spring08/cps124/notes/13_collisions/collision_detection.pdf
        # or just this https://www.youtube.com/watch?v=dn0hUgsok9M
        # (currently, i didnt use any of those, and the goal is to use collision normals (and pygame.Vector2, if possible))

        precision = 2 # because we don't need enormous floats

        movement: pygame.Vector2 = self.velocity_vector * delta

        def _apply(pos):
            self.position = pos
            self.calc_position_on_screen(offset_x, offset_y)
            # 'teleport' to the next position

        current_pos = self.position.copy()
        future_pos = pygame.Vector2(clamp(round(self.position.x + movement.x, precision), self.min_x, self.max_x), clamp(round(self.position.y + movement.y, precision), self.min_y, self.max_y))
        _apply(future_pos)
        
        if self.hitbox_on_screen == None:
            return
        
        # surface_travelled = pygame.Rect(current_pos.x, current_pos.y, (future_pos.x - current_pos.x) + self.surface_size[0], (future_pos.y - current_pos.y) + self.surface_size[0])
        # surface_travelled_on_screen = pygame.Rect(
        #     surface_travelled[0] * TILE_SIZE + offset_x, 
        #     surface_travelled[1] * TILE_SIZE + offset_y,
        #     surface_travelled[2] * TILE_SIZE,
        #     surface_travelled[3] * TILE_SIZE
        # )
        # roughly the are where collisions may have happened during movement, better than 'teleporting' the entity to the future position (because it can move trough objects, if fast enough)
        # TODO: currenty not used, try to use this

        for other in others:
            if other.hitbox_on_screen == None:
                continue
            
            # if surface_travelled_on_screen.colliderect(other.hitbox_on_screen):
            # self_hitbox_in_tiles = (self.hitbox_on_screen.width / TILE_SIZE, self.hitbox_on_screen.height / TILE_SIZE)
            if self.check_collision(other):
                # other_hitbox_in_tiles = (other.hitbox_on_screen.width / TILE_SIZE, other.hitbox_on_screen.height / TILE_SIZE)

                # # X-collision
                # if movement.x > 0:
                #     # movement.x = other.position.x - current_pos.x - self_hitbox_in_tiles[0]
                #     movement.x = (other.hitbox_on_screen.x - self.hitbox_on_screen.x - self.hitbox_on_screen.width) / (TILE_SIZE)
                # elif movement.x < 0:
                #     # movement.x = other.position.x - current_pos.x + other_hitbox_in_tiles[0]
                #     movement.x = (other.hitbox_on_screen.x - self.hitbox_on_screen.x + other.hitbox_on_screen.width) / (TILE_SIZE)

                # # Y-collision
                # if movement.y > 0:
                #     # movement.y = other.position.y - current_pos.y + other_hitbox_in_tiles[1]
                #     movement.y = (other.hitbox_on_screen.y - self.hitbox_on_screen.y - self.hitbox_on_screen.height) / (TILE_SIZE)
                # elif movement.y < 0:
                #     # movement.y = other.position.y - current_pos.y - self_hitbox_in_tiles[1]
                #     movement.y = (other.hitbox_on_screen.y - self.hitbox_on_screen.y + other.hitbox_on_screen.height) / (TILE_SIZE)

                # future_pos = pygame.Vector2(clamp(round(current_pos.x + movement.x, precision), self.min_x, self.max_x), clamp(round(current_pos.y + movement.y, precision), self.min_y, self.max_y))
                # _apply(future_pos)

                overlap_x = min(self.hitbox_on_screen.x + self.hitbox_on_screen.width, other.hitbox_on_screen.x + other.hitbox_on_screen.width) - max(self.hitbox_on_screen.x, other.hitbox_on_screen.x)
                overlap_y = min(self.hitbox_on_screen.y + self.hitbox_on_screen.height, other.hitbox_on_screen.y + other.hitbox_on_screen.height) - max(self.hitbox_on_screen.y, other.hitbox_on_screen.y)

                normal: pygame.Vector2 = pygame.Vector2(0, 0)
                if overlap_x < overlap_y: # meaning the the normal will be horizontal
                    if self.position.x < other.position.x: # meaning that 'self' is left of 'other'
                        normal.x = -1
                    else: # meaning that 'self' is right of 'other'
                        normal.x = 1
                else: # meaning that the normal will be vertical
                    if self.position.y < other.position.y: # meaning that 'self' is above 'other'
                        normal.y = -1
                    else: # meaning that 'self' is under 'other'
                        normal.y = 1

                result = movement.dot(normal)
                if result < 0:
                    projection = result * normal
                    movement -= projection

                future_pos = pygame.Vector2(clamp(round(current_pos.x + movement.x, precision), self.min_x, self.max_x), clamp(round(current_pos.y + movement.y, precision), self.min_y, self.max_y))
                _apply(future_pos)


                # TODO: the big problem is that we need to make the difference bewteen position and position on screen, 
                # and currently we're trying to change the position but 'hitbox' doesnt exists (only 'hitbox_on_screen')
                # we need the change that, and we also need to remember that 'self.position_on_screen.x' != 'self.hitbox_on_screen.x', for example (not necessaily true, only to remember to not mix up values)
                
                # TODO: we also really need to find a better way than the position in tiles and the position in pixels, because sometimes I dont know which one I should use :/

                # return # do we stop or not ?

    def attack(self, other):
        pass

    def print_velocity(self):
        print(f'\r{self.velocity_vector.x:<10} {self.velocity_vector.y:<10} ', end="", flush=True)
