import win32gui

windowDimensions = {}

def callback(hwnd, extra):
    rect = win32gui.GetWindowRect(hwnd)
    x = rect[0]
    y = rect[1]
    w = rect[2] - x
    h = rect[3] - y

    if 'VisualBoyAdvance-' in win32gui.GetWindowText(hwnd) and '%' in win32gui.GetWindowText(hwnd):
        # print("Window %s:" % win32gui.GetWindowText(hwnd))
        # print("\tLocation: (%d, %d)" % (x, y))
        # print("\t    Size: (%d, %d)" % (w, h))
        win32gui.SetForegroundWindow(hwnd)
        print('Set focus to: ' + win32gui.GetWindowText(hwnd))

        global windowDimensions
        windowDimensions = {'top': y, 'left': x, 'width': w, 'height': h}

def findWindow():
    win32gui.EnumWindows(callback, None)
    return windowDimensions
