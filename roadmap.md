Date: 2026/04/10, 1:45 p.m.
**Goal**. 
Allow for player to sprint 
Implementation
Go to player update function and put in an amplifier variable that changes with a key press and affects player input (mulitplier)
Technical Plan/Credit: same implementation of dodge/dash in my mid semester project game with the velocity multiplier
Content Credit: none
Commit message feat(sprint): add player input listener for velocity multiplier (sprinting)
Next/TO DO :
investigate double jump feature
investigate flappy.py to see how double jump is implemented

Date: 2026/04/10, 2:15 p.m.
Goal
Allow for player to shoot and render a bullet (no collision yet) 
Implementation
Copy and paste bullet class from 12.Gun_fight.py, put a bullet field in the player class, call update and draw on it in player update and draw, using player listener for left click
(mulitplier)
Technical Plan/Credit: same implementation of bullet in 12.Gun_fight.py. Sourced from that file
Content Credit: 12.Gun_fight.py
Commit message feat(bullet shoot and rendering): add player input listener for shooting that renders and shoots a bullet (no collision yet)
Next/TO DO :
investigate making the bullet collide with enemies and do damage

Date: 2026/04/15, 1:10 p.m.
Goal
Refactor code for ease of parsing my main project file
Implementation: took constants and put them in settings.py
Commit message: refactor(Global Constants) put constants in settings.py file
next to do more refactoring to set up code base

Date: 2026/12/15, 1:18 p.m.
Goal
Refactor code for ease of parsing my main project file
Implementation: added game_enums.py file
Commit message: refactor(Game enums) set up and added game_enums file for later use
next to do more refactoring to set up code base

Date: 2026/04/15, 1:25 p.m.
Goal
Allow for rendering of player hitbox for ease of development
Implementation
set a field in player fields: is_hitbox_visible
check this in the player draw function, if true draw a red box around the player hitbox
Technical plan / credit : same implementation as in pang of the damned (mid semester project)
Commit message: feat(hitbox drawing for player) added listener for key h for hitbox rendering for player
Next to do:
implement slide mechanic which should make the player hitbox tinier, and should additionally cause them to decelerate. May have to look into implementing a player state machine because sliding should likely set the player into a sliding state

Date: 2026/04/15, 1:40 p.m.
Goal
Add a player state field and transition helper function to transition between player states
Implementation
set a field in player fields: self.player_state, add player_state enum to game_enums.py,
Technical plan / credit : same implementation as in pang of the damned (mid semester project)
Commit message: feat(game_state and transition helper method) changed game_enums and final_project.py player class to support states
Next to do:
decided that sprinting doesn't need to be a state so will implement that simply as a flag

Date: 2026/04/15, 2:20 p.m.
Goal
Add is sprinting field to player and use that to change the speed at which the player moves
set a field in player fields: self.is_sprinting,
Technical plan / credit : basically refactoring the sprint mechanic from before
Commit message: refactor( changed final_project.py player init and update that uses sprint flag)
Next to do:
will try and implement sliding mechanic

Date: 2026/04/15, 2:31 p.m.
Goal
Get rid of bullet class from lab 09 as this game will not include the player bullet (cleaning up leftover)
Technical plan / credit : none deleted old code
Commit message: refactor( got rid of old bullet mechanic from lab09)
Next to do:
will try and implement sliding mechanic but may again have more refactoring

Date: 2026/04/20, 6:30 p.m.
Goal
Get basic anim state set up, just such an idle animation is displayed
Implementation
Animation state file copied from Mid semester project, player state, player frame, and player texture added to player class
Technical Plan/Credit: same implementation of mid semester project
Content Credit: https://monopixelart.itch.io/character-pack/download/eyJpZCI6MjkxMjQ1NywiZXhwaXJlcyI6MTc3NjcyMjc4Nn0%3d%2eowqBwbVFL%2fr7%2fvw9ARcBlW9Sxgs%3d
Commit message feat(): add player idle animation
Next/TO DO :
add player slide animation

