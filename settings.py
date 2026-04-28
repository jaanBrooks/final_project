from pyray import Vector2


SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
TILE_SIZE = 40          # Size of one tile in pixels
GRAVITY = 1800.0        # Downward acceleration (pixels/s/s)
JUMP_VELOCITY = -300.0  # Initial upward velocity on jump
STOMP_BOUNCE = JUMP_VELOCITY * 0.6 # Reduced jump velocity for bounce
PLAYER_SPEED = 400.0    # Player horizontal movement speed
ENEMY_SPEED = 100.0     # Enemy horizontal movement speed
PLAYER_WIDTH = TILE_SIZE * 0.8
PLAYER_HEIGHT = TILE_SIZE * 0.9
BULLET_SPEED = 500.0 
SPRINT_AMPLIFIER = 2.0
JUMP_TIME = .3
COFFEE_SPRINT_INCREMENTER = 2
COFFEE_MAX = 2

PLAYER_TILE_HEIGHT = 64
PLAYER_TILE_WIDTH = 96
SLIDE_VELOCITY = PLAYER_SPEED * .8

WALL_SLIDE_SPEED = 20.0
WALL_JUMP_POWER = Vector2(300, -480)
WALL_JUMP_DURATION = .3
MAX_FALL_SPEED = 600