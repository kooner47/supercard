import win32gui
import win32api
import win32con
from pynput.mouse import Button, Controller
import time
import pyautogui
import cv2
from enum import Enum
import numpy as np
import random
import keyboard
import sys


class State(Enum):
    SPLASH = 1
    MENU = 2
    OPPONENT = 3
    QUARTER = 4
    QUICK_GAME = 5
    TAP_TO_CONTINUE = 6
    PICK = 7
    PICK2 = 8
    DONE_PICKS = 9
    WHEEL2 = 10
    WHEEL3 = 11
    WHEEL4 = 12


WINDOW_NAME = 'NoxPlayer'
RESOLUTION = (338, 628)

mouse = Controller()

FLAG = True


def getLT():
    hwnd = win32gui.FindWindow(None, WINDOW_NAME)
    if hwnd:
        return win32gui.GetWindowRect(hwnd)
    else:
        print('%s window not found!' % WINDOW_NAME)
        exit()


def getMatchCoords(im, template):
    res = cv2.matchTemplate(im, template, cv2.TM_CCOEFF_NORMED)
    loc = np.where(res >= 0.9)
    if not len(loc[0]):
        return
    return (loc[1][0], loc[0][0])


def getStateAndCoords():
    im = pyautogui.screenshot(region=(LEFT, TOP, WIDTH, HEIGHT))
    im = np.array(im)[:, :, ::-1]
    for img_name, img_template in IMG_TEMPLATES.items():
        coords = getMatchCoords(im, img_template)
        if coords:
            return State[img_name], coords
    return 'UNKNOWN', []


def swapToBronzesThenAutofill():
    def clickSwap():
        clickPc(0.381481, 0.890656, 0.2)

    # Deck editor
    clickPc(0.359259, 0.960239, 0.5)

    # NBA 1
    clickPc(0.200000, 0.373757, 0.2)
    clickSwap()
    clickPc(0.507407, 0.337972, 0.2)

    # NBA 2
    clickPc(0.400000, 0.369781, 0.2)
    clickSwap()
    clickPc(0.503704, 0.483101, 0.2)

    # NBA 3
    clickPc(0.592593, 0.369781, 0.2)
    clickSwap()
    clickPc(0.492593, 0.626243, 0.2)

    # NBA 4
    clickPc(0.807407, 0.373757, 0.2)
    clickSwap()
    clickPc(0.500000, 0.751491, 0.2)

    # WNBA 1
    clickPc(0.396296, 0.552684, 0.2)
    clickSwap()
    clickPc(0.507407, 0.337972, 0.2)

    # WNBA 2
    clickPc(0.600000, 0.546720, 0.2)
    clickSwap()
    clickPc(0.503704, 0.483101, 0.2)

    # Support 1
    clickPc(0.407407, 0.691849, 0.2)
    clickSwap()
    clickPc(0.507407, 0.337972, 0.2)

    # Support 2
    clickPc(0.618519, 0.689861, 0.2)
    clickSwap()
    clickPc(0.503704, 0.483101, 0.2)

    # Back
    clickPc(0.059259, 0.079523, 1)

    # Deck editor
    clickPc(0.359259, 0.960239, 0.5)

    # Autofill, Yes
    clickPc(0.270370, 0.938370, 0.2)
    clickPc(0.300000, 0.604374, 0.2)

    # Back
    clickPc(0.059259, 0.079523, 1)


