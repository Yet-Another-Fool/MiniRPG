
import pygame
from config import MINIMAP_CURRENT_FORMAT, MINIMAP_DECALAGE, MINIMAP_SIZE_DIVIDER, TILE_SIZE, ADDED_SAFETY_TILES, MINIMAP_CAMERA_INDICATOR_COLOR, MINIMAP_CAMERA_INDICATOR_WITDH, MINIMAP_CAMERA_INDICATOR_ADDED_SIZE, MINIMAP_BORDER_COLOR, MINIMAP_BORDER_WIDTH, PLAYER_INDICATOR_ON_MINIMAP_COLOR
from assets_loader import assets
from task import Task
from .game import Game

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

    def __clamp(self, n: int | float, a: int | float, b: int | float):
        if n <= a:
            return a
        if n >= b:
            return b
        return n

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
        self.offset_x = self.__clamp(self.offset_x + dx, -self.max_x, 0)
        self.offset_y = self.__clamp(self.offset_y + dy, -self.max_y, 0)

    def set_offset(self, x: int, y: int):
        self.offset_x = self.__clamp(x, -self.max_x, 0)
        self.offset_y = self.__clamp(y, -self.max_y, 0)

    def get_visible_things(self, things: list | dict) -> list[tuple[str, tuple[float, float]]]:
        '''
        The goal of this method is to only render things that are within the screen.
        - This method takes either a list or a dict of things that are within the world.
        - If it is a list, each sub-list has to be a row of elements, the tile psoition being represented by [index_row, index_element].
        - If it is a dict, each key is a pair of coordinates representing a tile, and each value an element.
        - Either way, an element is just the path to its asset.
        - It returns the list of visible things, with each element being a tuple : an str (its asset filepath) and a position on the screen (a tuple of 2 floats).
        '''
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

    def render_prio(self, things: list | dict):
        temp_radius = 1
        real_player_pos = self.game.player.position_on_screen
        visible_things = self.get_visible_things(things)
        
        positions_under_player = set()
        positions_under_player.add(real_player_pos)
        for _ in range(1, temp_radius+1):
            new = set()
            for pos in positions_under_player:
                new.add((pos[0] - TILE_SIZE, pos[1] + TILE_SIZE))
                new.add((pos[0], pos[1] + TILE_SIZE))
                new.add((pos[0] + TILE_SIZE, pos[1] + TILE_SIZE))
            positions_under_player.update(new)
        positions_under_player.discard(real_player_pos)

        # for p in positions_under_player:
        #     pygame.draw.rect(self.game.screen, 'red', (p[0], p[1], TILE_SIZE, TILE_SIZE))

        priority_things = []
        for thing in visible_things:
            for pos in positions_under_player:
                within_x = abs(pos[0] - thing[0][0]) <= TILE_SIZE
                within_y = pos[1] - thing[0][1] <= TILE_SIZE # on n'utilise pas abs() pour éviter d'ajouter quelque chose au-dessus du joueur
                if within_x and within_y:
                    priority_things.append(thing)
                    break

        for position, thing in priority_things: 
            self.game.screen.blit(assets.get(thing), position)

    def render_player(self):
        #pygame.draw.rect(self.game.screen, 'purple', self.game.player.hitbox_on_screen)
        self.game.screen.blit(assets.get(self.game.player.current_skin), self.game.player.position_on_screen)

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
            self.minimap_position[0] + self.game.player.position[0] * self.minimap_tile_size[0],
            self.minimap_position[1] + self.game.player.position[1] * self.minimap_tile_size[1],
            self.game.player.indicator_on_minimap_size[0],
            self.game.player.indicator_on_minimap_size[1],
        )
        pygame.draw.rect(self.game.screen, self.game.player.indicator_on_minimap_color, player_indicator_on_minimap)

        # minimap borders
        pygame.draw.rect(self.game.screen, self.minimap_border[0], self.minimap_border[1], width=self.minimap_border[2])
        
    def render(self):
        self.game.screen.fill(("black"))
        self.render_visible_things(self.game.world.world_storage['ground']) # renders tiles
        self.render_visible_things(self.game.world.world_storage['decors']) # renders decors
        self.render_visible_things(self.game.world.world_storage['objects']) # renders objects
        self.render_player() # renders the player
        self.render_prio(self.game.world.world_storage['objects']) # renders objects that are under the player on screen, so that the player appears behind them
        self.render_minimap() # renders the minimap
