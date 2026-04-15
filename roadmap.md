Date: 2026/04/10, 1:45 p.m.
Goal
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