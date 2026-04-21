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