# NombrePendienteDeAprobacion

[GUL](https://github.com/guluc3m) project. Developed by [Patataman](https://github.com/Patataman) and [SeindElBardo](https://github.com/SeindElBardo).

This repository contains a 2D fighting game for 2 players.

Developed in Python using [Pygame](http://pygame.org) library.
Executable created with [Pyinstaller](http://www.pyinstaller.org/).


It has three screens:
- Start
- Character selection
- Fight

# Controls
Controls for each player
- Character selection:
-- "Space bar" for player 1
-- "Enter" for player 2
- Move Left:
-- "A" for player 1
-- "Left Arrow" for player 2
- Move Right:
-- "D" for player 1
-- "Right Arrow" for player 2
- Move Down:
-- "S" for player 1.
-- "Down Arrow" for player 2.
- Jump:
-- "W" for player 1.
-- "Up Arrow" for player 2.


Game code is organized in this folders:
- Root
 - Assets
 - Classes

# Root
  File *main.py*. Executes the game.
# Assets
  Contains files such as images, sounds, sprites sheets...
## Sprites (WIP)
Sprites are divided in two pieces, one for each orientation possible (right and left). Due to create sprites is a expensive job, each action is only composed by 4 frames.
## Characters (WIP)
To create a new character, it needs a sprite sheet, name and avatar.
# Classes
  Contains all .py that form the game.
  - *Functions.py*: Contains generic functions such as load images or create text.
  - *personajes.json*: Contains character list included in the game. .json has: Character name, path to character avatar and path to sprite sheet.
  - *Director.py*: Along Scene.py allows change scenes.
  - *Scene.py*: Contains all the different scenes that form the game (Start, Character selection and Fight).
  - *Player.py*: Contains all character representation, attributes and methods.



