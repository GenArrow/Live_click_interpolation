import operator
import time
import sympy as sym
import cv2
import numpy as np
import pyautogui
import pynput
from pynput.mouse import Listener

img = np.zeros([1080, 1920, 1], dtype=np.uint8)

# img = np.zeros([720, 1080, 1], dtype=np.uint8)
img[:] = 255


def on_click(x, y, button, pressed):
    global apasat
    global clicked
    clicked = 0
    apasat = 0
    if pressed:
        apasat = 1
    else:
        apasat = 0

    if button == pynput.mouse.Button.left:
        clicked = 1
        time.sleep(0.03)
        clicked = 0


def interpolator(point_list):
    point_list = sorted(point_list, key=operator.itemgetter(0))
    x = sym.Symbol('x')

    Sz = len(point_list)
    sum1, sum2 = 0, 0
    A = [point_list[i][0] for i in range(Sz)]
    B = [point_list[i][1] for i in range(Sz)]

    for i in range(len(point_list)):
        prod = 1
        for j in range(len(point_list)):
            if j != i:
                prod = prod * (A[i] - A[j])

        sum1 = sum1 + (B[i] / prod) / (x - A[i])
        sum2 = sum2 + 1 / (prod * (x - A[i]))

    return sum1 / sum2


def plotter(point_list, img):
    Lm = interpolator(point_list)
    img[:] = 255
    queue = [point_list[0]]
    for valx in range(0, 1920, 35):
        try:
            fvalx = int(Lm.subs(x, valx))
            queue.append((valx, fvalx))
            cv2.line(img, pt1=queue[0], pt2=queue[1], color=(0, 0, 0, 0), thickness=2)
            queue.pop(0)
        except Exception:
            pass


with Listener(on_click=on_click) as listener:
    x = sym.Symbol('x')

    # for drawing while mouse clicked

    # apasat = 0
    # while True:
    #    print(pyautogui.position())
    #    cv2.imshow('draw', img)
    #    k = cv2.waitKey(1)
    #    if k == 27:
    #        break

    #    if apasat:
    #        posy = int(pyautogui.position()[1] // 1.8)
    #        posx = int(pyautogui.position()[0] // 3.2)
    #        img[posy - 2:posy + 2, posx - 2:posx + 2] = 150

    # apasat = 0
    # while True:
    #    cv2.imshow('draw', img)
    #    cv2.moveWindow('draw', 0, -30)
    #    k = cv2.waitKey(1)
    #    if k == 27:
    #        break
    #    if k == ord('c'):
    #        img[:] = 255
    #    if apasat:
    #        try:
    #            posy = pyautogui.position()[1]
    #            posx = pyautogui.position()[0]
    #            img[posy - 2:posy + 2, posx - 2:posx + 2] = 50

    #        except Exception:
    #            pass

    apasat = 0
    clicked = 0
    point_list = [(0, 1080)]
    while True:
        cv2.imshow('draw', img)
        cv2.moveWindow('draw', 0, -30)
        k = cv2.waitKey(1)
        if k == 27:
            break
        if k == ord('c'):
            img[:] = 255
            point_list = [(0, 1080)]

        if k == ord('z'):
            try:
                point_list.pop()
                plotter(point_list, img)
            except Exception:
                pass

        if clicked:
            try:
                posy = pyautogui.position()[1]
                posx = pyautogui.position()[0]
                img[posy - 2:posy + 2, posx - 2:posx + 2] = 50
                if (posx, posy) not in point_list:
                    point_list.append((posx, posy))

                time.sleep(0.1)
                plotter(point_list, img)

            except Exception:
                pass
