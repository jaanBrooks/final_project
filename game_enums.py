from enum import IntEnum
class PLAYER_STATE(IntEnum):
    IDLE = 0
    RUNNING = 1
    SLIDING = 2
    JUMPING = 3
    FALLING = 4
    WALL_SLIDING = 5
    
class TILE_STATE(IntEnum):
    AIR = 0
    FLOOR = 1
    TILE_HALF = 4
    COFFEE = 5
    TILE_WALL = 6
    TILE_LEVEL_END = 7
    TILE_YAPPER = 8
    BEER = 9
class AnimationType(IntEnum):
    REPEATING = 1
    ONESHOT = 2

class Direction(IntEnum):
    LEFT = -1
    RIGHT = 1
    
class GAME_STATE(IntEnum):
    TITLE = 0
    PLAYING = 1
    PAUSED = 2
    LOST = 3
    WIN = 4
    TRANSITION = 5
    INTRO_EMAIL = 6
    OFFICIAL_ENROLLMENT = 7
    MONTAGE = 8
    DROPPED_OUT = 9
    MIDTERM = 10
    MIDTERM_UPDATE = 11
    LVL_TWO_INST = 12
    LVL_ONE_INST = 13
    OUT_OF_TIME = 14
    RETAKE = 15
    
    
class GAME_LEVEL(IntEnum):
    ONE = 0
    TWO = 1
    THREE = 2