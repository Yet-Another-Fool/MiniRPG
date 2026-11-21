import pygame
from assets_loader import assets
from config import TILE_SIZE, PLAYER_SKINS_PATH, PLAYER_ANIMATIONS_STATES, PLAYER_ANIMATION_WAIT, PLAYER_INDICATOR_ON_MINIMAP_SIZE, PLAYER_INDICATOR_ON_MINIMAP_COLOR
from .collider_and_entity import Entity
from typing import Literal

class Player(Entity):
    type Direction = Literal['sud', 'nord', 'est', 'ouest']
    type AnimationState = Literal['marche', 'repos']

    def __init__(self, name, starting_position, x_interval, y_interval):
        super().__init__(name, starting_position, x_interval, y_interval)
        
        self.inventory = {}
        
        self.current_direction: Player.Direction = 'sud'

        self.anim_states: dict[Player.AnimationState, list[int]] = PLAYER_ANIMATIONS_STATES
        self.anim_state: Player.AnimationState = 'repos'
        self.anim_state_frame: int = 0
        self.anim_delay_counter: int = 0
        self.anim_delay: int = PLAYER_ANIMATION_WAIT
        
        self.indicator_on_minimap_size = PLAYER_INDICATOR_ON_MINIMAP_SIZE
        self.indicator_on_minimap_color = PLAYER_INDICATOR_ON_MINIMAP_COLOR

        self.hitbox_on_screen = assets.get(self.get_skin()).get_bounding_rect()
        self.hitbox_on_screen = pygame.Rect(self.hitbox_on_screen[0], self.hitbox_on_screen[1], self.hitbox_on_screen[2] // 1.5, self.hitbox_on_screen[3] // 1.5)
        # i think that didviding the player size by 1.5 allows better collisions

    def calc_position_on_screen(self, offset_x, offset_y):
        self.position_on_screen = (self.position[0] * TILE_SIZE + offset_x, self.position[1] * TILE_SIZE + offset_y)
        if self.hitbox_on_screen != None:
            self.hitbox_on_screen = pygame.Rect(self.position_on_screen[0] + ((TILE_SIZE / 2) - (self.hitbox_on_screen[2] / 2)), self.position_on_screen[1] + ((TILE_SIZE / 2) - (self.hitbox_on_screen[3] / 2)), self.hitbox_on_screen[2], self.hitbox_on_screen[3])

        #print(self.position_on_screen, self.hitbox_on_screen)

    def get_skin(self):
        return f'{PLAYER_SKINS_PATH}personnage {self.current_direction} {self.anim_states[self.anim_state][self.anim_state_frame]:0>2}'

    def compute_animation(self):
        if self.dx > 0:
            self.current_direction = 'est'
        elif self.dx < 0:
            self.current_direction = 'ouest'
        if self.dy > 0:
            self.current_direction = 'sud'
        elif self.dy < 0:
            self.current_direction = 'nord'
        
        self.anim_delay_counter += 1
        if self.anim_delay_counter >= self.anim_delay:
            self.anim_delay_counter = 0

            new_state: Player.AnimationState = 'marche' if self.dx or self.dy else 'repos'
            if new_state != self.anim_state:
                self.anim_state = new_state
                self.anim_state_frame = 0
            else:
                self.anim_state_frame = (self.anim_state_frame + 1) % len(self.anim_states[self.anim_state])
