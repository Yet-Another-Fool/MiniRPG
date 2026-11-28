import pygame
from assets_loader import assets
from config import PLAYER_SKINS_PATH, PLAYER_ANIMATIONS_STATES, PLAYER_ANIMATION_WAIT, PLAYER_INDICATOR_ON_MINIMAP_SIZE, PLAYER_INDICATOR_ON_MINIMAP_COLOR, PLAYER_HITBOX_COEFF, HITBOXES_COEFF
from .collider_and_entity import Entity
from typing import Literal

class Player(Entity):
    type Direction = Literal['sud', 'nord', 'est', 'ouest']
    type AnimationState = Literal['marche', 'repos']

    def __init__(self, name, asset_filepath: str, starting_position, x_interval, y_interval):
        super().__init__(name, asset_filepath, starting_position, x_interval, y_interval)
        
        self.inventory = {}
        
        self.current_direction: Player.Direction = 'sud'

        self.anim_states: dict[Player.AnimationState, list[int]] = PLAYER_ANIMATIONS_STATES
        self.anim_state: Player.AnimationState = 'repos'
        self.anim_state_frame: int = 0
        self.anim_delay_counter: int = 0
        self.anim_delay: int = PLAYER_ANIMATION_WAIT
        
        self.indicator_on_minimap_size = PLAYER_INDICATOR_ON_MINIMAP_SIZE
        self.indicator_on_minimap_color = PLAYER_INDICATOR_ON_MINIMAP_COLOR  

        self.load_player_stats()
        self.calc_decalages_on_screen()

    def load_player_stats(self): # to overwrite some things inherited by the Entity.__init__() (or Collider.__init__()).        
        self.hitbox_on_screen = pygame.Rect(
            self.position_on_screen[0], 
            self.position_on_screen[1], 
            (self.hitbox_on_screen[2] / HITBOXES_COEFF[0]) * PLAYER_HITBOX_COEFF[0], 
            (self.hitbox_on_screen[3] / HITBOXES_COEFF[1]) * PLAYER_HITBOX_COEFF[1]
        )   

    def get_skin(self):
        return f'{PLAYER_SKINS_PATH}personnage {self.current_direction} {self.anim_states[self.anim_state][self.anim_state_frame]:0>2}'

    def compute_animation(self):
        if self.velocity_vector.x > 0:
            self.current_direction = 'est'
        elif self.velocity_vector.x < 0:
            self.current_direction = 'ouest'
        elif self.velocity_vector.y > 0:
            self.current_direction = 'sud'
        elif self.velocity_vector.y < 0:
            self.current_direction = 'nord'
        
        self.anim_delay_counter += 1
        if self.anim_delay_counter >= self.anim_delay:
            self.anim_delay_counter = 0

            new_state: Player.AnimationState = 'marche' if self.velocity_vector.x or self.velocity_vector.y else 'repos'
            if new_state != self.anim_state:
                self.anim_state = new_state
                self.anim_state_frame = 0
            else:
                self.anim_state_frame = (self.anim_state_frame + 1) % len(self.anim_states[self.anim_state])
