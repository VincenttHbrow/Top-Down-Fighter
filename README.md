# Top-Down-Fighter

[Roadmap](ROADMAP.md)

### Update Notes

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