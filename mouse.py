from pynput.mouse import Controller
import win32gui

mouse = Controller()


def getLT():
    hwnd = win32gui.FindWindow(None, 'NoxPlayer')
    if hwnd:
        rect = win32gui.GetWindowRect(hwnd)
        return rect
    else:
        print('NoxPlayer window not found!')
        exit()


if __name__ == '__main__':
    mouse = Controller()
    left, top, right, bottom = getLT()
    width = right - left
    height = bottom - top
    mouseLeft = mouse.position[0] - left
    mouseTop = mouse.position[1] - top
    print('clickPc(%f, %f)' %
          (mouseLeft / width, mouseTop / height))