Date: 2026/04/20, 8:15 p.m.
Goal
get running animation setup
Implementation
Technical Plan/Credit: same implementation of mid semester project
Commit message feat(): add player running animation
Next/TO DO :
add player slide animation


Date: 2026/04/20, 8:58 p.m.
Goal
Get player slide animation to work along with player input to cause slide to happen when player is in the run state
Implementation
had to go back and change the order of input listeners in the running state, additionally had to make it such that three different animations occurred while sliding because the texture pack came with three different ones for that so kinda a mini transition state in slide update
Technical Plan/Credit: same implementation of mid semester project
Commit message feat(): add player slide animation and slide activation (no hitbox adjustment yet)
Next/TO DO :
add htibox management for sliding

Date: 2026/04/20, 8:58 p.m.
Goal
create a function to determine if the player head will collide upon stopping the slide
copied code from handle_tile_collision but slightly altered where it checks if a collision would happen with the normal collision box and the slide collision box, if there is an xor of these we know that we need to keep sliding this is important for the slide mechanic later as outlined by this forum post
Technical Plan/Credit: https://forum.gamemaker.io/index.php?threads/how-would-i-make-a-sliding-mechanic-in-my-2d-platformer-game.117854/

"Slide state: moves forward until a timer hits zero, you have a smaller hitbox so you can fit under things. It checks if you would get stuck if you would stop sliding, and if so extends the counter a little bit (so sliding will keep going until you won't get stuck when it ends)"

Commit message feat(): add xor collision detection for sliding mechanic extender
Next/TO DO :
actually change hitbox for sliding mechanic, and create a tile that can be slid under but not ran under

Date: 2026/04/20, 10:12 p.m.
Goal
Get a block which is half tile height such that I can slide under it but not run through at normal height
Implementation
Created a new tile type corresponding to 4, where it is a half tile size, made it so the parser and collision methods treat it differently half height and currentyl the player can slide under it but not run through
Technical Plan/Credit: intuited it
Commit message feat(): add half height tiles
Next/TO DO :
make it so the player doesnt glitch when they stop sliding underneath one of these tiles, ie make the slide continue until they are out of a slide area

Date: 2026/04/20, 10:25 p.m.
Goal
Fix glitch where player may stand up while underneath sliding blocks
Implementation
before we transition to idle, we call check the xor collision funciton i made earlier
Technical Plan/Credit: kind of what https://forum.gamemaker.io/index.php?threads/how-would-i-make-a-sliding-mechanic-in-my-2d-platformer-game.117854/ this said but with my own workaround using the code for collision already present
Commit message feat(): making it such that slide lasts atleast necessary time to prevent standing up underneath slide blocks
Next/TO DO :
look into variable jump height mechanics

Date 2026/04/21, 12:06 Am
Goal:
make it such that player is able to have a variable jump height dependent on how long they hold down the space bar
Implementation
player now stores a:
self.can_big_jump
self.jumpTimeTimer

input for jumping is now held by a utility method called handle jump input:
if IsKeyPressed(KEY_SPACE) and self.is_grounded:
            self.is_grounded = False
            self.vy = JUMP_VELOCITY
            
            self.can_big_jump = True
            self.jumpTimeTimer = JUMP_TIME
        if IsKeyDown(KEY_SPACE) and self.can_big_jump:
            if self.jumpTimeTimer > 0:
                self.vy = JUMP_VELOCITY
                self.jumpTimeTimer -= dt
            else:
                self.can_big_jump = False
basically allows for the extesion of the application of the jump velocity until a timer runs out and then holding it down doesn;t do anything anymore
Technical plan/ credit: watched this video:
https://www.youtube.com/watch?v=avtm_F9HU3c&t=32s
copied the code for the jump handling here(found in the comment section of the youtube video):
https://github.com/ProjectMarzDev/Knight-Game/blob/main/Knight%20Game/knight.cpp
Commit message: feat(implemented variable jump heights)
Next To do:
make it such that jump is animated

