
import pygame
import math
from config import MINIMAP_CURRENT_FORMAT, MINIMAP_DECALAGE, MINIMAP_SIZE_DIVIDER, TILE_SIZE, ADDED_SAFETY_TILES, RENDER_HITBOXES, MINIMAP_CAMERA_INDICATOR_COLOR, MINIMAP_CAMERA_INDICATOR_WITDH, MINIMAP_CAMERA_INDICATOR_ADDED_SIZE, MINIMAP_BORDER_COLOR, MINIMAP_BORDER_WIDTH, PLAYER_PRIO_DISTANCE, PLAYER_SHOW_PRIO_DETECTOR
from assets_loader import assets
from task import Task
from .game import Game
from utils import clamp

class Rendering:
    def __init__(self, game: Game):
        self.game = game
        self.offset_x: int = 0
        self.offset_y: int = 0
        self.max_x = game.world.blocks_size[0] * TILE_SIZE - self.game.w
        self.max_y = game.world.blocks_size[1] * TILE_SIZE - self.game.h

        self.minimap: pygame.Surface | None = None

        self.priority_render: list[tuple[tuple, str]] = []

        self.compute_minimap()

    def compute_minimap(self):
        size_divider = MINIMAP_SIZE_DIVIDER
        ground = self.game.world.world_storage['ground']
        decors = self.game.world.world_storage['decors']
        blocks_number = self.game.world.blocks_size
        total_blocks = blocks_number[0] * blocks_number[1]
        
        temp_minimap_size = (blocks_number[0], blocks_number[1]) # so that every loaded tile image will have a size of 1
        temp_minimap = pygame.Surface(temp_minimap_size)
        temp_tile_size = (1, 1)
        # the equivalent of doing (temp_minimap_size[0] / blocks_number[0], temp_minimap_size[1] / blocks_number[1])
        # also, 1x1 is the minimum pygame.Surface size (i think that going lower or using a float will cause bugs) 

        for y, line in enumerate(ground):
            for x, tile in enumerate(line):
                temp_minimap.blit(pygame.transform.smoothscale(assets.get_original(tile), temp_tile_size), (x * temp_tile_size[0], y * temp_tile_size[1]))
                Task.get('minimap tiles').set_progess((x + 1 + y * blocks_number[0]) / total_blocks).print_loading_bar()

        total_decors = len(decors)
        i = 0
        for key, value in decors.items():
            temp_minimap.blit(pygame.transform.smoothscale(assets.get_original(value), temp_tile_size), (key[0] * temp_tile_size[0], key[1] * temp_tile_size[1]))
            Task.get('minimap decors').set_progess((i+1) / total_decors).print_loading_bar()
            i += 1

        format = MINIMAP_CURRENT_FORMAT
        horizontal_size = self.game.w / size_divider
        minimap_size = (horizontal_size * format[0], horizontal_size * format[1])

        self.minimap = pygame.transform.smoothscale(temp_minimap, minimap_size)
        self.minimap_position = (self.game.w - minimap_size[0] - MINIMAP_BORDER_WIDTH - MINIMAP_DECALAGE[0], MINIMAP_BORDER_WIDTH + MINIMAP_DECALAGE[1])
        self.minimap_tile_size = (minimap_size[0] / blocks_number[0], minimap_size[1] / blocks_number[1])

        self.camera_rect_on_minimap = (
            self.minimap_position[0] - ((self.offset_x / TILE_SIZE - ADDED_SAFETY_TILES + MINIMAP_CAMERA_INDICATOR_ADDED_SIZE) * self.minimap_tile_size[0]),
            self.minimap_position[1] - ((self.offset_y / TILE_SIZE - ADDED_SAFETY_TILES + MINIMAP_CAMERA_INDICATOR_ADDED_SIZE) * self.minimap_tile_size[1]),
            ((self.game.w // TILE_SIZE + ADDED_SAFETY_TILES * 2 + MINIMAP_CAMERA_INDICATOR_ADDED_SIZE * 2) * self.minimap_tile_size[0]),
            ((self.game.h // TILE_SIZE + ADDED_SAFETY_TILES * 2 + MINIMAP_CAMERA_INDICATOR_ADDED_SIZE * 2) * self.minimap_tile_size[1]),
        )

        self.minimap_border = (
            MINIMAP_BORDER_COLOR, # the color
            (
                self.minimap_position[0] - MINIMAP_BORDER_WIDTH,
                self.minimap_position[1] - MINIMAP_BORDER_WIDTH,
                minimap_size[0] + MINIMAP_BORDER_WIDTH * 2,
                minimap_size[1] + MINIMAP_BORDER_WIDTH * 2,
            ), # the rect
            MINIMAP_BORDER_WIDTH, # the width (without it, the rect will be filled and will hide the minimap)
        )

    def change_offset(self, *, dx: int = 0, dy: int = 0):
        self.offset_x = clamp(self.offset_x + dx, -self.max_x, 0)
        self.offset_y = clamp(self.offset_y + dy, -self.max_y, 0)
        #self.game.get_player().calc_position_on_screen()

    def set_offset(self, x: int, y: int):
        self.offset_x = clamp(x, -self.max_x, 0)
        self.offset_y = clamp(y, -self.max_y, 0)

    def get_visible_things(self, things: list | dict, it_already_has_a_pos=False) -> list[tuple[str, tuple[float, float]]]:
        '''
        The goal of this method is to only render things that are within the screen.
        - This method takes either a list or a dict of things that are within the world.
        - If it is a list, each sub-list has to be a row of elements, the tile psoition being represented by [index_row, index_element].
        - If it is a dict, each key is a pair of coordinates representing a tile, and each value an element.
        - Either way, an element is just the path to its asset.
        - It returns the list of visible things, with each element being a tuple : an str (its asset filepath) and a position on the screen (a tuple of 2 floats).
        - The parameter 'it_already_has_a_pos' is temporary, and used for Collider and Entity things, because the calculated pos would be wrong otherwise.
        '''
        # TODO: find a cleaner way that using 'it_already_has_a_pos'
        visible_things = []
        blocks = self.game.world.blocks_size
        
        x, max_x = -(self.offset_x // TILE_SIZE) - ADDED_SAFETY_TILES, -(self.offset_x // TILE_SIZE) + self.game.w // TILE_SIZE + ADDED_SAFETY_TILES
        y, max_y = -(self.offset_y // TILE_SIZE) - ADDED_SAFETY_TILES, -(self.offset_y // TILE_SIZE) + self.game.h // TILE_SIZE + ADDED_SAFETY_TILES
        
        if x < 0:
            x = 0
        if max_x > blocks[0] - 1:
            max_x = blocks[0] - 1
        if y < 0:
            y = 0
        if max_y > blocks[1] - 1:
            max_y = blocks[1] - 1

        initial_x = x

        if type(things) == list:
            def get_element(x, y):
                if y < 0 or y >= len(things):
                    return
                if x < 0 or x >= len(things[y]):
                    return
                return things[y][x]
        
        elif type(things) == dict:
            def get_element(x, y):
                if (x, y) not in things.keys():
                    return
                return things[(x, y)]

        while y <= max_y:
            while x <= max_x:
                pos = (x * TILE_SIZE + self.offset_x, y * TILE_SIZE + self.offset_y)
                element = get_element(x, y)
                if element != None:
                    visible_things.append((pos, element))
                x += 1
            y += 1
            x = initial_x

        return visible_things

    def render_visible_things(self, things: list | dict):
        things_to_render = self.get_visible_things(things)
        for position, thing in things_to_render:
            self.game.screen.blit(assets.get(thing), position)

    def render_visible_colliders(self, colliders: dict): # temporary
        # TODO: find a better way to render the colliders (because the pos calculated by .get_visible_things() is wrong for them, and that's why we need this function)
        for collider in colliders.values():
            self.game.screen.blit(assets.get(collider.name), collider.surface_position_on_screen)

    def render_prio(self, things: list | dict):
        real_player_pos = self.game.get_player().surface_position_on_screen
        visible_things = self.get_visible_things(things)

        def calc_distance(point_a, point_b):
            return math.sqrt((point_b[0] - point_a[0]) ** 2 + (point_b[1] - point_a[1]) ** 2)

        max_range = PLAYER_PRIO_DISTANCE * TILE_SIZE

        if PLAYER_SHOW_PRIO_DETECTOR:
            circle_center = (real_player_pos[0] + self.game.get_player().hitbox_on_screen[2], real_player_pos[1] + self.game.get_player().hitbox_on_screen[3])
            # not the real center, but better visually
            pygame.draw.circle(self.game.screen, 'red', circle_center, max_range, width=10, draw_bottom_left=True, draw_bottom_right=True)

        for position, thing in visible_things:
            if position[1] >= real_player_pos[1]: # check if the object is under the player
                if calc_distance(real_player_pos, position) <= max_range:
                    self.game.screen.blit(assets.get(thing), position)

    def render_prio_v2(self, colliders: dict): # temporary
        # TODO: same problem as .render_visible_colliders()
        player = self.game.get_player()
        max_range = PLAYER_PRIO_DISTANCE
        for collider in colliders.values():
            if collider.position[1] >= player.position[1]: # check if the object is under the player
                #if collider.calc_distance(player) <= max_range:
                if collider.calc_distance_squared(player) <= max_range ** 2:
                    self.game.screen.blit(assets.get(collider.name), collider.surface_position_on_screen)

    def render_player(self):
        self.game.screen.blit(assets.get(self.game.get_player().get_skin()), self.game.get_player().surface_position_on_screen)
        # only useful if we want to render the player separately from other entities

    def render_minimap(self):
        # minimap tiles
        self.game.screen.blit(self.minimap, self.minimap_position)

        # camera indicator
        self.camera_rect_on_minimap = (
            self.minimap_position[0] - ((self.offset_x / TILE_SIZE - ADDED_SAFETY_TILES + MINIMAP_CAMERA_INDICATOR_ADDED_SIZE) * self.minimap_tile_size[0]),
            self.minimap_position[1] - ((self.offset_y / TILE_SIZE - ADDED_SAFETY_TILES + MINIMAP_CAMERA_INDICATOR_ADDED_SIZE) * self.minimap_tile_size[1]),
            self.camera_rect_on_minimap[2],
            self.camera_rect_on_minimap[3],
        )
        pygame.draw.rect(self.game.screen, MINIMAP_CAMERA_INDICATOR_COLOR, self.camera_rect_on_minimap, width=MINIMAP_CAMERA_INDICATOR_WITDH)

        # player indicator
        player_indicator_on_minimap = (
            self.minimap_position[0] + self.game.get_player().position[0] * self.minimap_tile_size[0],
            self.minimap_position[1] + self.game.get_player().position[1] * self.minimap_tile_size[1],
            self.game.get_player().indicator_on_minimap_size[0],
            self.game.get_player().indicator_on_minimap_size[1],
        )
        pygame.draw.rect(self.game.screen, self.game.get_player().indicator_on_minimap_color, player_indicator_on_minimap)

        # minimap borders
        pygame.draw.rect(self.game.screen, self.minimap_border[0], self.minimap_border[1], width=self.minimap_border[2])

    def render_hitboxes(self):
        if not RENDER_HITBOXES:
            return
        
        for collider in self.game.world.loaded_colliders.values():
            if collider.hitbox_on_screen != None:
                pygame.draw.rect(self.game.screen, 'red', collider.hitbox_on_screen, width=5)
        for entity in self.game.world.loaded_entities.values():
            if entity.hitbox_on_screen != None:
                pygame.draw.rect(self.game.screen, 'red', entity.hitbox_on_screen, width=5)

    def render_entities(self):
        for entity in self.game.world.loaded_entities.values():
            self.game.screen.blit(assets.get(entity.get_skin()), entity.surface_position_on_screen)
        
    def render(self):
        self.game.screen.fill(("black"))
        self.render_visible_things(self.game.world.world_storage['ground']) # renders tiles
        self.render_visible_things(self.game.world.world_storage['decors']) # renders decors
        self.render_hitboxes()
        #self.render_visible_things(self.game.world.world_storage['objects']) # renders objects
        self.render_visible_colliders(self.game.world.loaded_colliders)
        #self.render_player() # renders the player
        self.render_entities()
        #self.render_prio(self.game.world.world_storage['objects']) # renders objects that are under the player on screen, so that the player appears behind them
        self.render_prio_v2(self.game.world.loaded_colliders)
        self.render_minimap() # renders the minimap
