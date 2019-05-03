

![alt text][logo]

[logo]: /shinyhunterlogo.png


## About
Shinyhunter is a bot that will search/hunt for shiny Pokémon in Pokémon Leaf Green and Fire Red. Shinyhunter uses the VisualBoyAdvance-1.8.0-beta3 emulator for this. 

A list of supported shiny Pokémon can be found [here](/shinyList.json).

---

## Setup
1. Download VisualBoyAdvance [here](http://www.emulator-zone.com/doc.php/gba/vboyadvance.html).

2. To use Shinyhunter we will need to change the default controls of VisualBoyAdvance. 

3. Go to: **Options > Joypad > Configure > 1**

Control | Mapping |
--- | --- |
Up| W
Down| S
Left| A
Right| D
Button A| Q
Button B| Backspace
Start| Enter

4. Change the video mode, go to: **Options > Video > x3**
5. Change the color mode, go to: **Options > Gameboy > Real Colors**
---
## Usage

1. Go to a grassy area with atleast 4 blocks of space (vertical)
2. Make sure your character is on the most northern block and facing north
3. Run the Python (shinyhunter.py) script. 
4. Profit. Shinyhunter will now look keep looking for shiny Pokémons. When a shiny is found the script will be executed, so the user can catch the shiny himself.
---


## Future features
* Detect which way the player is facing so the player does not have to face north when starting the script
* Detect when players Pokémon is low health and heal automatically
* Add more supported shiny Pokémons
* Add more advanced movements (currently we can only walk vertical)
* Add custom controls
---

## Tech stack
### [OpenCV-Python](https://pypi.org/project/opencv-python/)
For image manipulation/detection I use OpenCV-Python. By using OpenCV-Python we can get the color of a certain pixels. With the color we can decide if there is a shiny Pokémon or not.

### [scikit-learn](https://pypi.org/project/scikit-learn/) (OCR)
Because we need to read a lot of information of the screen I have made my own OCR. This is done with scikit-learn, using Bagging for the classifier and for preprocessing I use the Normalizer.

### [Directkeys](https://stackoverflow.com/questions/14489013/simulate-python-keypresses-for-controlling-a-game)
For the simulation of key input I use a slightly modified version of Directkeys.



