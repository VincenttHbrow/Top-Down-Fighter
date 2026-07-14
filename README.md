# Top-Down-Fighter

[Roadmap](ROADMAP.md)

Thank you to jsbueno on stackoverflow for helping solve performance issues!

Any mention of AI in this document or project has nothing to do with generative AI or LLMs.
In all likelihood it is referring to enemy behaviours.
This is a human-made game.

### Update Notes

##### V0.0.9 - Uncancellable animations
- Added a punch animation for the PC triggered with LMB
- Currently just knocks characters/objects back
- Player cannot move or turn when punch is being performed
- Animation frame now resets when animation is changed

##### V0.0.8 - Primitive enemy AI
- Added an enemy to the game.
- Currently, it just turns to face you and moves to keep distance.
- Functions properly with physics interactions between sprites
- Added fullscreen setting
- Added new spritesheet for enemy, currently just a copy of player spritesheet

##### V0.0.7 - Actual optimisation improvements
- More or less fixed frame drop while rotating map. Will have to test on lower end machine but the FPS is fairly consistent?
- Fixed bug where guy gets stuck on walls. It was leftover code from when all the movement stuff was in the player module.
- Simplified existing movement code.
- Entity centers no longer offset by half a tile, though that is easy enough to reintroduce.
- Clarified the data displayed in debug mode, including making hitboxes red.
- Added camera setting that allows display without the zoom & rotation effects, for debugging

##### V0.0.6 - Optimisation... improvements?
- Noticed on larger maps, drawing the whole map at once and then rotating was killing my FPS
- Spent like 3 hours rewriting the whole map drawing thing
- Didn't fix the performance issues, arguably made it worse
- Posted on stackoverflow, hopefully someone says something
- FML

##### V0.0.5 - Movement & Hitbox improvements
- Hitboxes no longer are altered in size by the direction of an object
- Character hitbox made smaller (1/2 of tilesize)
- Debug mode; currently only shows hitboxes but may do more in future
- Movement is now constant speed instead of being higher when moving diagonally
- Checks for wall collisions with the corners of the hitbox instead of center
- Moved the movement code around

##### V0.0.4 - Entity Systems
- Made an entity system to draw things (as it stands just the player sprite and a crate) on the map.
- Made sprites capable of being animated and rotating, as well as colliding
- Added "sprites" folder with little animated dude to walk around and a crate
- Will have to move some of the player movement stuff (collisions etc) to the entity class because of streamlining
- Added new tileset, looks better IMO
- Locked the mouse to the screen and hid it
- Added "esc" as exit shortcut
- Added ENTITYSIZE and ANIMATIONSPEED variables to settings, fairly self explanatory.

##### V0.0.3 - Tilesets
- Added link to the roadmap in the readme
- Tiles are now stored in and created from single tileset files.
- "Solid" tiles are now decided based on the first line in any given map file.
- Added folders "maps" and "tilesets" to contain (you guessed it) maps and tilesets.

##### V0.0.2 - Collisions
Main focus of this update is cleaning up the code, writing comments, and making collisions work.
- Moved much of the player input code and many variables to new player module
- Fixed (temporarily?) the map displaying at a different position than intended
- Added ROADMAP.md to keep track of and prioritise goals for the project
- Player can now move freely in four directions
- Player now collides with tiles marked solid

##### V0.0.1 - Engine Basics
This took me so long it's not even funny.
- main module contains main loop as well as essential pygame stuff (clock, display, etc.)
- settings module has easily accessible parameters like FPS and Resolution as well as RESOLUTIONMULT which is just for scaling the tiles correctly
- camera module is dedicated to making the game's perspective work. rotates and scales the map, draws entities, etc.
- testmap is just a txt that the map module uses for data
- wall and door tiles are placeholders, will eventually be tilesets
- I'm aware this is messy. I will clean it up tomorrow. Hopefully.