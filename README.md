# AI-Mario-Kart
A Convolutional Neural Network that can drive Mario Kart Wii on Dolphin by moving the mouse pointer horizontally to control the steering angle. This project was done as a "learning excercise" back in 2021 when I was learning about self driving cars and CNNs. It can steer round a track but often steers wrong and gets stuck, as is typical with Imitation Learning methods "going out of distribution" like this one

## Gamplay on pre-trained model
To play this download the repo and move AI Mario Kart.ini to ```%USERPROFILE%\Documents\Dolphin Emulator\Config\Profiles\Wiimote``` Then run AI_Player, it will find the pre-trained model in the /models directory. Launch Dolphin with the game at native resolution

### Controlling the AI
You can then play with the AI by moving the dolphin window so that it fits inside the window from AI_player (screen capture) the AI will then view your gameplay and attempt to steer for you. Press the ```m``` key to start the AI (it will control your mouse to steer), ```c``` to stop and ```q``` to quit.

Note that gameplay requires Windows due to AI_player requiring the ```pydirectinput``` library to simulate hardware imput (to circumvent directX anti-cheat) that only works on Windows sadly. You can still build and train the dataset though on other operating systems but AI_player is Windows only. 

## Training on custom dataset
Data_collection v4.3.py is used to build a dataset and CNN_Training v5.5.ipynb is used to train and export a model using your dataset. You can then use AI_player to play mario kart using your trained model.

