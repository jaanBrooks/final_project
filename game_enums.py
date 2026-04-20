from enum import IntEnum
class PLAYER_STATE(IntEnum):
    IDLE = 0
    WALKING = 1
    SLIDING = 2
    JUMPING = 3

class AnimationType(IntEnum):
    REPEATING = 1
    ONESHOT = 2

class Direction(IntEnum):
    LEFT = -1
    RIGHT = 1
    
