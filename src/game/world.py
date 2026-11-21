import pygame
import csv
from .collider_and_entity import Collider, Entity
from .player import Player
from config import TILE_SIZE, PLAYER_STARTING_POSITION, FRICTION
from assets_loader import assets
from task import Task
from .game import Game

type Position = tuple[int, int]
type Filepath = str

class World:
    def __init__(self, game: Game, ground_filepath: str, decors_filepath: str, objects_filepath: str):
        self.game = game

        self.filepaths = {
            'ground': ground_filepath,
            'decors': decors_filepath,
            'objects': objects_filepath,
        }

        self.world_storage = {
            'ground': [],       # list[list[str]]
            'decors': {},       # dict[tuple, str]
            'objects': {},      # dict[tuple, str]
        }
        '''This dict is only useful to render things. Basically, it only contains positions (tuples) and filepaths (str), which are used in Rendering.'''

        self.blocks_size: tuple[int, int] = (-1, -1) # computed with World.load_ground()
        '''The size of the map, in blocks, in this format : (horizontal_size, vertical_size).'''

        self.colliders: dict[str, Collider] = {}
        '''Each key is an id (a collider name/type and its number), each value a Collider.'''
        self.entities: dict[str, Entity] = {}
        '''Each key is an id (an entity name/type and its number), each value an Entity.'''

        self.collider_range = (self.game.w // TILE_SIZE)
        self.loaded_colliders = {}

        self.entity_range = (self.game.w // TILE_SIZE) * 2
        self.loaded_entities = {}

        self.load_things('ground')
        self.load_things('decors')
        self.load_things('objects')
        self.blocks_size = (len(self.world_storage['ground'][0]), len(self.world_storage['ground']))

        self.load_colliders()
        self.load_entities()

    def load_things(self, filepath_name: str, storage_name: str | None = None):
        filepath = self.filepaths[filepath_name]
        if storage_name == None:
            storage_name = filepath_name
        where_to_store = self.world_storage[storage_name]

        if type(where_to_store) == list:
            def store_element(storage: list, pos, element):
                '''
                This version of the function is for a list.
                - If the row (pos[1]) doesn't exist, a new row will be added.
                - If the element's index (pos[0] doesn't exist, it will be added to the last row.
                - But if the row and the element's index are within the list, the element will replace the value that is currently at this position. 
                '''
                if pos[1] < 0 or pos[1] >= len(storage):
                    storage.append([])
                if pos[0] < 0 or pos[0] >= len(storage[pos[1]]):
                    storage[-1].append(element)
                storage[pos[1]][pos[0]] = element
        elif type(where_to_store) == dict:
            def store_element(storage: dict, pos, element):
                '''
                This version of the function is for a dict. 
                - It only needs to set "pos" as the key and "element" as the value.
                '''
                storage[pos] = element

        filenames = []
        with open(filepath, 'r') as f:
            for iy, ligne in enumerate(csv.reader(f)):
                for ix, element in enumerate(ligne):
                    if len(element) > 1:
                        store_element(where_to_store, (ix, iy), element)
                        if element not in filenames:
                            filenames.append(element)

        assets.load_multiple_assets(filenames, (TILE_SIZE, TILE_SIZE), f'{filepath_name} assets')
        #assets.load_multiple_original_assets(filenames, f'{filepath_name} assets')

    def load_colliders(self):
        index = 0
        total = len(self.world_storage['objects'])
        for position, name in self.world_storage['objects'].items():
            collider = Collider(name, position)
            self.add_collider(name, collider)
            Task.get('colliders').set_progess((index + 1) / total).print_loading_bar()
            index += 1

    def load_entities(self): # TODO (linked to the SavesHandler maybe ? or just a dict of entities in config.py ?)
        self.make_player()
        self.add_entity('player', Player('player', (10, 10), (0, self.blocks_size[0]), (0, self.blocks_size[1])))
        Task.get('entities').set_progess(1).print_loading_bar() # temporary

    def add_collider(self, collider_name, collider: 'Collider'):
        i = 0
        while True:
            id = f'{collider_name} {i}'
            if id not in self.colliders.keys():
                self.colliders[id] = collider
                break
            i += 1

    def add_entity(self, entity_name, entity: 'Entity'):
        i = 0
        while True:
            id = f'{entity_name} {i}'
            if id not in self.entities.keys():
                self.entities[id] = entity
                break
            i += 1

    def make_player(self):
        player = Player('player', PLAYER_STARTING_POSITION, (0, self.blocks_size[0]), (0, self.blocks_size[1]))
        self.add_entity('player', player)

    def compute_loaded_colliders(self):
        '''This method detects which colliders are currently in range and stores them in 'self.loaded_colliders'. 
        Colliders outside of this range will not be checked for collisons (to prevent lag).'''
        self.loaded_colliders = {}
        player = self.entities[self.game.player_id]
        for id, collider in self.colliders.items():
            if collider.calc_distance(player) <= self.collider_range:
                collider.calc_position_on_screen(self.game.rendering.offset_x, self.game.rendering.offset_y)
                self.loaded_colliders[id] = collider

    def compute_loaded_entities(self):
        '''This method detects which entities are currently in range and stores them in 'self.loaded_entities'. 
        Entities outside of this range will not do anything (to prevent lag).'''
        self.loaded_entities = {}
        player = self.entities[self.game.player_id]
        for id, entity in self.entities.items():
            if entity.calc_distance(player) <= self.entity_range:
                entity.calc_position_on_screen(self.game.rendering.offset_x, self.game.rendering.offset_y)
                self.loaded_entities[id] = entity

    def compute_movements(self):
        self.compute_loaded_colliders()
        self.compute_loaded_entities()        

        for id in self.loaded_entities.keys():
            collisions_to_check = self.loaded_entities | self.loaded_colliders
            collisions_to_check.pop(id) # to remove the current entity (to prevent checking its collision with itself)

            collisions_list = []
            for key, value in collisions_to_check.items():
                collisions_list.append(value)
            # to only keep the hitboxes to check in a list (no need for a dict)

            self.entities[id].apply_movement(collisions_list, self.game.rendering.offset_x, self.game.rendering.offset_y)
            self.entities[id].apply_friction(FRICTION, self.game.delta)
            # est-ce que cela modifiera aussi la position des entités dans 'loaded_entities' ? 
            # parce que sinon bugs :/
            # >> exemple : entity_1 bouge de (0, 1) en (1, 1). entity_2 bouge de (1, 0) en (1, 1). 
            # >> est-ce que leurs positions seront aussi modifiées dans loaded_entities ? parce que sinon, la collision ne sera pas détectée.

            self.loaded_entities[id] = self.entities[id] # pour update (est-ce que ça empeche les bugs ? est-ce que ça update bien l'entité ? est-ce qu'il y a meme besoin de cette ligne ?)

        self.center_camera(self.game.player_id)

    def center_camera(self, entity_id):
        pos = (
            - int((self.entities[entity_id].position[0] + 0.5) * TILE_SIZE - self.game.w / 2),
            - int((self.entities[entity_id].position[1] + 0.5) * TILE_SIZE - self.game.h / 2),
        )
        self.game.rendering.set_offset(pos[0], pos[1])

    def get_new_player_id(self, current_id: str): # only useful if we want to control another entity
        entity_list = []
        for id in self.entities.keys():
            entity_list.append(id)

        for index, id in enumerate(entity_list):
            if id == current_id:
                return entity_list[(index + 1) % len(entity_list)]
        return entity_list[0]
