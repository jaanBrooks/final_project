from enum import IntEnum
class PLAYER_STATE(IntEnum):
    IDLE = 0
    RUNNING = 1
    SLIDING = 2
    JUMPING = 3
    FALLING = 4
    WALL_SLIDING = 5
    def get_state(state):
        if state == 0:
            return "IDLE"
        if state == 1:
            return "RUNNING"
        if state == 2:
            return "SLIDING"
        if state == 3:
            return "JUMPING"
        if state == 4:
            return "FALLING"
        if state == 5:
            return "WALL_SLIDING"
class TILE_STATE(IntEnum):
    AIR = 0
    SOLID = 1
    COIN = 2 
    ENEMY = 3 
    SOLID_TOP_HALF = 4
    COFFEE = 5
class AnimationType(IntEnum):
    REPEATING = 1
    ONESHOT = 2

class Direction(IntEnum):
    LEFT = -1
    RIGHT = 1
    