def doActionForState(state, coords):
    global NUM_GAMES
    if state == State.SPLASH:
        click(*coords)
        return 3
    elif state == State.MENU:
        click(*coords)
        return 1
    elif state == State.OPPONENT:
        if NUM_GAMES >= 20:
            swapToBronzesThenAutofill()
            NUM_GAMES = 0
        click(*coords)
        NUM_GAMES += 1
        return 7
    elif state == State.QUARTER:
        clickPc(0.177778, 0.940239, 0.02)
        clickPc(0.325926, 0.940239, 0.02)
        clickPc(0.459259, 0.940239, 0.02)
        clickPc(0.596296, 0.940239, 0.02)
        clickPc(0.759259, 0.940239, 0.02)
        clickPc(0.907407, 0.940239, 0.02)
        return 0.5
    elif state == State.QUICK_GAME:
        for _ in range(5):
            clickPc(0.518519 + (random.random() - 0.5) * 0.01,
                    0.545817 + (random.random() - 0.5) * 0.01, 0.001)
        return 0.1
    elif state == State.TAP_TO_CONTINUE:
        clickPc(0.5, 0.5)
        return 0.8
    elif state == State.PICK or state == State.PICK2:
        x = 0.118
        y = 0.245
        rand = random.random()
        if rand < 0.25:
            for row in range(5):
                for col in range(5):
                    if random.random() < 0.5:
                        continue
                    clickPc(x + 0.188 * col, y + 0.127 * row, timeout=0.001)
        elif rand < 0.5:
            for col in range(5):
                for row in range(5):
                    if random.random() < 0.5:
                        continue
                    clickPc(x + 0.188 * col, y + 0.127 * row, timeout=0.001)
        elif rand < 0.75:
            for row in range(4, -1, -1):
                for col in range(4, -1, -1):
                    if random.random() < 0.5:
                        continue
                    clickPc(x + 0.188 * col, y + 0.127 * row, timeout=0.001)
        else:
            for col in range(4, -1, -1):
                for row in range(4, -1, -1):
                    if random.random() < 0.5:
                        continue
                    clickPc(x + 0.188 * col, y + 0.127 * row, timeout=0.001)
        return 1
    elif state == State.WHEEL2:
        click(*coords)
        return 2
    elif state == State.WHEEL3:
        click(*coords)
        time.sleep(2)
        click(*coords)
        return 2
    elif state == State.WHEEL4:
        clickPc(0.5, 0.5)
        time.sleep(2)
        clickPc(0.5, 0.5)
        return 1
    elif state == State.DONE_PICKS:
        clickPc(0.5000, 0.9422)
        return 1.2


def clickPc(xPc, yPc, timeout=0.05):
    click(xPc * WIDTH, yPc * HEIGHT, timeout)


def click(x, y, timeout=0.05):
    time.sleep(timeout)
    mouse.position = (LEFT + x, TOP + y)
    time.sleep(timeout)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
    time.sleep(timeout)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
    time.sleep(timeout)


def killer():
    global FLAG
    FLAG = False
    print('killer')


def main():
    num_unknowns = 0
    while FLAG:
        state, coords = getStateAndCoords()
        if state == 'UNKNOWN':
            time.sleep(0.5)
            num_unknowns += 1
            if num_unknowns >= 20:
                print('Received 20 unknowns in a row. Exiting.')
                exit()
            continue
        else:
            num_unknowns = 0
            if state != State.QUICK_GAME:
                print(state)
                if state == State.OPPONENT:
                    print('Starting match #%d.' % NUM_GAMES)
        timeout = doActionForState(state, coords)
        time.sleep(timeout)


if __name__ == "__main__":
    if len(sys.argv) >= 2:
        NUM_GAMES = int(sys.argv[1])
    else:
        NUM_GAMES = 1
    keyboard.add_hotkey('ctrl+shift+s', killer)
    print('Press ctrl+shift+s to kill the program.')
    IMG_TEMPLATES = {}
    for state in list(State):
        IMG_TEMPLATES[state.name] = cv2.imread('imgs/%s.jpg' % state.name)
    LEFT, TOP, RIGHT, BOTTOM = getLT()
    WIDTH = RIGHT - LEFT
    HEIGHT = BOTTOM - TOP
    print('Width=%d, Height=%d' % (WIDTH, HEIGHT))
    time.sleep(2)
    main()
