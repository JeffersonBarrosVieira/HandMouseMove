#Bibliotecas: 
#   opencv-python 
#   mediapipe 
#   pycaw

import cv2
import time
import numpy as np
from HandTrackingModule import handDetector
import math
import os

from pynput.mouse import Button, Controller
import tkinter as tk

root = tk.Tk()

#################################################
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
#################################################

mouse = Controller()

####################################
wCam, hCam = 640, 480
####################################


cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)
fps, pTime = 0, 0

detector = handDetector(detecConfidence=0.4)

finalizar, cond = False, 0

def attMouse(lmList, cond):
    if len(lmList) != 0:

        x1, y1 = lmList[4][1], lmList[4][2] # ponta do dedo polegar
        x2, y2 = lmList[8][1], lmList[8][2] # ponta do dedo indicador
        x3, y3 = lmList[20][1], lmList[20][2] # ponta do dedo midinho

        cx, cy = (x1+x2)//2 , (y1+y2)//2
        cx, cy = cx/640, cy/480 # pega o percentual de 0 a 1 dos centros

        # ifs para evitar que envie uma coordenada maior que o tamanho da tela, 1.1 por exemplo
        if cx > 1:
            cx = 1
        if cx < 0:
            cx = 0
        if cy > 1:
            cy = 1
        if cy < 0:
            cy = 0

        length1, length2 = math.hypot(x2-x1,y2-y1), math.hypot(x3-x1,y3-y1) # (distancia do dedão ao indicador), (distancia do dedao ao midinho)

        if length1<35 and cond == 0: #condição para executar o comando só uma vez ("pressionar")
            mouse.press(Button.left)
            cond = 1

        elif length1>35 and cond == 1: #condição para executar o comando só uma vez ("soltar")
            mouse.release(Button.left)
            cond = 0

        mouse.position = (screen_width*(1 - cx), screen_height*cy) # att posição do mouse

        if length2>300 : # verifica se a mão está "aberta" se a distancia do dedão ao midinho ultrapassou 300
            os.system('clear')
            print("Programa Finalizado!!")
            return (True, cond)
        else:
            return (False, cond)
    else:
        return (False, cond)





while True:
    
    success, img = cap.read()
    img = detector.findHands(img, draw=False)
    lmList = detector.findPosition(img, draw=False)
    
    finalizar, cond = attMouse(lmList, cond)

    if finalizar:
        break
        
    cv2.waitKey(1)
    time.sleep(0.02)
