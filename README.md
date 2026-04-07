# Top-Down-Fighter

[Roadmap](ROADMAP.md)

### Update Notes

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