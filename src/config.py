# screen
W, H                                = 1280, 720
FPS                                 = 60

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
RENDER_HITBOXES = False

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
PLAYER_PRIO_DISTANCE                = 1 # in blocks
# how far the ".render_prio()" method will detect objects under the player. 
# it can be useful to prevent rendering bugs, but it can also cause lag if the number is too high.
# for example, if a big house (4x4) is 3 tiles under the player but its hitbox and position are only one tile (1x1, which is an error at least for the hitbox), 
# then setting the distance to 3 or more will still detect it.
PLAYER_SHOW_PRIO_DETECTOR           = False 
# this variable can be used to see the zone of detection for the ".render_prio()" method.
# basically, any object in this zone will be rendered on top of the player.

# camera
CAMERA_SPEED                        = 50 / (1000 / FPS)
# 50 est la valeur que je souhaite atteindre, en pixels.
# puisqu'elle sera multipliée par delta, je la divise d'abord par la valeur que delta est censée être (1000 / FPS), 
# pour qu'elle soit ensuite ramenée à 50 si delta est la bonne valeur (donc sans lag).
'''To be multiplied by game.delta. In pixels.'''
# plus TILE_SIZE sera élevée plus la vitesse sera lente (car l'offset maximum sera plus grand)
# il faut savoir que cette valeur sera multipliée par delta, donc par (1000 / FPS) quand il n'y a pas de lag.

# player
PLAYER_STARTING_POSITION            = (0, 0)
PLAYER_SPEED                        = 0.005 / (1000 / FPS)
# same as 'CAMERA_SPEED', you can look at its explanation to understand why the math looks like this.
'''To be multiplied by delta. In blocks size (meaning that 1 equals a speed of 1 tile per frame).'''

# colliders and entities
COLLIDERS_STATS                     = {
    'default': {'hitbox':[TILE_SIZE * 0.75, TILE_SIZE * 0.75], 'health':100, 'defense':0}
}
ENTITIES_STATS                      = {
    'default': {'hitbox':[TILE_SIZE * 0.75, TILE_SIZE * 0.75], 'health':100, 'defense':5, 'attack_power':10, 'speed':PLAYER_SPEED},
    'player': {'hitbox':[TILE_SIZE, TILE_SIZE], 'health':100, 'defense':5, 'attack_power':10, 'speed':PLAYER_SPEED}
}
MAX_ACCELERATION = (1000 / FPS) # so that the max acceleration is reached in 1 second (without taking friction into account)
'''The maximum amount of acceleration 'stacks'. For example, an entity with an acceleration of 0.1 and a maximum of 10 stacks can reach a speed of 1.'''
FRICTION = 0.0025 / (1000 / FPS)

# temporary
GLOBAL_SIZE_FACTOR                  = 1
W, H                                = round(W * GLOBAL_SIZE_FACTOR), round(H * GLOBAL_SIZE_FACTOR)
TILE_SIZE                           = round(TILE_SIZE * GLOBAL_SIZE_FACTOR)
