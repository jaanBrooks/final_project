import random
import math
from unittest import case
from raylib import *
from pyray import *
from anim import *
from particle import *
from settings import *
from game_enums import *
from os.path import join
from levels import *

# --- Game Constants ---


# --- Tilemap Definitions ---
""" TILE_AIR = 0
TILE_SOLID = 1
TILE_COIN = 2 
TILE_ENEMY = 3 
TILE_SOLID_TOP_HALF = 4
TILE_COFFEE = 5
"""

# --- Utility Functions ---

def parse_level(level, tile_rows, tile_cols):
    """
    Parses the level map, extracts all dynamic entities (coins, enemies), 
    replaces their spawn points with air, and returns the modified collision map and entity lists.
    """
    enemies = []
    coffees = []
    yappers = []
    beers = []
    # Create a deep copy of the level to modify the tiles, leaving the original map intact
    new_level = [row[:] for row in level] 
    
    for r in range(tile_rows):
        for c in range(tile_cols):
            x = c * TILE_SIZE
            y = r * TILE_SIZE
            
            if new_level[r][c] == TILE_STATE.COFFEE:
                coffees.append((x, y))
                new_level[r][c] = TILE_STATE.AIR
            
            elif new_level[r][c] == TILE_STATE.TILE_YAPPER:
                yappers.append(Yapper(x, y))
            
            elif new_level[r][c] == TILE_STATE.BEER:
                beers.append((x, y))
                new_level[r][c] = TILE_STATE.AIR
                
    return new_level, enemies, coffees, yappers, beers


# Utility function to get level parameters based on level number
def get_level_params(level_to_set):
    time_left_before_decrement = DURATION_BEFORE_DECREMENT
    
    if level_to_set == GAME_LEVEL.ONE:
        game_level, enemies, coffees, yappers, beers = parse_level(LEVEL_1, TILE_ROWS_LEVEL_1, TILE_COLS_LEVEL_1)
        time_left_in_level = LEVEL_ONE_DURATION
        
    elif level_to_set == GAME_LEVEL.TWO:
        game_level, enemies, coffees, yappers, beers = parse_level(LEVEL_2, TILE_ROWS_LEVEL_2, TILE_COLS_LEVEL_2)
        time_left_in_level = LEVEL_TWO_DURATION
       
    return game_level, enemies, coffees, yappers, beers, time_left_in_level, time_left_before_decrement