Date: 2026/04/21, 1:27 a.m.
Goal
Get jumping animation to work
Implementation
simply loaded in jump animation, made it load in with proper fields like oneshot and frames being right number
Technical Plan/Credit: intuited it
Commit message feat(): add jump animation
Next/TO DO :
explore how to do coffee speed boost

Date 2026/04/21 2:21 PM
Goal
Implement coffee collectible, sprite, and collection
Implementation: created a new TILE_COFFEE = 5, in parse level i added a coffees list coffees = []

if the newlevel[r][c] = Tile coffee we append a coffee to the list

parse level now returns coffees and no longer collectibles coins are now separate from collectibles

check collection was also refactored to make collection hitbox more streamlined and also reusable for any type of collectible

Also utilized a sprite from online for the coffee draw function of draw texture pro

Technical plan/credit: utilized pre-existing collection methods from coins

commit message: feat(added coffee collectible with sprite and collection/collision)
Next TO/DO:
implement coffee collection giving the player a bankable speed boost (can be used for later)

Date 2026/04/22 2:37 PM
Goal
Make it so that collecting coffee increases coffee count and then player can press left-shift sprint to activate caffeinated mode which multiplies left and right movement speed
Implementation: 
collection of coffee items checks if player coffee count < COFFEE COUNT
in handle left and right input, check if player is pressing left shift and coffee count is > 0 and player isnt already sprinting, if so set sprinting to true and increment sprint timer
Then every update call will call check and handle speed boost which increases sprint speed multiplier and while the player is sprinting decrement timer until reaches zero and from then on speed boost will be 1.0

Technical plan/credit: no help, basically used same thing from dodge in mid semester project

commit message: feat(added functionality of coffee feature to make player caffeinated (horizontal speed multiplier))
Next TO/DO:
create visual effect for when you are caffeinated 

Date 2026/04/23 4:08 PM
Goal
Refactor tiles to use an enum
Implementation: 
self explanatory

commit message: refactor(tiles now use enum)
Next TO/DO:
try and figure out wall slide mechanic

Date 2026/04/22 4:44 PM
Goal
successfully detect if the player is wall sliding or not
Implementation: 
after checking collisions we check if the player has the three conditions met:
1. they are inputting key A or key D
2. they are not grounded
3. horizontal velocity is 0

These three ensure that the player is pressing up against a wall and then we set that flag to true

Technical plan/credit: got the flags and general structure from https://gist.github.com/bendux/b6d7745ad66b3d48ef197a9d261dc8f6, but had to use my own logic for detection as they use a overlap method with a wall layer would require a whole restructuring to match their method so just doing my own

commit message: feat(added detection of when the player should be wallsliding)
Next TO/DO:
get the player to actually slide when pressing against the wall in the air


Date: 2026/04/27, 9:09 p.m.
Goal
Get the player to slide on walls, and also be able to wall jump
Implementation:
Player now has a wall sliding state for the animation, in addition to a flag, a wall jump lock timer and a wall jump flag. Wall slide and jump Global constants are defined in the settings.py. Detection for wall sliding is the same before, and now sets the player in the wall sliding state. When the player is wall sliding, the affect of gravity is halved in this line if self.check_wall_slide():
            self.is_wall_sliding = True
            self.transition(PLAYER_STATE.WALL_SLIDING)
            self.y -= self.vy * delta_time * 0.5

we do this in this line because this check can not properly occur before checking tile collision on the x axis.

When play is in state wall sliding, the input for handling wall jump input occurs, wherein if the player presses the space key the wall jump lock timer is set which locks the player from initiating input from the left and right keys so the player can actually experience proper x axis movement, and additionally there vy is increased and set to wall jump power global constant. Until this timer runs out at the beginning of the update function the player x movement is locked to get the wall jump
Technical Plan/Credit: 

