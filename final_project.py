import random
import math
from unittest import case
from raylib import *
from pyray import *
from anim import *
from settings import *
from game_enums import *
from os.path import join

# --- Game Constants ---


# --- Tilemap Definitions ---
""" TILE_AIR = 0
TILE_SOLID = 1
TILE_COIN = 2 
TILE_ENEMY = 3 
TILE_SOLID_TOP_HALF = 4
TILE_COFFEE = 5
"""

# --- Expanded Level Tilemap Definition (50x16 tiles = 2000px wide) ---
LEVEL = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 5, 0, 0, 5, 5, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0],
    [0, 0, 0, 0, 1, 0, 0, 0, 2, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 1, 1, 3, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 3, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
    [0, 0, 2, 0, 4, 0, 4, 4, 4, 4, 4, 4, 0, 4, 0, 2, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
]
TILE_ROWS = len(LEVEL)
TILE_COLS = len(LEVEL[0])

# --- World Dimensions ---
WORLD_WIDTH = TILE_COLS * TILE_SIZE
WORLD_HEIGHT = TILE_ROWS * TILE_SIZE

# --- Utility Functions ---

def parse_level(level):
    """
    Parses the level map, extracts all dynamic entities (coins, enemies), 
    replaces their spawn points with air, and returns the modified collision map and entity lists.
    """
    coins = []
    enemies = []
    coffees = []
    # Create a deep copy of the level to modify the tiles, leaving the original map intact
    new_level = [row[:] for row in level] 
    
    for r in range(TILE_ROWS):
        for c in range(TILE_COLS):
            x = c * TILE_SIZE
            y = r * TILE_SIZE

            if new_level[r][c] == TILE_STATE.COIN:
                # Coin position is center
                coins.append((x + TILE_SIZE / 2, y + TILE_SIZE / 2))
                new_level[r][c] = TILE_STATE.AIR 
            
            elif new_level[r][c] == TILE_STATE.ENEMY:
                # Enemy position is top-left
                enemies.append(Enemy(x, y))
                new_level[r][c] = TILE_STATE.AIR 
            
            elif new_level[r][c] == TILE_STATE.COFFEE:
                coffees.append((x + TILE_SIZE / 2, y + TILE_SIZE / 2))
                new_level[r][c] = TILE_STATE.AIR
                
    return new_level, coins, enemies, coffees


# --- Game Object Classes ---
class Player:
    def __init__(self, x, y):
        
        # Store starting position for reset
        self.start_x = x 
        self.start_y = y
        # Current position (top-left for collision)
        self.x = x
        self.y = y
        self.width = PLAYER_WIDTH
        self.height = PLAYER_HEIGHT
        self.collision_rec = (self.x, self.y, self.width, self.height)
        # Physics
        self.vx = 0.0
        self.vy = 0.0
        self.is_grounded = False
        self.is_sprinting = True
        self.state = PLAYER_STATE.IDLE
        self.anim = Animation(0, 7, 0, 1, .1, .1, AnimationType.REPEATING, 0, 8)
        self.frame = self.anim.frame(PLAYER_TILE_WIDTH, PLAYER_TILE_HEIGHT)
        self.direction = Direction.RIGHT
        self.can_big_jump = False
        self.jumpTimeTimer = JUMP_TIME
        self.sprint_timer = 0.0
        self.sprint_speed_multiplier = 1.0
        self.coffee_count = 0
        
        self.is_wall_sliding = False
        self.is_wall_jumping = False
        
    def startup(self):
        self.idle_texture = load_texture(join('CharacterPack-Version1','Character-No-Weapon', 'idle.png'))
        self.texture = self.idle_texture   
        self.slide_start_texture = load_texture(join('CharacterPack-Version1','Character-No-Weapon', 'slide_start.png'))
        self.slide_middle_texture = load_texture(join('CharacterPack-Version1','Character-No-Weapon', 'slide_middle.png'))
        self.slide_end_texture = load_texture(join('CharacterPack-Version1','Character-No-Weapon', 'slide_end.png'))
        self.running_texture = load_texture(join('CharacterPack-Version1','Character-No-Weapon', 'run.png'))
        self.jump_texture = load_texture(join('CharacterPack-Version1','Character-No-Weapon', 'jump.png'))
    def get_rect(self):
        """Returns the player's collision bounding box (top-left, width, height)."""
        return (self.x, self.y, self.width, self.height)
    def get_rect_sliding(self):
        return self.x, self.y + PLAYER_HEIGHT * 0.5, self.width, self.height * 0.5
    def transition(self, state):
        if self.state == state:
            return
        match state:
            
            case PLAYER_STATE.IDLE:
                self.state = PLAYER_STATE.IDLE
                self.anim.last = 7
                self.anim.cur = 0
                self.anim.type = AnimationType.REPEATING
                self.anim.duration = .1
                self.anim.duration_left = self.anim.duration
                self.anim.sprites_in_row = 8
                self.texture = self.idle_texture
                
            case PLAYER_STATE.RUNNING:
                self.state = PLAYER_STATE.RUNNING
                self.anim.last = 7
                self.anim.cur = 0
                self.anim.type = AnimationType.REPEATING
                self.anim.duration = .1
                self.anim.duration_left = self.anim.duration
                self.anim.sprites_in_row = 8
                self.texture = self.running_texture
            
            case PLAYER_STATE.SLIDING:
                self.anim.done = False
                self.state = PLAYER_STATE.SLIDING
                self.anim.last = 1
                self.anim.cur = 0
                self.anim.type = AnimationType.ONESHOT
                self.anim.duration = .1
                self.anim.duration_left = self.anim.duration
                self.anim.sprites_in_row = 2
                self.texture = self.slide_start_texture
            
            case PLAYER_STATE.JUMPING:
                self.state = PLAYER_STATE.JUMPING
                self.texture = self.jump_texture
                self.anim.last = 5
                self.anim.cur = 0
                self.anim.type = AnimationType.ONESHOT
                self.anim.duration = .1
                self.anim.duration_left = self.anim.duration
                self.anim.sprites_in_row = 6

    def update(self, delta_time, level):
        # 1. Handle Input (Horizontal Movement)
        self.vx = 0.0
        self.sprint_speed_multiplier = 1.0
        
        if self.is_sprinting:
            self.handle_speed_boost(delta_time)
        
        match self.state:
            
            case PLAYER_STATE.IDLE:
                self.handle_speed_boost(delta_time)
                self.handle_left_and_right_input(delta_time)
                
                self.handle_jump_input(delta_time)
            
            case PLAYER_STATE.RUNNING:
                self.handle_speed_boost(delta_time)
                self.handle_jump_input(delta_time)
                self.handle_left_and_right_input(delta_time)
                if IsKeyPressed(KEY_S):
                    self.transition(PLAYER_STATE.SLIDING)
                if self.vx == 0:
                    self.transition(PLAYER_STATE.IDLE)
            
            case PLAYER_STATE.SLIDING:
                self.handle_speed_boost(delta_time)
                self.vx = SLIDE_VELOCITY * self.direction.value
                if self.texture == self.slide_start_texture:
                    
                    if self.anim.done:
                        self.texture = self.slide_middle_texture
                        self.anim.start = 0
                        self.last = 3
                        self.anim.cur = 0
                        self.anim.duration = .3
                        self.anim.duration_left = self.anim.duration
                        self.anim.sprites_in_row = 4
                        self.anim.done = False
                
                elif self.texture == self.slide_middle_texture:
                    if self.anim.done and not self.check_slide_head_collision(level):
                        self.texture = self.slide_end_texture
                        self.anim.start = 0
                        self.anim.last = 1
                        self.anim.cur = 0
                        self.anim.duration = .1
                        self.anim.duration_left = self.anim.duration
                        self.anim.sprites_in_row = 2
                        self.anim.done = False
                else:
                    if self.anim.done:
                        if not self.check_slide_head_collision(level):
                            self.transition(PLAYER_STATE.IDLE)
            case PLAYER_STATE.JUMPING:
                self.handle_speed_boost(delta_time)
                self.handle_jump_input(delta_time)
                self.handle_left_and_right_input(delta_time)
                if self.is_grounded:
                    self.transition(PLAYER_STATE.IDLE)
        
        
        # 3. Apply Gravity
        self.vy += GRAVITY * delta_time
        if self.vy > 1000:
            self.vy = 1000

        # --- Reset grounded state at start of frame update ---
        self.is_grounded = False
        
        # Apply X movement
        self.x += self.vx * delta_time
        self.is_wall_sliding = False
        self.handle_tile_collision(level, 'X')
        
        # Apply Y movement
        self.y += self.vy * delta_time
        self.handle_tile_collision(level, 'Y')
        
        if not self.is_grounded and (IsKeyDown(KEY_A) or IsKeyDown(KEY_D)) and self.vx == 0:
            self.is_wall_sliding = True
        
        # --- Safety Clamp to World Bounds ---
        self.x = max(0, min(self.x, WORLD_WIDTH - self.width))
        
        self.anim.update(delta_time)
        self.frame = self.anim.frame(PLAYER_TILE_WIDTH, PLAYER_TILE_HEIGHT)
        self.frame.width *= self.direction.value
    def handle_speed_boost(self, delta_time):
        if self.is_sprinting:
            self.sprint_timer -= delta_time
            self.sprint_speed_multiplier = SPRINT_AMPLIFIER
            if self.sprint_timer <= 0:
                self.is_sprinting = False
                self.sprint_timer = 0
            
    def handle_left_and_right_input(self, dt):
        if IsKeyDown(KEY_LEFT_SHIFT) and not self.is_sprinting and self.coffee_count > 0:
            self.is_sprinting = True
            self.coffee_count -= 1
            self.sprint_timer += COFFEE_SPRINT_INCREMENTER
        if IsKeyDown(KEY_A):
            self.vx = -PLAYER_SPEED * self.sprint_speed_multiplier
            self.direction = Direction.LEFT
            if self.is_grounded:
                self.transition(PLAYER_STATE.RUNNING)
        elif IsKeyDown(KEY_D):
            self.vx = PLAYER_SPEED * self.sprint_speed_multiplier
            self.direction = Direction.RIGHT
            if self.is_grounded:
                self.transition(PLAYER_STATE.RUNNING)
        return
    
    def handle_jump_input(self, dt):
        if IsKeyPressed(KEY_SPACE) and self.is_grounded:
            self.is_grounded = False
            self.vy = JUMP_VELOCITY
            self.transition(PLAYER_STATE.JUMPING)
            self.can_big_jump = True
            self.jumpTimeTimer = JUMP_TIME
        if IsKeyDown(KEY_SPACE) and self.can_big_jump:
            if self.jumpTimeTimer > 0:
                self.vy = JUMP_VELOCITY
                self.jumpTimeTimer -= dt
            else:
                self.can_big_jump = False
        else:
            if IsKeyReleased(KEY_SPACE):
                self.can_big_jump = False
    
    #easy way to check if the player will collide with a tile with normal hitbox but not with sliding hitbox so we now know whether to keep sliding or not
    def check_slide_head_collision(self, level):
        player_norm_rect = self.get_rect()
        player_slide_rect = self.get_rect_sliding()
        
        px, py, pw, ph = player_norm_rect
        min_col = int(px / TILE_SIZE)
        max_col = int((px + pw) / TILE_SIZE)
        min_row = int(py / TILE_SIZE)
        max_row = int((py + ph) / TILE_SIZE)
        for row in range(min_row, max_row + 1):
            for col in range(min_col, max_col + 1):
                
                if row < 0 or row >= TILE_ROWS or col < 0 or col >= TILE_COLS:
                    continue
                
                if level[row][col] == TILE_STATE.SOLID or (level[row][col] == TILE_STATE.SOLID_TOP_HALF):
                    if level[row][col] == TILE_STATE.SOLID_TOP_HALF:
                        tile_rect = (col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE, TILE_SIZE // 2)
                    else:
                        tile_rect = (col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                    
                    if CheckCollisionRecs(player_norm_rect, tile_rect) and not CheckCollisionRecs(player_slide_rect, tile_rect):
                        return True
        return False
    def handle_tile_collision(self, level, axis):
        """Performs AABB collision checks against solid tiles and resolves the collision."""
        if self.state == PLAYER_STATE.SLIDING:
            player_rect = self.get_rect_sliding()
        else:
            player_rect = self.get_rect()
        px, py, pw, ph = player_rect
        
        min_col = int(px / TILE_SIZE)
        max_col = int((px + pw) / TILE_SIZE)
        min_row = int(py / TILE_SIZE)
        max_row = int((py + ph) / TILE_SIZE)

        for row in range(min_row, max_row + 1):
            for col in range(min_col, max_col + 1):
                
                if row < 0 or row >= TILE_ROWS or col < 0 or col >= TILE_COLS:
                    continue
                
                if level[row][col] == TILE_STATE.SOLID or (level[row][col] == TILE_STATE.SOLID_TOP_HALF):
                    match level[row][col]:
                        case TILE_STATE.SOLID:
                            tile_rect = (col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                        case TILE_STATE.SOLID_TOP_HALF:
                            tile_rect = (col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE, TILE_SIZE // 2)
                    if CheckCollisionRecs(player_rect, tile_rect):
                        if axis == 'X':
                            
                            if self.vx > 0: # Moving Right
                                self.x = tile_rect[0] - self.width
                            elif self.vx < 0: # Moving Left
                                self.x = tile_rect[0] + TILE_SIZE
                            self.vx = 0.0 
                            
                        elif axis == 'Y':
                            if self.vy >= 0: # Falling (Hitting Ground)
                                self.y = tile_rect[1] - self.height
                                self.is_grounded = True 
                            elif self.vy < 0: # Jumping (Hitting Ceiling)
                                self.y = tile_rect[1] + TILE_SIZE
                                
                            self.vy = 0.0 
                            
                        player_rect = self.get_rect()
                        px, py, pw, ph = player_rect
                
                        
    def check_collection(self, collectibles):
        """Checks for collision with collectibles and returns indices of collected items."""
        collected_indices = []
        if self.state == PLAYER_STATE.SLIDING:
            player_rect = self.get_rect_sliding()
        else:
            player_rect = self.get_rect()
        
        
        for i, (cx, cy) in enumerate(collectibles):
            collectible_rect = (cx + 8, cy + 8, TILE_SIZE - 16, TILE_SIZE - 16)
            
            if CheckCollisionRecs(player_rect, collectible_rect):
                collected_indices.append(i)
                
        return collected_indices
    
    def check_enemy_collision(self, enemies):
        """Checks for collision with enemies and determines outcome (stomp or death).
        Returns (hit_type, enemy_index) or (None, -1).
        hit_type: "STOMP" (safe kill) or "LETHAL" (death)
        """
        player_rect = self.get_rect()
        px, py, pw, ph = player_rect
        
        for i, enemy in enumerate(enemies):
            enemy_rect = enemy.get_rect()
            
            if CheckCollisionRecs(player_rect, enemy_rect):
                
                # STOMP Condition: 
                # 1. Player is falling (vy > 0) 
                # 2. Player's bottom is above the enemy's mid-point (approximate stomping zone)
                is_stompable_zone = py + ph < enemy.y + enemy.height * 0.5 
                
                if self.vy > 0 and is_stompable_zone:
                    return "STOMP", i
                else:
                    # Lethal collision (side, head, or missing the stomp zone)
                    return "LETHAL", i
                    
        return None, -1
    
    def reset(self):
        """Resets the player to their starting position."""
        self.x = self.start_x
        self.y = self.start_y
        self.vx = 0.0
        self.vy = 0.0
        self.is_grounded = False

    def draw(self, is_hitbox_visible):
        """Draws the player at their world coordinates."""
        #DrawRectangle(int(self.x), int(self.y), int(self.width), int(self.height), BLUE) 
        draw_texture_pro(self.texture, self.frame, Rectangle(self.x - PLAYER_TILE_WIDTH / 3, self.y - PLAYER_TILE_HEIGHT / 2.2, PLAYER_TILE_WIDTH, PLAYER_TILE_HEIGHT), Vector2(0, 0), 0.0, WHITE)
        if is_hitbox_visible:
            if self.state == PLAYER_STATE.SLIDING:
                DrawRectangleLines(int(self.x), int(self.y + self.height * 0.5), int(self.width), int(self.height * 0.5), RED)
            else:
                DrawRectangleLines(int(self.x), int(self.y), int(self.width), int(self.height), RED)
        draw_text(PLAYER_STATE.get_state(self.state),200,200,11, BLACK)
        draw_text(str(self.sprint_timer),int(self.x),250,11, BLACK)
        draw_text(str("is wall sliding: " + str(self.is_wall_sliding)),int(self.x),270,11, BLACK)
        draw_text(str("is grounded: " + str(self.is_grounded)),int(self.x),290,11, BLACK)
        
class Enemy:
    def __init__(self, x, y):
        # Position (top-left for collision)
        self.x = x
        self.y = y
        self.width = TILE_SIZE * 0.7
        self.height = TILE_SIZE * 0.7
        
        # Physics/Movement
        self.vx = ENEMY_SPEED # Start moving right
        self.vy = 0.0 
        self.is_grounded = False

    def get_rect(self):
        """Returns the enemy's collision bounding box."""
        return (self.x, self.y, self.width, self.height)

    def update(self, delta_time, level):
        # 1. Apply Gravity
        if self.is_grounded:
            self.vy = 0.0
        self.vy += GRAVITY * delta_time
        self.is_grounded = False 

        # 2. Apply Movement 

        # Apply X movement
        self.x += self.vx * delta_time
        self.handle_tile_collision(level, 'X')
        
        # Apply Y movement
        self.y += self.vy * delta_time
        self.handle_tile_collision(level, 'Y')

    def handle_tile_collision(self, level, axis):
        """Enemy collision: reverses direction on horizontal wall contact, respects vertical floor contact."""
        enemy_rect = self.get_rect()
        px, py, pw, ph = enemy_rect
        
        min_col = int(px / TILE_SIZE)
        max_col = int((px + pw) / TILE_SIZE)
        min_row = int(py / TILE_SIZE)
        max_row = int((py + ph) / TILE_SIZE)

        for row in range(min_row, max_row + 1):
            for col in range(min_col, max_col + 1):
                
                if row < 0 or row >= TILE_ROWS or col < 0 or col >= TILE_COLS:
                    continue
                
                if level[row][col] == TILE_STATE.SOLID:
                    tile_rect = (col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                elif level[row][col] == TILE_STATE.SOLID_TOP_HALF:
                    tile_rect = (col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE, TILE_SIZE / 2)    
                    if CheckCollisionRecs(enemy_rect, tile_rect):
                        
                        if axis == 'X':
                            # Reverses direction on horizontal collision
                            if self.vx > 0:
                                self.x = tile_rect[0] - self.width
                            elif self.vx < 0:
                                self.x = tile_rect[0] + TILE_SIZE
                            self.vx *= -1 # Reverse direction
                            
                        elif axis == 'Y':
                            if self.vy >= 0: # Hitting Ground
                                self.y = tile_rect[1] - self.height
                                self.is_grounded = True 
                                
                            self.vy = 0.0 
                            
                        enemy_rect = self.get_rect() # Update rect after resolution

    def draw(self):
        """Draws the enemy as a red rectangle with a directional indicator."""
        DrawRectangle(int(self.x), int(self.y), int(self.width), int(self.height), RED)
        DrawRectangleLines(int(self.x), int(self.y), int(self.width), int(self.height), BLACK)
        
        # Draw a small indicator for direction
        center_x = self.x + self.width / 2
        center_y = self.y + self.height / 2
        indicator_size = self.width * 0.2
        
        if self.vx > 0: # Moving Right
            DrawTriangle(Vector2(center_x + indicator_size, center_y), 
                         Vector2(center_x - indicator_size, center_y - indicator_size), 
                         Vector2(center_x - indicator_size, center_y + indicator_size), WHITE)
        elif self.vx < 0: # Moving Left
            DrawTriangle(Vector2(center_x - indicator_size, center_y), 
                         Vector2(center_x + indicator_size, center_y - indicator_size), 
                         Vector2(center_x + indicator_size, center_y + indicator_size), WHITE)


# --- Drawing and Camera Functions (Unchanged) ---
                
def draw_level(level):
    """Draws the solid tiles of the level map."""
    for row in range(TILE_ROWS):
        for col in range(TILE_COLS):
            tile_value = level[row][col]
            if tile_value == TILE_STATE.SOLID:
                x = col * TILE_SIZE
                y = row * TILE_SIZE
                
                DrawRectangle(x, y, TILE_SIZE, TILE_SIZE, DARKGRAY)
                DrawRectangleLines(x, y, TILE_SIZE, TILE_SIZE, BLACK)
            
            if tile_value == TILE_STATE.SOLID_TOP_HALF:
                x = col * TILE_SIZE
                y = row * TILE_SIZE
                
                DrawRectangle(x, y, TILE_SIZE, TILE_SIZE // 2, DARKGRAY)
                DrawRectangleLines(x, y, TILE_SIZE, TILE_SIZE // 2, BLACK)

def draw_coffees(coffees, coffee_texture,is_hitbox_mode):
    for cx, cy in coffees:
        draw_texture_pro(coffee_texture, Rectangle(0, 0, 64, 64), Rectangle(cx,cy, TILE_SIZE, TILE_SIZE), Vector2(0, 0), 0.0, WHITE)
        if is_hitbox_mode:
            DrawRectangleLines(int(cx) + 8, int(cy) + 8, int(TILE_SIZE) - 16, int(TILE_SIZE) - 16, BLUE)

def draw_coins(coins):
    """Draws the active coins as small yellow diamonds (polygons)."""
    radius = TILE_SIZE * 0.3 / 2 
    
    for cx, cy in coins:
        v1 = Vector2(cx, cy - radius * 2)
        v2 = Vector2(cx + radius * 1.5, cy)
        v3 = Vector2(cx, cy + radius * 2)
        v4 = Vector2(cx - radius * 1.5, cy)
        
        DrawTriangle(v1, v2, v4, YELLOW)
        DrawTriangle(v2, v3, v4, GOLD)
        
        DrawLineV(v1, v3, BLACK)
        DrawLineV(v2, v4, BLACK)


def update_camera(camera, player, world_width, world_height, screen_width, screen_height):
    """Centers the camera on the player and clamps the camera's target to the world bounds."""
    
    camera.target.x = player.x + player.width / 2
    camera.target.y = player.y + player.height / 2

    min_x = screen_width / 2
    max_x = world_width - screen_width / 2
    
    if camera.target.x < min_x:
        camera.target.x = min_x
    if camera.target.x > max_x:
        camera.target.x = max_x

    min_y = screen_height / 2
    max_y = world_height - screen_height / 2
    
    if camera.target.y < min_y:
        camera.target.y = min_y
    if camera.target.y > max_y:
        camera.target.y = max_y
    
    camera.offset.x = screen_width / 2
    camera.offset.y = screen_height / 2


# --- Main Game Logic ---
def main():
    # --- Initialization ---
    InitWindow(SCREEN_WIDTH, SCREEN_HEIGHT, "Raylib 2D Platformer Clone (Stomp Mechanic)".encode('utf-8'))
    SetTargetFPS(60)

    # Prepare Level Data: Separate collision map from dynamic entities
    game_level, coins, enemies, coffees = parse_level(LEVEL)
    
    # Game State Variables
    # Player starts at TILE_SIZE * 2, TILE_SIZE * 2
    player = Player(TILE_SIZE * 2, TILE_SIZE * 2)
    player.startup() # Load player textures/animations
    score = 0
    game_state = "PLAYING" 
    
    # --- Camera Initialization ---
    camera = Camera2D()
    camera.target = Vector2(player.x, player.y) 
    camera.offset = Vector2(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2) 
    camera.rotation = 0.0
    camera.zoom = 1.0
    is_hitbox_mode = False
    
    #textures
    coffee_texture = load_texture(join('Items','coffee.png'))

    # --- Game Loop ---
    while not WindowShouldClose():
        
        delta_time = GetFrameTime()
        if IsKeyPressed(KEY_H):
            is_hitbox_mode = not is_hitbox_mode
        # --- Update ---
        if game_state == "PLAYING":
            player.update(delta_time, game_level)
            # Update Enemies
            for enemy in enemies:
                enemy.update(delta_time, game_level)

            update_camera(camera, player, WORLD_WIDTH, WORLD_HEIGHT, SCREEN_WIDTH, SCREEN_HEIGHT)

            # Check for coin collection
            collected_indices = player.check_collection(coins)
            if collected_indices:
                for index in sorted(collected_indices, reverse=True):
                    coins.pop(index)
                    score += 10

            # Check for coffee collection
            if player.coffee_count < COFFEE_MAX:
                collected_coffee_indices = player.check_collection(coffees)
                if collected_coffee_indices:
                    for index in sorted(collected_coffee_indices, reverse=True):
                        coffees.pop(index)
                        player.coffee_count += 1

            # Check for enemy collision (Stomp/Death/Reset)
            hit_type, enemy_index = player.check_enemy_collision(enemies)

            if hit_type == "STOMP":
                # Stomp mechanic: Remove enemy, score, and bounce
                enemies.pop(enemy_index)
                score += 100 
                player.vy = STOMP_BOUNCE # Player bounces up
                
            elif hit_type == "LETHAL":
                # Death/Reset mechanic: Penalty and restart
                player.reset()
                score -= 50 
                if score < 0: score = 0
            
        # --- Draw ---
        BeginDrawing()
        ClearBackground(SKYBLUE) 
        
        # Start the 2D camera mode
        BeginMode2D(camera)
        
        # 1. Draw the Level
        draw_level(game_level)

        # 2. Draw Collectibles
        draw_coins(coins)
        draw_coffees(coffees, coffee_texture,is_hitbox_mode)
            
        # 3. Draw Enemies
        for enemy in enemies:
            enemy.draw()

        # 4. Draw Player 
        player.draw(is_hitbox_mode)
        
        # End the 2D camera mode
        EndMode2D()
        
        # 5. Draw HUD (Drawn on screen, outside of BeginMode2D)
        score_text = f"Score: {score}".encode('utf-8')
        DrawText(score_text, SCREEN_WIDTH - MeasureText(score_text, 20) - 10, 10, 20, BLACK)
        
        debug_text = f"Grounded: {player.is_grounded} | Enemies: {len(enemies)}".encode('utf-8')
        DrawText(debug_text, 10, 10, 20, BLACK) 


        EndDrawing()

    # --- De-Initialization ---
    CloseWindow()

if __name__ == "__main__":
    main()
