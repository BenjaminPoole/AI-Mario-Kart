import cv2
import os
import numpy as np
from time import time
import pyautogui
import keyboard

loop_time = time()

i=0
start_recording=False
while True:

    img= np.array(pyautogui.screenshot(region=(200,100, 820, 400))) ## Dolphin Dimensions = 832, 486
    img=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    
    
    #cv2.putText(img,f'FPS: {round(1/(time()-loop_time))}',(15,40),cv2.FONT_HERSHEY_SIMPLEX,1.2,(0,0,255),2)
    cv2.imshow('Computer Vision',img)
    
    w=False
    a=False
    s=False
    d=False
    
    if keyboard.is_pressed("r"):
        if start_recording==False:
            print('Started Recording')
            print('=============================================')
        start_recording=True
        
        
    if start_recording:
        if keyboard.is_pressed("w"):
            w=True
        if keyboard.is_pressed("a"):
            a=True
        if keyboard.is_pressed("s"):
            s=True
        if keyboard.is_pressed("d"):
            d=True

        #cv2.imwrite(os.path.join('output',f'id={i}_f={f}_b={b}_l={l}_r={r}_.png'),img)
        cv2.imwrite(os.path.join('output5',f'id={i}_wasd={int(w)}{int(a)}{int(s)}{int(d)}_.png'),img)
        i+=1
    
    #print(f'FPS: {round(1/(time()-loop_time))}')
    loop_time = time()
    
    if cv2.waitKey(1) == ord('q'):
        cv2.destroyAllWindows()
        break
print('Done')
