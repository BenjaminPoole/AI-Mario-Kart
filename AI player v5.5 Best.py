import cv2
import numpy as np
from time import time
import pydirectinput
import keyboard
from tensorflow.keras.models import load_model
import mss
from os.path import join
import matplotlib.pyplot as plt

#model = 'v5.2_(200, 410, 3)_new_model_more_training.h5'
model = 'v5.4_epoch=18.h5'
model_path = join('models','v5.4_color_augmentation_YUV',model)

model = load_model(model_path)
img_size = (410,200)


autonomous = False

sct = mss.mss()
mon = {'top': 197, 'left':544,'width':820,'height': 400} # 960-832/2,540-486/2, 820, 400)

drive = True
mean_fps = []


while True:
    old_time = time()

    img = np.asarray(sct.grab(mon))
    


    
    if keyboard.is_pressed("m"):
        autonomous = True
        if drive:
            pydirectinput.keyDown('g',_pause=False)
    
    if keyboard.is_pressed("c"):
        autonomous = False
        pydirectinput.keyUp('g',_pause=False)
        
    if keyboard.is_pressed('r'):
        drive = True
        pydirectinput.keyDown('g',_pause=False)
        
    elif keyboard.is_pressed('t'):
        drive = False
        
    if autonomous:

        
        x = 130
        y = 200
        #cv2.rectangle(img, (x, y), (x+360, 400), (0,0,0), -1)
        
        img=cv2.resize(img,img_size)
        
        #img=cv2.cvtColor(img,cv2.COLOR_BGRA2RGB)#[50:,:] #img[40:200,200:700]
        img=cv2.cvtColor(img,cv2.COLOR_BGR2YUV)#[50:,:] # this is correct


        img=img/255
        
        # plt.imshow(img)
        # plt.show()
        # break
        
        
        output = model.predict(np.asarray([img]))[0][0]
        x_coord = int(output * 960*2 + 960) # inverse the normalization
        if drive:
            pydirectinput.moveTo(x_coord,_pause=False)
            
        print(output,end = ' ')
        
        

    
    ## Calculate mean fps, mean is needed because the fps fluctuates rapidly
    time_difference = time()-old_time
    if time_difference == 0:
        time_difference = 0.016

    mean_fps.append(round(1/time_difference))
    if len(mean_fps) > 5: # sample the last 5 fps times
        mean_fps.pop(0)

    FPS = sum(mean_fps)/len(mean_fps)
    print(f'FPS = {FPS}')

    cv2.imshow('AI Mario Kart player',img)
    
    if cv2.waitKey(1) == ord('q'):
        cv2.destroyAllWindows()
        break
    
pydirectinput.keyUp('g',_pause=False)
print('Done')