https://gist.github.com/bendux/b6d7745ad66b3d48ef197a9d261dc8f6

additionally I DID utilize chatGPT in integrating my approach, i did not have it generate code, but I did ask clarifying questions like "what is the purpose of the jump lock timer and why was the detection for is wall sliding off (it did point me in the right direction with respect to this because the legacy check utilized the key press "a" or "d", but needed to also use player direction)


Commit message: feat() added player wall slide, and wall jump
Next/TO DO : look into building the structure of the first tutorial level


Date: 2026/04/28, 12:47 p.m.
Goal
Refactor movements, constants, and level 1 design to get a working tutorial level that demonstrates key features
Implementation
refactored constants to make it such that wall jump doesnt allow you to infinitely ascend, only 3 blocks wide, sliding is more fluid.
Technical Plan/Credit: intuited it
Commit message refactor(created first tutorial level and adjusted constants for movement (fine tuning))
Next/TO DO :
make coffee boost indicator


Date: 2026/04/29 2:00 PM
Goal:
implement particle effects for coffee boost
Implementation:
player now stores particles and when the coffee boost is activated particles are generated at that position
Technical plan/credit:
particles: https://github.com/nas-programmer/raylib_projects/blob/main/Particle%20System/main.cpp
https://stackoverflow.com/questions/6339057/draw-transparent-rectangles-and-polygons-in-pygame
First link for particle and particle management
second link for color management and getting it to fade
Commit message feat(implemented particles for coffee boost)
Next to do:
coffee boost meter bar and coffee collection HUD

Date: 2026/04/29 2:20 PM
goal fix wall slide mechanic because before were able to keep wall sliding when you werent supposed to
Implementation:
set a flag that checks if a collision happened this frame on the x axis and added that to check wall slide
Technical plan credit:
asked ai to diagnose the issue, it gave a solution involving checking the tile next to the player but then I realized that we can just set a flag with the prexisting collision function and just use that way simpler
Commit message (debug): fixed wall slide mechanic
Next to do:
coffee boost meter bar and coffee collection HUD

Date: 2026/04/30 2:40 PM
implement coffee boost meter
Implementation:
little bar that renders underneath player that decreases as the sprint timer goes donwn
Technical plan credit:
same thing i did in mid semester project for the dash indicator
Commit message (feature): coffee boost meter
Next to do:
coffee collection HUD

Date: 2026/04/30 7:59 PM
implement coffee collection HUD
Implementation:
used textures from coffe, and made it drawn outside camer
Technical plan credit:
intuitive but used google color picker
Commit message (feature): coffee collection HUD
Next to do:
pick textures for level one

Date: 2026/04/30 8:35 PM
Implemented background
Implementation:
used ai to generate an image of an image i found online and then made the image drawn with draw texture pro to fit entire level width and height
Technical plan credit:
chatgpt google search of colgate images
Commit message (feature): background implemented
Next to do:
pick textures for tiles

Date: 2026/04/30 9:52 PM
Implemented textures for tiles
Implementation:
just asked ai for textures, and then adjusted colors in preview
Commit message (feature): textures implemented for tiles
Next to do:
implement intro screen and game state management

Date: 2026/04/30 10:41 PM
Implemented Game state management and title screen
Implementation:
utilized match case for game state update and draw
Technical plan / credit:
Same thing i did for project 1
Commit message (feature): title screen and better game state management with match case
Next to do:
implement intro dialogue

Date: 2026/05/1 1:58 AM
Implemented end condition for level One with montage to next stage
Implementation:
Created a new tile that sets a flag upon collision to change game state
Technical plan / credit:
animations and textures from chatgpt more in resources or wherever i put the ai stuff
Commit message (feature): completed level one
Next to do:
Create Level Two


