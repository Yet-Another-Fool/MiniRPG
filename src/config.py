# screen
W, H                                = 1280, 720
FPS                                 = 60
EXPECTED_DELTA                      = (1 / FPS)

# assets
ASSETS_PATH                         = 'assets_finaux'
ASSETS_SIZES                        = {}
# dictionnaire pour l'instant non utilisé, pourrait servir plus tard à assigner une taille à chaque asset

# cartes
MAP_CSV_FILES_PATH                  = f'{ASSETS_PATH}/cartes'
MAP_GROUND_FILE_PATH                = f'{MAP_CSV_FILES_PATH}/monde_sol.csv'
MAP_DECORS_FILE_PATH                = f'{MAP_CSV_FILES_PATH}/monde_decors.csv'
MAP_OBJECTS_PATH                    = f"{MAP_CSV_FILES_PATH}/monde_objets.csv"

# world loading
MINIMAP_SIZE_DIVIDER                = 5

# world rendering
TILE_SIZE                           = 64
ADDED_SAFETY_TILES                  = 1
# number of additional tiles rendered in each direction to avoid voids (when the player moves its camera)
# i don't even know why i made this variable, any value besides 1 will cause bugs and won't make any sense...
RENDER_HITBOXES                     = True

# minimap rendering (currently, can also be considered part of 'world rendering')
MINIMAP_FORMATS                     = [(1, H/W), (1, 1), (1, 0.7)]
MINIMAP_CURRENT_FORMAT              = MINIMAP_FORMATS[2]
MINIMAP_DECALAGE                    = (10, 10) # en pixels
MINIMAP_CAMERA_INDICATOR_COLOR      = 'red'
MINIMAP_CAMERA_INDICATOR_WITDH      = 2 # en pixels
MINIMAP_CAMERA_INDICATOR_ADDED_SIZE = 2 # en tiles
# n'ajoute aucune tile, sert juste à rendre plus grand l'indicateur de caméra sur la minimap (ou plus petit)
MINIMAP_BORDER_COLOR                = 'black'
MINIMAP_BORDER_WIDTH                = 4 # en pixels
# optional setting to increase the size of the camera indicator

# player_rendering
PLAYER_SKINS_PATH                   = f'personnage/'
PLAYER_ANIMATIONS_STATES            = {
    "repos": [ 0 ],
    "marche": [ 1, 2, 3, 2 ],
    "frappe": [ 0, 4, 4, 5, 5, 0 ],
    "recolte": [ 0, 6, 6, 0 ],
    "utilise": [ 0, 7, 7, 0 ],
}
PLAYER_ANIMATION_WAIT               = 10
PLAYER_INDICATOR_ON_MINIMAP_SIZE    = (5, 5)
PLAYER_INDICATOR_ON_MINIMAP_COLOR   = 'purple'
PLAYER_PRIO_DISTANCE                = 10 # in blocks
# how far the ".render_prio()" method will detect objects under the player. 
# it can be useful to prevent rendering bugs, but it can also cause lag if the number is too high.
# for example, if a big house (4x4) is 3 tiles under the player but its hitbox and position are only one tile (1x1, which is an error at least for the hitbox), 
# then setting the distance to 3 or more will still detect it.
# also, i just set the value high to prevent some bugs that i couldnt fix :) (basically, if a collider is in the prio range, it can be rendered on top of others colliders, which is annoying)
PLAYER_SHOW_PRIO_DETECTOR           = False 
# this variable can be used to see the zone of detection for the ".render_prio()" method.
# basically, any object in this zone will be rendered on top of the player.

# player
PLAYER_STARTING_POSITION            = (110, 110)
PLAYER_SPEED                        = 0.5
#PLAYER_SPEED                        = 0.5 / (FPS/60) # because i want the speed to stay the same, no matter the FPS, and i want it to be 'normal' when FPS == 60
#                                                       (doesnt work because we would have to change the math for other things, because the speed hasnt the same value)
'''To be multiplied by delta. In blocks size (meaning that 1 equals a speed of 1 tile per frame, and at 60 FPS, 60 tiles per second).'''
# TODO: we should try to make it so that the speed's value represent the wanted number of tile per second. 1 speed should be 1 tile per second, not 60.
PLAYER_HITBOX_COEFF                 = (0.75, 0.375)
# i think that multiplying the player size by (0.75, 0.375) gives a hitbox that allows better collisions
# it's a ratio based on the size of the player's asset, that's why the second coeff is smaller : 
# the player's asset is a rectangle that's bigger vertically, and we want it to be a small square in the middle of the player.
# sorry for the bad explanation, if you want you can check it with RENDER_HITBOXES set to True.

# colliders and entities
ENTITIES_AND_COLLIDERS_STATS        = {
    'default': {'health':100, 'defense':5, 'attack_power':10, 'speed':PLAYER_SPEED},
    'player': {'health':100, 'defense':5, 'attack_power':10, 'speed':PLAYER_SPEED}
}
HITBOXES_COEFF                      = (0.75, 0.75)
#HITBOXES_COEFF                      = (1, 1) # temporary, to be only used when we want to check if hitboxes are correctly on top of images
#MAX_ACCELERATION                    = FPS // 4 # so that the max acceleration is reached in MAX_ACCELERATION frames (without taking friction into account)
MAX_ACCELERATION                    = 15 # so that the max acceleration is reached in MAX_ACCELERATION frames (without taking friction into account)
'''The maximum amount of acceleration 'stacks'. For example, an entity with an acceleration of 0.1 and a maximum of 10 stacks can reach a speed of 1.'''
# TODO: please fix this. it is really broken, and doesnt work as expected.
ADDITIVE_FRICTION                   = 0.25 / EXPECTED_DELTA
#MULTIPLICATIVE_FRICTION             = 0.90 / EXPECTED_DELTA
MULTIPLICATIVE_FRICTION             = 0.95
# TODO: the math for 'MULTIPLICATIVE_FRICTION' is wrong, 
# because if for example expected delta is 16 and delta is 32, then MULTIPLICATIVE_FRICTION = (0.95/16)*32 = 1.90, which will accelerate entities infinitely.
COLLIDERS_REAL_SIZE                 = True
'''This variable is temporary. If set to True, the colliders and their assets will be of their 'original size'. If not, they will be of the TILE_SIZE size.'''

# temporary
GLOBAL_SIZE_FACTOR                  = 1
W, H                                = round(W * GLOBAL_SIZE_FACTOR), round(H * GLOBAL_SIZE_FACTOR)
TILE_SIZE                           = round(TILE_SIZE * GLOBAL_SIZE_FACTOR)
