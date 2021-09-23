import cv2
import numpy as np
from time import time
import pydirectinput
import keyboard
from tensorflow.keras.models import load_model
import mss
from os.path import join

model_path = join('models','v4.6_new_model.h5') #v4.7_N64_Mario_Raceway
#model_path = join('models','v4.7_N64_Mario_Raceway.h5')
model = load_model(model_path)


autonomous = False

sct = mss.mss()
mon = {'top': 197, 'left':544,'width':820,'height': 400} # 960-832/2,540-486/2, 820, 400)

drive = True


while True:
    old_time = time()
    
    img = np.asarray(sct.grab(mon))

    
    if keyboard.is_pressed("m"):
        autonomous = True
        if drive:
            pydirectinput.keyDown('g')
    
    if keyboard.is_pressed("c"):
        autonomous = False
        pydirectinput.keyUp('g')
        
    if keyboard.is_pressed('r'):
        drive = True
        pydirectinput.keyDown('g')
        
    elif keyboard.is_pressed('t'):
        drive = False
        
    if autonomous:

        
        x = 130
        y = 200
        #cv2.rectangle(img, (x, y), (x+360, 400), (0,0,0), -1)
        
        img=cv2.resize(img,(200,66))
        
        img=cv2.cvtColor(img,cv2.COLOR_BGR2YUV)#[50:,:] #img[40:200,200:700]
        img=img/255

        
        img=cv2.GaussianBlur(img,(3,3),0)
        
        
        
        output = model.predict(np.asarray([img]))[0][0]
        x_coord = int(output * 960 + 960) # inverse the normalization
        if drive:
            pydirectinput.moveTo(x_coord)
            
        print(output,end = ' ')
        
        
    cv2.imshow('AI Mario Kart player',img)
    
    if cv2.waitKey(1) == ord('q'):
        cv2.destroyAllWindows()
        break
    
    print(f'FPS = {round(1/(time()-old_time))}')
    
pydirectinput.keyUp('g')
print('Done')