# --- Game Object Classes ---
class Player:
    def __init__(self, x, y):
        
        # Current position (top-left for collision)
        self.x = x
        self.y = y
        self.width = PLAYER_WIDTH
        self.height = PLAYER_HEIGHT
        
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
        self.wall_jump_lock_timer = 0.0
        
        
        self.is_wall_jumping = False
        self.particles = None
        
        self.collided_with_x = False
        self.reach_level_end = False
        
        self.freshmen_fifteen_meter = 0
        
        self.tile_rows = TILE_ROWS_LEVEL_1
        self.tile_cols = TILE_COLS_LEVEL_1
        self.world_width = WORLD_WIDTH_LEVEL_1
        self.world_height = WORLD_HEIGHT_LEVEL_1
        
        self.start_x = PLAYER_WIDTH * 2 
        self.start_y = self.world_height - TILE_SIZE * 2
        
        self.yap_timer = 0
        self.yap_message = "Blah BLAH blah bLah . . . ."
        
    def startup(self):
        self.idle_texture = load_texture(join('CharacterPack-Version1','Character-No-Weapon', 'idle.png'))
        self.texture = self.idle_texture   
        self.slide_start_texture = load_texture(join('CharacterPack-Version1','Character-No-Weapon', 'slide_start.png'))
        self.slide_middle_texture = load_texture(join('CharacterPack-Version1','Character-No-Weapon', 'slide_middle.png'))
        self.slide_end_texture = load_texture(join('CharacterPack-Version1','Character-No-Weapon', 'slide_end.png'))
        self.running_texture = load_texture(join('CharacterPack-Version1','Character-No-Weapon', 'run.png'))
        self.jump_texture = load_texture(join('CharacterPack-Version1','Character-No-Weapon', 'jump.png'))
        self.wall_slide_middle_texture = load_texture(join('CharacterPack-Version1','Character-No-Weapon', 'wall_slide_middle.png'))
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
                self.anim.duration = .05
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
            
            case PLAYER_STATE.WALL_SLIDING:
                self.state = PLAYER_STATE.WALL_SLIDING
                self.texture = self.wall_slide_middle_texture
                self.anim.last = 3
                self.anim.cur = 0
                self.anim.type = AnimationType.REPEATING
                self.anim.duration = .1
                self.anim.duration_left = self.anim.duration
                self.anim.sprites_in_row = 4

    def update(self, delta_time, level):
        # 1. Handle Input (Horizontal Movement)
        self.sprint_speed_multiplier = 1.0
        if self.yap_timer >= 0:
            self.yap_timer -= delta_time
            if self.yap_timer < 0:
                self.yap_timer = 0
        if self.wall_jump_lock_timer > 0:
            self.wall_jump_lock_timer -= delta_time
            self.vx = WALL_JUMP_POWER.x * self.direction
        else:
            self.is_wall_jumping = False
            self.vx = 0.0

        if self.is_sprinting:
            self.handle_speed_boost(delta_time)
        
        match self.state:
            
            case PLAYER_STATE.IDLE:
                self.handle_speed_boost(delta_time)
                
                if not self.is_wall_jumping and self.yap_timer == 0:
                    self.handle_left_and_right_input(delta_time)
                
                if self.yap_timer == 0:
                    self.handle_jump_input(delta_time)
            
            case PLAYER_STATE.RUNNING:
                self.handle_speed_boost(delta_time)
                if self.yap_timer == 0:
                    self.handle_jump_input(delta_time)
                
                if not self.is_wall_jumping and self.yap_timer == 0:
                    self.handle_left_and_right_input(delta_time)
                
                if IsKeyPressed(KEY_S) and self.yap_timer == 0:
                    self.transition(PLAYER_STATE.SLIDING)
                if self.vx == 0:
                    self.transition(PLAYER_STATE.IDLE)
            
            case PLAYER_STATE.SLIDING:
                will_bang_head = self.check_slide_head_collision(level, self.tile_rows, self.tile_cols )
                self.handle_speed_boost(delta_time)
                self.vx = SLIDE_VELOCITY * self.direction.value   
                if self.texture == self.slide_start_texture:
                    
                    if self.anim.done:
                        self.texture = self.slide_middle_texture
                        self.anim.start = 0
                        self.last = 3
                        self.anim.cur = 0
                        self.anim.duration = .15
                        self.anim.duration_left = self.anim.duration
                        self.anim.sprites_in_row = 4
                        self.anim.done = False
                
                elif self.texture == self.slide_middle_texture:
                    if self.anim.done and not will_bang_head:
                        self.texture = self.slide_end_texture
                        self.anim.start = 0
                        self.anim.last = 1
                        self.anim.cur = 0
                        self.anim.duration = .025
                        self.anim.duration_left = self.anim.duration
                        self.anim.sprites_in_row = 2
                        self.anim.done = False
                    elif will_bang_head and self.anim.done:
                        self.vx = SLIDE_VELOCITY * self.direction * .8
                else:
                    if self.anim.done:
                        self.vx = SLIDE_VELOCITY * self.direction * .2
                        if not self.check_slide_head_collision(level, self.tile_rows, self.tile_cols):
                            self.transition(PLAYER_STATE.IDLE)
            
            case PLAYER_STATE.JUMPING:
                self.handle_speed_boost(delta_time)
                if self.yap_timer == 0:
                    self.handle_jump_input(delta_time)
                
                if not self.is_wall_jumping and self.yap_timer == 0:
                    self.handle_left_and_right_input(delta_time)
                if self.is_grounded:
                    self.transition(PLAYER_STATE.IDLE)
            
            case PLAYER_STATE.WALL_SLIDING:
                if not self.is_wall_sliding:
                    if self.is_grounded:
                        self.transition(PLAYER_STATE.IDLE)
                    else:
                        self.transition(PLAYER_STATE.JUMPING)
                else:
                    self.vx = PLAYER_SPEED * self.direction # need this so the player keeps pressing into the wall and we get a collision every frame
                    self.handle_wall_jump_input()
        if self.particles:
            self.particles.update(Vector2(self.x + self.width / 2, self.y + self.height), delta_time)
        
        # 3. Apply Gravity
        self.vy += GRAVITY * delta_time
        if self.vy > MAX_FALL_SPEED:
            self.vy = MAX_FALL_SPEED

        # --- Reset grounded state at start of frame update ---
        self.is_grounded = False
        
        # Apply X movement
        self.x += self.vx * delta_time
        self.is_wall_sliding = False
        self.collided_with_x = False
        self.handle_tile_collision(level, 'X', self.tile_rows, self.tile_cols)
        
        # Apply Y movement
        self.y += self.vy * delta_time
        self.handle_tile_collision(level, 'Y', self.tile_rows, self.tile_cols)
        
        
        if self.check_wall_slide():
            self.is_wall_sliding = True
            self.transition(PLAYER_STATE.WALL_SLIDING)
            self.y -= self.vy * delta_time * 0.7
        
        # --- Safety Clamp to World Bounds ---
        self.x = max(0, min(self.x, self.world_width - self.width))
        
        self.anim.update(delta_time)
        self.frame = self.anim.frame(PLAYER_TILE_WIDTH, PLAYER_TILE_HEIGHT)
        self.frame.width *= self.direction
    
    def check_wall_slide(self):
        return self.collided_with_x and not self.is_grounded and (IsKeyDown(KEY_A) and self.direction== Direction.LEFT or IsKeyDown(KEY_D) and self.direction == Direction.RIGHT) and self.vx == 0
    
    def handle_wall_jump_input(self):
        
        if IsKeyPressed(KEY_SPACE):
            self.is_wall_jumping = True
            self.is_wall_sliding = False
            self.wall_jump_lock_timer = WALL_JUMP_DURATION
            self.vy = WALL_JUMP_POWER.y
            self.transition(PLAYER_STATE.JUMPING)

            self.direction *= -1
            self.vx = WALL_JUMP_POWER.x * self.direction
    
    def handle_speed_boost(self, delta_time):
        if self.is_sprinting:
            self.sprint_timer -= delta_time
            self.sprint_speed_multiplier = SPRINT_AMPLIFIER
            if self.sprint_timer <= 0:
                self.is_sprinting = False
                self.sprint_timer = 0
                self.particles = None
            
    def handle_left_and_right_input(self, dt):
        
        if IsKeyDown(KEY_LEFT_SHIFT) and not self.is_sprinting and self.coffee_count > 0:
            self.is_sprinting = True
            self.coffee_count -= 1
            self.sprint_timer += COFFEE_SPRINT_DURATION
            self.particles = System(Vector2(self.x + self.width / 2, self.y + self.height))
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
    def check_slide_head_collision(self, level, tile_rows, tile_cols):
        player_norm_rect = self.get_rect()
        player_slide_rect = self.get_rect_sliding()
        
        px, py, pw, ph = player_norm_rect
        min_col = int(px / TILE_SIZE)
        max_col = int((px + pw) / TILE_SIZE)
        min_row = int(py / TILE_SIZE)
        max_row = int((py + ph) / TILE_SIZE)
        
        for row in range(min_row, max_row + 1):
            for col in range(min_col, max_col + 1):
                
                if row < 0 or row >= tile_rows or col < 0 or col >= tile_cols:
                    continue
                
                if level[row][col] == TILE_STATE.FLOOR or (level[row][col] == TILE_STATE.TILE_HALF) or (level[row][col] == TILE_STATE.TILE_WALL):
                    if level[row][col] == TILE_STATE.TILE_HALF:
                        tile_rect = (col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE, TILE_SIZE // 2)
                    else:
                        tile_rect = (col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                    
                    if CheckCollisionRecs(player_norm_rect, tile_rect) and not CheckCollisionRecs(player_slide_rect, tile_rect):
                        return True
        return False
    def handle_tile_collision(self, level, axis, tile_rows, tile_cols):
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

        original_vy = self.vy #needed to prevent shooting up bug
        
        for row in range(min_row, max_row + 1):
            for col in range(min_col, max_col + 1):
                
                if row < 0 or row >= tile_rows or col < 0 or col >= tile_cols:
                    continue
                if level[row][col] == TILE_STATE.TILE_YAPPER:
                    tile_rect = (col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                    if CheckCollisionRecs(player_rect, tile_rect):
                        self.yap_timer = YAP_DURATION
                        level[row][col] = TILE_STATE.AIR
                elif level[row][col] == TILE_STATE.FLOOR or (level[row][col] == TILE_STATE.TILE_HALF) or (level[row][col] == TILE_STATE.TILE_WALL) or (level[row][col] == TILE_STATE.TILE_LEVEL_END) :
                    match level[row][col]:
                        case TILE_STATE.FLOOR:
                            tile_rect = (col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                        case TILE_STATE.TILE_WALL:
                            tile_rect = (col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                        case TILE_STATE.TILE_LEVEL_END:
                            tile_rect = (col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                        case TILE_STATE.TILE_HALF:
                            tile_rect = (col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE, TILE_SIZE // 2)
                    if CheckCollisionRecs(player_rect, tile_rect):
                        if (level[row][col] == TILE_STATE.TILE_LEVEL_END):
                            self.reach_level_end = True
                            break
                        if axis == 'X':
                            
                            if self.vx > 0: # Moving Right
                                self.x = tile_rect[0] - self.width
                            elif self.vx < 0: # Moving Left
                                self.x = tile_rect[0] + TILE_SIZE
                            self.vx = 0.0 
                            self.collided_with_x = True
                            
                        elif axis == 'Y':
                            if self.vy >= 0: # Falling (Hitting Ground)
                                self.y = tile_rect[1] - self.height
                                self.is_grounded = True 
                            elif original_vy < 0: # Jumping (Hitting Ceiling)
                                self.y = tile_rect[1] + TILE_SIZE
                                
                            self.vy = 0.0 
                            return
                
                        
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
    
    def reset(self):
        """Resets the player to their starting position."""
        self.x = self.start_x
        self.y = self.start_y

        self.vx = 0.0
        self.vy = 0.0

        self.is_grounded = False
        self.is_wall_sliding = False
        self.is_wall_jumping = False
        self.collided_with_x = False
        self.reach_level_end = False

        self.wall_jump_lock_timer = 0.0
        self.jumpTimeTimer = JUMP_TIME
        self.can_big_jump = False

        self.yap_timer = 0
        
        self.freshmen_fifteen_meter = 0
        
        self.is_sprinting = False
        self.sprint_timer = 0.0
        self.sprint_speed_multiplier = 1.0
        self.particles = None

        self.direction = Direction.RIGHT
        self.state = PLAYER_STATE.IDLE
        self.texture = self.idle_texture

        self.anim.last = 7
        self.anim.cur = 0
        self.anim.type = AnimationType.REPEATING
        self.anim.duration = .1
        self.anim.duration_left = self.anim.duration
        self.anim.sprites_in_row = 8
        self.anim.done = False
        self.frame = self.anim.frame(PLAYER_TILE_WIDTH, PLAYER_TILE_HEIGHT)

    def draw(self, is_hitbox_visible):
        """Draws the player at their world coordinates."""
        #DrawRectangle(int(self.x), int(self.y), int(self.width), int(self.height), BLUE) 
        draw_texture_pro(self.texture, self.frame, Rectangle(self.x - ((PLAYER_TILE_WIDTH / 3) + 5), self.y - PLAYER_TILE_HEIGHT / 2.2, PLAYER_TILE_WIDTH, PLAYER_TILE_HEIGHT), Vector2(0, 0), 0.0, WHITE)
        if self.is_sprinting:
            DrawRectangleLines(int(self.x), int(self.y)+ int(self.height) + 3,40, 6, BROWN)
            DrawRectangleGradientV(int(self.x), int(self.y)+ int(self.height) + 3,int(40 * self.sprint_timer / COFFEE_SPRINT_DURATION), 6, ORANGE, WHITE)
        if self.particles:
            self.particles.draw()
        if is_hitbox_visible:
            if self.state == PLAYER_STATE.SLIDING:
                DrawRectangleLines(int(self.x), int(self.y + self.height * 0.5), int(self.width), int(self.height * 0.5), RED)
            else:
                DrawRectangleLines(int(self.x), int(self.y), int(self.width), int(self.height), RED)
        draw_text(PLAYER_STATE.get_state(self.state),200,200,11, BLACK)
        draw_text(str(self.sprint_timer),int(self.x),250,11, BLACK)
        draw_text(str("is wall sliding: " + str(self.is_wall_sliding)),int(self.x),270,11, BLACK)
        draw_text(str("is grounded: " + str(self.is_grounded)),int(self.x),290,11, BLACK)

        if self.yap_timer > 0:
            draw_text(self.yap_message, int(self.x - (10* self.direction)),int( self.y - 10), 10, BLACK)
            DrawRectangleLines(int(self.x - 15), int( self.y - 20),140, 9, BLACK)
            DrawRectangleGradientV(int(self.x - 15), int( self.y - 20),int(140 * self.yap_timer / YAP_DURATION), 9, PURPLE, RED)
class Yapper:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.anim = Animation(0, 3, 0, 1, .2, .2, AnimationType.REPEATING, 0, 4)
        self.frame = self.anim.frame(YAPPER_TILE_WIDTH, YAPPER_TILE_HEIGHT)

    def update(self, delta_time):
        self.anim.update(delta_time)
        self.frame = self.anim.frame(YAPPER_TILE_WIDTH, YAPPER_TILE_HEIGHT)

    def draw(self, is_hitbox_visible, yap_texture):
        draw_texture_pro(yap_texture, self.frame, Rectangle(self.x, self.y, TILE_SIZE, TILE_SIZE), Vector2(0, 0), 0.0, WHITE)
        if is_hitbox_visible:
            DrawRectangleLines(int(self.x), int(self.y), TILE_SIZE, TILE_SIZE, PURPLE)
# --- Drawing and Camera Functions (Unchanged) ---
                
def draw_level(level, tile_floor_text, tile_half_text, tile_wall_text, level_end_texture, is_hitbox, TILE_ROWS, TILE_COLS, is_hitbox_mode):
    """Draws the solid tiles of the level map."""
    for row in range(TILE_ROWS):
        for col in range(TILE_COLS):
            tile_value = level[row][col]
            x = col * TILE_SIZE
            y = row * TILE_SIZE
            if tile_value == TILE_STATE.FLOOR:
                
                
                """ DrawRectangle(x, y, TILE_SIZE, TILE_SIZE, DARKGRAY)
                DrawRectangleLines(x, y, TILE_SIZE, TILE_SIZE, BLACK) """
                draw_texture_pro(tile_floor_text, Rectangle(0,0, tile_floor_text.width, tile_floor_text.height), Rectangle(x, y, TILE_SIZE,TILE_SIZE), Vector2(0,0), 0.0, WHITE)
                
            if tile_value == TILE_STATE.TILE_HALF:
                draw_texture_pro(tile_half_text, Rectangle(0,0, tile_half_text.width, tile_half_text.height), Rectangle(x, y, TILE_SIZE,TILE_SIZE //2), Vector2(0,0), 0.0, WHITE)
                """ DrawRectangle(x, y, TILE_SIZE, TILE_SIZE // 2, DARKGRAY)
                DrawRectangleLines(x, y, TILE_SIZE, TILE_SIZE // 2, BLACK) """

            if tile_value == TILE_STATE.TILE_WALL:
                draw_texture_pro(tile_wall_text, Rectangle(0,0, tile_wall_text.width, tile_wall_text.height), Rectangle(x, y, TILE_SIZE,TILE_SIZE), Vector2(0,0), 0.0, WHITE)
            
            if tile_value == TILE_STATE.TILE_LEVEL_END:
                draw_texture_pro(level_end_texture, Rectangle(0,0,level_end_texture.width, level_end_texture.height), Rectangle(x - TILE_SIZE, y - (2 * TILE_SIZE) + 20, TILE_SIZE*3,TILE_SIZE*3), Vector2(0,0), 0.0, WHITE)
                draw_ellipse(x + 20,y + 37,20,5,Color(42, 250, 87, 205))
                if is_hitbox:
                    draw_rectangle_lines(x,y,TILE_SIZE,TILE_SIZE, GREEN)
def draw_coffees(coffees, coffee_texture,is_hitbox_mode):
    for cx, cy in coffees:
        draw_texture_pro(coffee_texture, Rectangle(0, 0, 64, 64), Rectangle(cx,cy, TILE_SIZE, TILE_SIZE), Vector2(0, 0), 0.0, WHITE)
        if is_hitbox_mode:
            DrawRectangleLines(int(cx) + 8, int(cy) + 8, int(TILE_SIZE) - 16, int(TILE_SIZE) - 16, BLUE)

def draw_beers(beers, beer_texture,is_hitbox_mode):
    for cx, cy in beers:
        draw_texture_pro(beer_texture, Rectangle(0, 0, beer_texture.width, beer_texture.height), Rectangle(cx,cy, TILE_SIZE, TILE_SIZE), Vector2(0, 0), 0.0, WHITE)
        if is_hitbox_mode:
            DrawRectangleLines(int(cx) + 8, int(cy) + 8, int(TILE_SIZE) - 16, int(TILE_SIZE) - 16, BLUE)


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
    game_level, enemies, coffees, yappers, beers = parse_level(LEVEL_1, TILE_ROWS_LEVEL_1, TILE_COLS_LEVEL_1)
    tile_rows = TILE_ROWS_LEVEL_1
    tile_cols = TILE_COLS_LEVEL_1
    world_height = WORLD_HEIGHT_LEVEL_1
    world_width = WORLD_WIDTH_LEVEL_1
    level_num = GAME_LEVEL.ONE
    # Game State Variables
    # Player starts at TILE_SIZE * 2, TILE_SIZE * 2
    player = Player(TILE_SIZE * 2, TILE_SIZE * 12)
    player.startup() # Load player textures/animations
    score = 0
    game_state = GAME_STATE.TITLE
    next_state = GAME_STATE.OFFICIAL_ENROLLMENT
    time_left_in_level = LEVEL_ONE_DURATION
    time_left_before_decrement = DURATION_BEFORE_DECREMENT
    # --- Camera Initialization ---
    camera = Camera2D()
    camera.target = Vector2(player.x, player.y) 
    camera.offset = Vector2(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2) 
    camera.rotation = 0.0
    camera.zoom = 1.0
    is_hitbox_mode = False
    
    #textures
    scale_texture = load_texture('scale.png')
    beer_texture = load_texture("beer_texture.png")
    coffee_texture = load_texture(join('Items','coffee.png'))
    coffee_outline_texture = load_texture(join('Items','coffee_outline.png'))
    bg_texture = load_texture('backgroundFP.png')
    title_texture = load_texture('title_screen.png')
    acceptance_texture = load_texture('acceptance.png')
    level_one_end_texture = load_texture('level_1_end.png')
    official_enrollment_texture = load_texture('official_enrollment.png')
    montage_texture = load_texture('montage.png')
    level_end_texture = level_one_end_texture
    
    tile_floor_text = load_texture('tile_floor.png')
    tile_half_text = load_texture('tile_half.png')
    tile_wall_text = load_texture("tile_wall.png")
    yapper_texture = load_texture("yapper.png")

    #background shapes
    coffee_count_rect = Rectangle(SCREEN_WIDTH - 55, SCREEN_HEIGHT - 30, 50, 10)
    coffee_count_rect_color_one = Color(245, 138, 56, 100) 
    coffee_hud_bg_rect = Rectangle(SCREEN_WIDTH - 50, SCREEN_HEIGHT - 100, 40, 68)
    coffee_hud_bg_rect_color = Color(61, 13, 13, 120)
    background_rect = Rectangle(0,0, TILE_SIZE * tile_cols, TILE_SIZE * tile_rows)
    
    # --- Game Loop ---
    while not WindowShouldClose():
        
        delta_time = GetFrameTime()
        if IsKeyPressed(KEY_H):
            is_hitbox_mode = not is_hitbox_mode
        # --- Update ---
        match game_state:
            
            case GAME_STATE.TITLE:
                if IsKeyPressed(KEY_S):
                    game_state = GAME_STATE.INTRO_EMAIL
            
            case GAME_STATE.INTRO_EMAIL:
                if IsKeyPressed(KEY_S):
                    game_state = GAME_STATE.PLAYING
            
            case GAME_STATE.OFFICIAL_ENROLLMENT:
                if IsKeyPressed(KEY_S):
                    game_state = GAME_STATE.MONTAGE
            
            case GAME_STATE.MONTAGE:
                if IsKeyPressed(KEY_S):
                    world_width = WORLD_WIDTH_LEVEL_2
                    world_height = WORLD_HEIGHT_LEVEL_2
                    player.world_width = world_width
                    player.world_height = world_height
                    player.reach_level_end = False
                    game_state = GAME_STATE.PLAYING
                    level_num = GAME_LEVEL.TWO
                    player.x = PLAYER_WIDTH * 2
                    player.y = world_height - TILE_SIZE * 2
                    player.start_y = player.y
                    time_left_in_level = LEVEL_TWO_DURATION
                    time_left_before_decrement = DURATION_BEFORE_DECREMENT
                    tile_cols = TILE_COLS_LEVEL_2
                    tile_rows = TILE_ROWS_LEVEL_2
                    player.tile_rows = tile_rows
                    player.tile_cols = tile_cols
                    game_level, enemies, coffees, yappers, beers = parse_level(LEVEL_2, TILE_ROWS_LEVEL_2, TILE_COLS_LEVEL_2)
                    background_rect = Rectangle(0,0, TILE_SIZE * tile_cols, TILE_SIZE * tile_rows)
                pass
            
            case GAME_STATE.LOST:
                if is_key_pressed(KEY_R):
                    player.reset()
                    game_level, enemies, coffees, yappers, beers, time_left_in_level, time_left_before_decrement = get_level_params(level_num)
                    game_state = GAME_STATE.PLAYING
                pass
            
            case GAME_STATE.PLAYING:
                if IsKeyPressed(KEY_R):
                    player.reset()
                    game_level, enemies, coffees, yappers, beers, time_left_in_level, time_left_before_decrement = get_level_params(level_num)
                    game_state = GAME_STATE.PLAYING
                player.update(delta_time, game_level)
                for yapper in yappers:
                    yapper.update(delta_time)
                
                time_left_before_decrement -= delta_time
                
                if time_left_before_decrement <= 0:
                    if level_num == GAME_LEVEL.ONE:
                        time_left_in_level -= LEVEL_DURATION_DECREMENT
                    else:
                        time_left_in_level -= LEVEL_DURATION_DECREMENT + player.freshmen_fifteen_meter
                    time_left_before_decrement = DURATION_BEFORE_DECREMENT
                
                if time_left_in_level <= 0:
                    game_state = GAME_STATE.LOST
                
                if IsMouseButtonPressed(MOUSE_BUTTON_LEFT):
                    mouse_world_pos = GetScreenToWorld2D(GetMousePosition(), camera)
                    player.x = mouse_world_pos.x
                    player.y = mouse_world_pos.y
                if player.y > world_height:
                    player.reset()

                update_camera(camera, player, world_width, world_height, SCREEN_WIDTH, SCREEN_HEIGHT)

                # Check for coin collection
                """  collected_indices = player.check_collection(coins)
                if collected_indices:
                    for index in sorted(collected_indices, reverse=True):
                        coins.pop(index)
                        score += 10 """

                # Check for coffee collection
                if player.coffee_count < COFFEE_MAX:
                    collected_coffee_indices = player.check_collection(coffees)
                    if collected_coffee_indices:
                        for index in sorted(collected_coffee_indices, reverse=True):
                            coffees.pop(index)
                            player.coffee_count += 1
                
                beer_collected_indices = player.check_collection(beers)
                
                if beer_collected_indices:
                    for index in sorted(beer_collected_indices, reverse=True):
                        beers.pop(index)
                        if player.freshmen_fifteen_meter < 15:
                            player.freshmen_fifteen_meter += 3
                           
                if player.reach_level_end:
                    game_state = next_state

                    

            
        # --- Draw ---
        BeginDrawing()
        ClearBackground(SKYBLUE)
        match game_state:
            
            case GAME_STATE.TITLE:
                draw_texture_pro(title_texture, Rectangle(0,0,title_texture.width, title_texture.height), Rectangle(0,0,SCREEN_WIDTH,SCREEN_HEIGHT), Vector2(0,0), 0.0, WHITE)
                draw_text("PRESS S to START", SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 5, 30, WHITE)
            
            case GAME_STATE.INTRO_EMAIL:
                draw_texture_pro(acceptance_texture, Rectangle(0,0,acceptance_texture.width, acceptance_texture.height), Rectangle(0,0,SCREEN_WIDTH,SCREEN_HEIGHT), Vector2(0,0), 0.0, WHITE)
                draw_text("PRESS S to CONTINUE", SCREEN_WIDTH // 2 - 120, SCREEN_HEIGHT - 45, 24, WHITE)
            
            case GAME_STATE.MONTAGE:
                draw_texture_pro(montage_texture, Rectangle(0,0,montage_texture.width, montage_texture.height), Rectangle(0,0,SCREEN_WIDTH,SCREEN_HEIGHT), Vector2(0,0), 0.0, WHITE)
                draw_text("PRESS S to CONTINUE", SCREEN_WIDTH // 2 - 120, SCREEN_HEIGHT - 45, 24, WHITE)
                draw_text("THE FOLLOWING WEEKS. . .", 20, 40, 30, WHITE)
            
            case GAME_STATE.OFFICIAL_ENROLLMENT:
                draw_texture_pro(official_enrollment_texture, Rectangle(0,0,official_enrollment_texture.width, official_enrollment_texture.height), Rectangle(0,0,SCREEN_WIDTH,SCREEN_HEIGHT), Vector2(0,0), 0.0, WHITE)
                draw_text("PRESS S to CONTINUE", SCREEN_WIDTH // 2 - 120, SCREEN_HEIGHT - 45, 24, WHITE)
            
            case GAME_STATE.LOST:
                draw_text("YOU_LOST", SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, 10, RED)
            
            case GAME_STATE.PLAYING:
                # Start the 2D camera mode
                BeginMode2D(camera)
                
                #draw background before level
                draw_texture_pro(bg_texture,Rectangle(0,0,bg_texture.width,bg_texture.height), background_rect, Vector2(0,0), 0.0, WHITE)
                
                # 1. Draw the Level
                draw_level(game_level, tile_floor_text, tile_half_text,tile_wall_text, level_end_texture,is_hitbox_mode, tile_rows, tile_cols, is_hitbox_mode)
                for yapper in yappers:
                    yapper.draw(is_hitbox_mode, yapper_texture)

                # 2. Draw Collectibles
                draw_coffees(coffees, coffee_texture,is_hitbox_mode)
                draw_beers(beers, beer_texture, is_hitbox_mode)  

                # 4. Draw Player 
                player.draw(is_hitbox_mode)
                
                # End the 2D camera mode
                EndMode2D()
                
                # 5. Draw HUD (Drawn on screen, outside of BeginMode2D)
                
                debug_text = f"Grounded: {player.is_grounded} | Enemies: {len(enemies)}".encode('utf-8')
                DrawText(debug_text, 10, 10, 20, BLACK) 
                draw_text(str(level_num), 300, 20, 20, RED)
                draw_rectangle_rounded_lines_ex(coffee_count_rect, 2.0, 10,1.0,WHITE)
                draw_rectangle_rounded(coffee_count_rect, 2.0, 10,coffee_count_rect_color_one)
                draw_text("COFFEE",SCREEN_WIDTH - 50, SCREEN_HEIGHT - 30, 9, YELLOW)
                draw_texture_pro(coffee_outline_texture, Rectangle(1, 1, 62, 63), Rectangle(SCREEN_WIDTH - 45, SCREEN_HEIGHT - 65, 32, 32), Vector2(0, 0), 0.0, WHITE)
                draw_texture_pro(coffee_outline_texture,Rectangle(1, 1, 62, 63), Rectangle(SCREEN_WIDTH - 45, SCREEN_HEIGHT - 100, 32, 32), Vector2(0, 0), 0.0, WHITE)
                draw_text("Coffee Count:" + str(player.coffee_count), 0, 40, 10, WHITE)
                draw_rectangle_rounded(coffee_hud_bg_rect, 1.0, 5, coffee_hud_bg_rect_color)
                if player.coffee_count >= 1:
                    draw_texture_pro(coffee_texture,Rectangle(1, 1, 62, 63), Rectangle(SCREEN_WIDTH - 45, SCREEN_HEIGHT - 65, 32, 32), Vector2(0, 0), 0.0, WHITE)
                if player.coffee_count >= 2:
                    draw_texture_pro(coffee_texture,Rectangle(1, 1, 62, 63), Rectangle(SCREEN_WIDTH - 45, SCREEN_HEIGHT - 100, 32, 32), Vector2(0, 0), 0.0, WHITE)
                if level_num != GAME_LEVEL.ONE:
                    draw_texture_pro(scale_texture, Rectangle(0,0,scale_texture.width,scale_texture.height), Rectangle(SCREEN_WIDTH // 2 - (50), 20, 100, 100), Vector2(0,0), 0.0, WHITE)
                    draw_text("+" + str(player.freshmen_fifteen_meter) + " lbs", SCREEN_WIDTH // 2 - (22), 38, 14, RED  )
                draw_text("TIME_LEFT: " + str(time_left_in_level), SCREEN_WIDTH -160, 60, 15, RED)
                draw_text("TIME_LEFT before decrement: " + str(time_left_before_decrement), SCREEN_WIDTH -350, 90, 15, RED)
        EndDrawing()
    # --- De-Initialization ---
    CloseWindow()

if __name__ == "__main__":
    main()
