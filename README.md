# AI-Mario-Kart
A Convolutional Neural Network that can drive Mario Kart Wii on Dolphin by moving the mouse pointer horizontally to control the steering angle.

## Gamplay on pre-trained model
To play this download the repo and move AI Mario Kart.ini to ```%USERPROFILE%\Documents\Dolphin Emulator\Config\Profiles\Wiimote``` Then run AI_Player, it will find the pre-trained model in the /models directory. Launch Dolphin with the game at native resolution

### Controlling the AI
You can then play with the AI by moving the dolphin window so that it fits inside the window from AI_player (screen capture) the AI will then view your gameplay and attempt to steer for you. Press the ```m``` key to start the AI (it will control your mouse to steer), ```c``` to stop and ```q``` to quit.

## Training on custom dataset
Data_collection v4.3.py is used to build a dataset and CNN_Training v5.5.ipynb is used to train and export a model using your dataset. You can then use AI_player to play mario kart using your trained model.

