from msilib import sequence
import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
from sklearn.utils import shuffle
from sklearn.model_selection import train_test_split
import matplotlib.image as mpimg
from imgaug import augmenters as iaa
import cv2
import random

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Convolution2D,Flatten,Dense
from tensorflow.keras.optimizers import Adam

def getName(filepath):
    return filepath.split('\\')[-1]

def importDataInfo(path):
    columns=['Center','Left','Right','Steering','Throttle','Brake','Speed']
    data = pd.read_csv(os.path.join(path,'driving_log.csv'),names=columns)
    #print(type(data))
    data['Center']=data['Center'].apply(getName)

    print(f'Total images imported: {data.shape[0]}')
    return data

def balanceData(data,display=True):
    nBins=31
    samplesPerBin=1000
    
    hist,bins=np.histogram(data['Steering'],nBins)
    #print(bins)
    if display:
        center=(bins[:-1]+bins[1:])*0.5
        # print(bins,end='\n\n')
        # print(len(bins),len(center))
        # print(center)
        plt.bar(center,hist,width=0.06) # lines has 1 less than areas
        plt.plot((-1,1),(samplesPerBin,samplesPerBin))
        plt.show()

    removeIndexList=[]
    for j in range(nBins):
        binDataList=[] # reset the list each time

        for i in range(len(data['Steering'])): # for each group iterate through and assign the data values to a group
            #                                   i is the index of the steering value
            if data['Steering'][i] >= bins[j] and data['Steering'][i] <= bins[j+1]:
                binDataList.append(i)

        #print(binDataList)
        binDataList=shuffle(binDataList) # randomise the list

        binDataList=binDataList[samplesPerBin:] # get the ones beyond 1000
        removeIndexList.extend(binDataList)     # and remove them from our list

    print('Removed Images: ',len(removeIndexList))
    data.drop(data.index[removeIndexList],inplace=True) # now we actuall remove these values from our list 
    #                                                   using the indexes we collected earlier in line 41
    print('Remaining Images: ',len(data))

    if display:
        hist,_=np.histogram(data['Steering'],nBins)

        plt.bar(center,hist,width=0.06) # lines has 1 less than areas
        plt.plot((-1,1),(samplesPerBin,samplesPerBin))
        plt.show()

def loadData(path,data):
    imagesPath=[]
    steering=[]

    for i in range(len(data)):
        indexedData=data.iloc[i] # data.iloc[i] = data[i]
        #                        # with standard index
        #print(indexedData)
        imagesPath.append(os.path.join(path,'IMG',indexedData[0])) # indexedData[0] is our image
        steering.append(float(indexedData[3]))
    imagesPath=np.asarray(imagesPath)
    steering=np.asarray(steering)
    return imagesPath,steering

def augmentImage(imgPath,steering):
    img=mpimg.imread(imgPath) # where we actually read the image not just edit the csv
    ## PAN
    if np.random.rand()<0.5:
        pan=iaa.Affine(translate_percent={'x':(-0.1,0.1),'y':(-0.1,0.1)})
        img=pan.augment_image(img)

    ## ZOOM
    if np.random.rand()<0.5:
        zoom=iaa.Affine(scale=(1,1.2))
        img=zoom.augment_image(img)

    ## BRIGHTNESS
    if np.random.rand()<0.5:
        brightness = iaa.Multiply((0.4,1.2))
        img=brightness.augment_image(img)
    
    ## FLIP
    if np.random.rand()<0.5:
        img=cv2.flip(img,1)
        steering=-steering # if we flip the image we have to flip the steering


    return img,steering

def preProcessing(img): 
    img=img[60:135,:,:] # we will crop so that we only have the road region
    img=cv2.cvtColor(img,cv2.COLOR_RGB2YUV)
    
    img=cv2.GaussianBlur(img,(3,3),0)
    img=cv2.resize(img,(200,66))

    # Normalise
    img=img/255
    return img

def batchGen(imagesPath,steeringList,batchSize,trainFlag):
    while True:
        imgBatch=[]
        steeringBatch=[]

        for i in range(batchSize):
            index=random.randint(0,len(imagesPath)-1)
            if trainFlag:
                img,steering=augmentImage(imagesPath[index],steeringList[index])
            else:
                img=mpimg.imread(imagesPath[index])
                steering=steeringList[index]

            img=preProcessing(img)
            
            imgBatch.append(img)
            steeringBatch.append(steering)

        yield(np.asarray(imgBatch),np.asarray(steeringBatch))

def createModel():
    model=Sequential()

    model.add(Convolution2D(24,(5,5),(2,2),input_shape=(66,200,3),activation='elu'))
    model.add(Convolution2D(36,(5,5),(2,2),activation='elu'))
    model.add(Convolution2D(48,(5,5),(2,2),activation='elu'))
    model.add(Convolution2D(64,(3,3),activation='elu'))
    model.add(Convolution2D(64,(3,3),activation='elu'))

    model.add(Flatten())
    model.add(Dense(100,activation='elu'))
    model.add(Dense(50,activation='elu'))
    model.add(Dense(10,activation='elu'))
    model.add(Dense(1))

    model.compile(Adam(learning_rate=0.0001),loss='mse')
    
    return model


# print(mpimg.imread('left.jpg'))
# imgRe=preProcessing(mpimg.imread('left.jpg'))
# plt.imshow(imgRe)
# plt.show()