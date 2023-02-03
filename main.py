from pyautogui import *
import pyautogui
import time
import keyboard
import win32api, win32con
import numpy as np
import cv2
from mss import mss 
from PIL import Image
from matplotlib import pyplot as plt

def click(x,y):
    win32api.SetCursorPos((x,y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0)
    time.sleep(0.01)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0)
    
bounding_blue = {'top': 200, 'left': 810-500, 'width': 300, 'height': 300}
bounding_red = {'top': 200, 'left': 810, 'width': 300, 'height': 300}
bounding_yellow = {'top': 200, 'left': 810+500, 'width': 300, 'height': 300}
sct = mss()
avg =[0,0,0,0]
iteracji = 0
odpowiedz = []
nic=0

while keyboard.is_pressed('/') == False:
    #print("working")
    print("mouse = ",pyautogui.position())
    sct_img_blue = sct.grab(bounding_blue)
    sct_img_red = sct.grab(bounding_red)
    sct_img_yellow = sct.grab(bounding_yellow)
    #cv2.imshow('screen', np.array(sct_img))
    #plt.imshow(sct_img)
    #plt.show()
    odpowiedzi_prawo = 0
    odpowiedzi_lewo = 0
    for i in range(0,3):
        if i==0:
            sct_img=sct_img_blue
        elif i==1:
            sct_img=sct_img_red
        else:
            sct_img=sct_img_yellow
        average_color_row = np.average(sct_img, axis=0)
        average_color = np.average(average_color_row, axis=0)
        avg[i] = (avg[i] +average_color)/2
        
        #print("avg now = ", average_color)
        #print("diff check = ", average_color-avg[i])
        
        if any(average_color-avg[i] > 0.5):
            if i==0:
                print("blue")
                odpowiedz.append("Blue")
                odpowiedzi_lewo = odpowiedzi_lewo+1
            elif i==1:
                print("red")
                odpowiedz.append("Red")
                odpowiedzi_lewo = odpowiedzi_lewo+1
                odpowiedzi_prawo = odpowiedzi_prawo+1
            else:
                print("yellow")
                odpowiedz.append("Yellow")
                odpowiedzi_prawo = odpowiedzi_prawo+1
                
            print("avg now = ", average_color)
            print("avg avg = ", avg[i])
            print("diff = ", average_color-avg[i])

        #if odpowiedzi_lewo>1:
        #    if all(average_color-avg[0] > average_color-avg[1]):
        #        print("poprawna blue")
        #    else:
        #        print("poprawna red")   
        #if odpowiedzi_prawo>1: 
        #    if all(average_color-avg[1] > average_color-avg[2]):
        #        print("poprawna red")
        #    else:
        #        print("poprawna yellow")    
        
    if odpowiedzi_lewo==0 and odpowiedzi_prawo==0 and iteracji > 20:
        nic=nic+1
        if nic > 4:
            print("algorytm odpowiadania")
            odpowiedz.clear()
            nic=0
            
    time.sleep(0.7)
    iteracji = iteracji + 1
    
    if iteracji <20:
        odpowiedz.clear()
        
    print("odpowiedz",odpowiedz)
                          