Date: 2026/05/1 2:09 PM
Implemented timer condition for end state
Implementation:
store a timer variable that decrements by a fixed amount after a certain amount of time is passed and this decrement, assuming it is not level_one, is increased by the freshmen 15 meter which is a field in the player class
Technical plan / credit:
intuited it, not that complicated, similar to jumpTimeTimer from earlier
Commit message (feature): level timer implementation with lose state timer <= 0
Next to do:
make this timer look pretty and the you lost screen and resetting a level

Date: 2026/05/1 2:40 PM
moved level information in levels.py and refactored final_project.py to utilize this new file which stores everything
Implementation:
refactoring, kept running and finding errors, going to the line with command click and replacing old constants either with local variables or arguments
Technical plan / credit:
refactoring not much technicality
Commit message (refactor): moved level data into own file for ease of use for levels 2 and 3
Next to do:
start making level 2 to implement freshmen 15 display

Date: 2026/05/1 4:07 PM
fixed collision issue where jumping between intersection of two blocks from beneath shot the player up between
Implementation:
Store the original vy before loop because you want to use this before it gets changed by a collsion to know if the player should go up or below a block
Technical plan / credit:
Spent like an hour trying to figure it out by myself so I asked ai and it was literally a two line fix
Commit message (debug):fixed jumping between two blocks from beneath bug
Next to do:
start making level 2 to implement freshmen 15 displa

Date: 2026/05/1 4:21 PM
created level 2 template
Implementation:
copied level one and made it twice as big
Technical plan / credit:
simple copy and paste with name changing
Commit message (feature): created level 2 and 3 template
Next to do:
start making level 2 to implement freshmen 15 display, and also have guy that makes you wait if you collide with him and makes you talk to him

Date: 2026/05/1 5:53 PM
Goal
Implement “yapper” NPC that temporarily locks the player and displays dialogue upon interaction
Implementation:
Added TILE_YAPPER to level map and updated parse_level to instantiate Yapper objects at those tile positions while keeping the tile for collision detection.
Created Yapper class with animation state using anim.py
in handle_tile_collision added detection for TILE_YAPPER that triggers a yap interaction sets player.yap_timer to YAP_DURATION Removes tile sets to AIR to prevent repeated triggering player update now checks yap_timer while yap_timer > 0 player input is disabled no movement or jumping timer decrements each frame until player regains control by dt player draw renders a dialogue bar and message above the player while yap_timer is active, along with a visual timer bar
Technical plan/credit:
built on existing tile parsing system and collision handling reused nimation system from player for NPC animation. General structure mix of tiles and objects like coffee and tile solid or whatever

Commit message: feat(yapper npc interaction and animation): added NPC that locks player movement and displays dialogue on collision

Next/TO DO:
implement beer and salad collectible

Date: 2026/05/1 6:30 PM
Goal: implement beer collection which affects freshmen 15 meter
Implementation:
literally same thing as coffee just changes different fields
Technical plan / credit:
got sprite on google search will list later trying to rush rn
Commit message (feature): beer collection and freshmen 15 meter incrementation
Next to do:
display for freshmen 15 meter
level 2 design layout
level 3 design layout

Date: 2026/05/1 6:51 PM
Goal: implemented Freshmen 15 scale display and hud
Implementation:
literally just drawing fields available
Technical plan / credit:
got sprite on google search will list later trying to rush rn
Commit message (feature): freshmen fifteen meter HUD display
Next to do:
level 2 design layout
level 3 design layout

Date: 2026/05/1 7:52 PM
Goal: implemented player reset and level reset
Implementation:
for player reset, just make fields as they were at start of level, for level reset, call parse level in a new function called get fields and return all appropriate starting fields for level and set them
Technical plan / credit:
seems intuitive, but it took me over an hour to get all the fields set appropriately 
Commit message (feature): appropriate level and player reset
Next to do:
level 2 design layout

Date: 2026/05/2 2:52 PM
Goal: Finished level 2
Implementation:
just placed appropriate tiels
Technical plan / credit:
none
Commit message (feature): level 2 implemented
Next to do:
sound effects
refactoring
transition state animations

