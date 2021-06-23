import ctypes
import time

# direct inputs
# source to this solution and code:
# http://stackoverflow.com/questions/14489013/simulate-python-keypresses-for-controlling-a-game
# http://www.gamespp.com/directx/directInputKeyboardScanCodes.html

codes = { 
    'q': 0x10, 
    'w': 0x11, 
    'e': 0x12, 
    'r': 0x13, 
    't': 0x14, 
    'y': 0x15, 
    'u': 0x16, 
    'i': 0x17, 
    'o': 0x18, 
    'p': 0x19, 
    'a': 0x1E, 
    's': 0x1F, 
    'd': 0x20, 
    'f': 0x21, 
    'g': 0x22, 
    'h': 0x23, 
    'j': 0x24, 
    'k': 0x25, 
    'l': 0x26, 
    'z': 0x2C, 
    'x': 0x2D, 
    'c': 0x2E, 
    'v': 0x2F, 
    'b': 0x30, 
    'n': 0x31, 
    'm': 0x32,
    }

SendInput = ctypes.windll.user32.SendInput

# C struct redefinitions 
PUL = ctypes.POINTER(ctypes.c_ulong)
class KeyBdInput(ctypes.Structure):
    _fields_ = [("wVk", ctypes.c_ushort),
                ("wScan", ctypes.c_ushort),
                ("dwFlags", ctypes.c_ulong),
                ("time", ctypes.c_ulong),
                ("dwExtraInfo", PUL)]

class HardwareInput(ctypes.Structure):
    _fields_ = [("uMsg", ctypes.c_ulong),
                ("wParamL", ctypes.c_short),
                ("wParamH", ctypes.c_ushort)]

class MouseInput(ctypes.Structure):
    _fields_ = [("dx", ctypes.c_long),
                ("dy", ctypes.c_long),
                ("mouseData", ctypes.c_ulong),
                ("dwFlags", ctypes.c_ulong),
                ("time",ctypes.c_ulong),
                ("dwExtraInfo", PUL)]

class Input_I(ctypes.Union):
    _fields_ = [("ki", KeyBdInput),
                 ("mi", MouseInput),
                 ("hi", HardwareInput)]

class Input(ctypes.Structure):
    _fields_ = [("type", ctypes.c_ulong),
                ("ii", Input_I)]

# Actual functions
def PressKey(hexKeyCode):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput( 0, hexKeyCode, 0x0008, 0, ctypes.pointer(extra) )
    x = Input( ctypes.c_ulong(1), ii_ )
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

def ReleaseKey(hexKeyCode):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput( 0, hexKeyCode, 0x0008 | 0x0002, 0, ctypes.pointer(extra) )
    x = Input( ctypes.c_ulong(1), ii_ )
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

# https://www.reddit.com/r/learnpython/comments/22tke1/use_python_to_send_keystrokes_to_games_in_windows/
"""
Simulates a keypress. The string thats passed to the function will be used to obtain the hex code from the dictionary.

Parameters
----------
key : string
    The key you want to press as a string, if you want to press A you pass the string 'A'.
"""
def keyPress(key):
    key = key.lower()
    hexKeyCode = codes[key]

    PressKey(hexKeyCode)
    time.sleep(.05)
    ReleaseKey(hexKeyCode)
