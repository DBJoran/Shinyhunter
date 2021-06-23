

![alt text][logo]

[logo]: /shinyhunterlogo.png


## About
Shinyhunter is a bot that will search/hunt for shiny Pokémon in Pokémon Leaf Green and Fire Red. Shinyhunter uses the VisualBoyAdvance-1.8.0-beta3 emulator for this. 

A list of supported shiny Pokémon can be found [here](/shinylist.json).

---

## Setup
1. Download VisualBoyAdvance [here](http://www.emulator-zone.com/doc.php/gba/vboyadvance.html).

2. Pip install all the Python dependencies

    `pip install -r requirement.txt`

3. To use Shinyhunter we will need to change the default controls of VisualBoyAdvance. 

4. Go to: **Options > Joypad > Configure > 1**

Control | Mapping |
--- | --- |
Up| W
Down| S
Left| A
Right| D
GBA A Button| Q

These are the default controls of Shinyhunter, if you'd like to use different controls you will have to change it in VisualBoyAdvance and in the **config.yaml** file.


5. Change the video mode, go to: **Options > Video > x3**
6. Change the render mode, go to: **Options > Video > Render Method > Direct 3D**
7. Change the color mode, go to: **Options > Gameboy > Real Colors**
---
## Usage

1. Go to a grassy area with atleast 4 blocks of space (vertical)
2. Run the Python (shinyhunter.py) script.
3. Profit. Shinyhunter will now look keep looking for shiny Pokémons. When a shiny is found the script will be executed, so the user can catch the shiny himself.
---


## Future features
* Add more supported shiny Pokémons
* Add more advanced movements (currently we can only walk vertical)
---

## Tech stack

### [Python 3.7](https://www.python.org/downloads/release/python-370/)

### [OpenCV-Python](https://pypi.org/project/opencv-python/)
For image manipulation/detection I use OpenCV-Python. By using OpenCV-Python we can get the color of a certain pixels. With the color we can decide if there is a shiny Pokémon or not.

### [scikit-learn](https://pypi.org/project/scikit-learn/) (OCR)
Because we need to read a lot of information of the screen I have made my own OCR. This is done with scikit-learn, using Bagging for the classifier and for preprocessing I use the Normalizer.

### [Directkeys](https://stackoverflow.com/questions/14489013/simulate-python-keypresses-for-controlling-a-game)
For the simulation of key input I use a slightly modified version of Directkeys.



