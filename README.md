# Top-Down-Fighter

### Update Notes

##### V0.0.1 - Engine Basics
This took me so long it's not even funny.
- main module contains main loop as well as essential pygame stuff (clock, display, etc.)
- settings module has easily accessible parameters like FPS and Resolution as well as RESOLUTIONMULT which is just for scaling the tiles correctly
- camera module is dedicated to making the game's perspective work. rotates and scales the map, draws entities, etc.
- testmap is just a txt that the map module uses for data
- wall and door tiles are placeholders, will eventually be tilesets
- I'm aware this is messy. I will clean it up tomorrow. Hopefully.