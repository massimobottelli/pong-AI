# Pong AI

This project aims to train a machine learning model to play the classic video game Pong against a human opponent.

To do this, I developed a Python script to play Pong and record all relevant metrics (such as paddle position and ball angle) to create a dataset. 
This dataset is then used to train the machine learning model using scikit-learn. 
The resulting model is able to predict the proper position of the paddle to catch the ball when the computer plays against a human player.

The project is composed by three script:

## Train

An implementation of the classic game Pong using Python's turtle library. The game is played on a screen with two paddles and a ball. The ball bounces off the top and bottom edges of the screen, and when it hits one of the paddles, it bounces back and its angle is modified according to the position it hits on the paddle. For machine learning training purpose, both paddles are moved automatically, based on vertical position of the ball, with random variation to include variation of angle when hitting the ball.

In addition to the game logic, the code also includes functionality to store data on the ball's position and angle, as well as the right paddle's position, when the ball hits the right paddle. This data is stored in a CSV file called "dataset.csv". The code also includes a loop that restarts the game after the ball hits the right paddle for training purposes.

## Learn
xxx

## Play
xxx

# How to use

1. Run the train.py script to start training the model. The script will automatically play Pong and record the necessary data to create the dataset. 
2. Once the dataset big enough (2000 to 3000 records recommended), run learn.py script to train the machine learning model.
3. You can finally run the play.py script to play Pong against the computer using the trained model. 

