import cv2
import os
import numpy as np
from time import time
import keyboard
import pyautogui
import mss

dir_name = 'myData'

loop_time = time()

if not os.path.exists(dir_name): # if the dir dosen't exist create one
    os.makedirs(dir_name)
    new_dir_name = 0

else:
    new_dir_name = max(list(map(int,(os.listdir(dir_name))))) + 1 # get name of the dir with the max id and create new dir with id+=1
    
output_dir = os.path.join(dir_name,str(new_dir_name))
os.mkdir(output_dir)

data_collection = False
i = 0

sct = mss.mss()
mon = {'top': 197, 'left':544,'width':820,'height': 400} # 960-832/2,540-486/2, 820, 400)


def UI(text,display,x,y,color=(50,100,255)):
    # Draw black background rectangle
    cv2.rectangle(display, (x-15, y-50), (x+len(text)*17, y+20), (0,0,0), -1)
    cv2.putText(display,text,(x,y),cv2.FONT_HERSHEY_SIMPLEX,1,color,2)
    
while True:

    img = np.asarray(sct.grab(mon))#[:,:,0]
    
    display=np.copy(img)
    
    if not(data_collection):
        UI('Press "r" to record or "q" to exit',display,15,40)
        
    if keyboard.is_pressed("r"):
        data_collection = True
    
    if data_collection:   

        x_coord=pyautogui.position()[0]
        
        UI(f'Recording "p" -> pause: FPS = {round(1/(time()-loop_time))}   ',display,15,40,(100,255,100))
        UI(f'X coord = {x_coord}, FPS = {round(1/(time()-loop_time))}   ',display,15,100,(255,255,100))
        
        cv2.imwrite(os.path.join(output_dir,f'id={i}_xPos=_{pyautogui.position()[0]}_.jpg'),img)
        i+=1
        
        if keyboard.is_pressed("p"):
            data_collection=False
     
        
           
    
    cv2.imshow('Data Collection',display)
    loop_time = time()
    
    if cv2.waitKey(1) == ord('q'):
        cv2.destroyAllWindows()
        break
print('Done')
