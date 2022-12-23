# Import required library
import turtle
import math
import random
import time
import os
import pandas as pd
import warnings

from joblib import dump, load
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestRegressor

warnings.filterwarnings("ignore", category=UserWarning)

while True:  # loop

    if 'mode' not in vars():
        # User select Train or Play
        print("Select mode:\n1 = Train\n2 = Play")
        mode = int(input("Your choice? "))

    if mode == 1:
        size = int(input("Size of training dataset? (recommended > 500): "))
        cont = 0
        print("Collecting dataset...")

    # Initialize screen
    if 'sc' not in vars():
        sc = turtle.Screen()
        sc.title("Pong-AI")
        sc.bgcolor("black")
        sc.setup(width=1000, height=600)
        sketch = turtle.Turtle()
        sketch.speed(0)
        sketch.color("white")
        sketch.penup()
        sketch.hideturtle()
        sketch.goto(0, 240)

        # Draw left paddle
        left_pad = turtle.Turtle()
        left_pad.speed(0)
        left_pad.shape("square")
        left_pad.color("white")
        left_pad.shapesize(stretch_wid=4, stretch_len=1)
        left_pad.penup()
        left_pad.goto(-400, 0)

        # Draw right paddle
        right_pad = turtle.Turtle()
        right_pad.speed(0)
        right_pad.shape("square")
        right_pad.color("white")
        right_pad.shapesize(stretch_wid=4, stretch_len=1)
        right_pad.penup()
        right_pad.goto(400, 0)
        right_pad.speed(10)

        # Draw ball
        ball = turtle.Turtle()
        ball.speed(50)
        ball.shape("square")
        ball.color("white")
        ball.penup()
        ball.goto(0, 0)

    # Functions to move left paddle vertically


    def paddle_a_up():
        left_pad.sety(left_pad.ycor() + 25)


    def paddle_a_down():
        left_pad.sety(left_pad.ycor() - 25)


    # initialize game
    x = 0
    y = 0
    angle = random.randint(-5, 5)
    speed = 20
    direction = -1
    score_human = 0
    score_ai = 0
    spacer = ""
    for n in range(80):
        spacer += " "

    sc.listen()
    sc.onkeypress(paddle_a_up, "e")
    sc.onkeypress(paddle_a_down, "x")

    if mode == 2:  # play mode
        # show score
        sketch.clear()
        sketch.write("HUMAN: " + str(score_human) + spacer + "AI: " + str(score_ai),
                     align="center", font=("helvetica", 24, "normal"))

    if mode == 2:  # play mode
        # import the machine learning model
        spline_model = load('spline_model.joblib')

    while True:  # loop

        sc.update()

        # calculate ball motion
        dx = speed * math.cos(math.radians(angle)) * direction
        dy = speed * math.sin(math.radians(angle)) * direction
        x = int(x + dx)
        y = int(y + dy)
        ball.setx(x)
        ball.sety(y)

        if mode == 1:  # train mode
            # automatic move paddles for training
            right_pad.sety(y + random.randint(-45, 45))

        # ball bounce on top and bottom edges
        if y > 280:
            y = 275
            angle = -angle
        if y < -280:
            y = -275
            angle = -angle

        # detect ball collision with left paddle
        if (-370 > ball.xcor() > -390) and (
                left_pad.ycor() + 40 > ball.ycor() > left_pad.ycor() - 40):
            angle = 180 - angle + y - left_pad.ycor()  # angle modified according to impact position
            while angle > 360:
                angle = angle - 360
            while angle < 0:
                angle = angle + 360
            x = -365

            if mode == 2:  # play mode
                # move right paddle to predicted position
                prediction_paddle_y = spline_model.predict([[y, angle]])
                right_pad.sety(int(prediction_paddle_y) + random.randint(-5, 5))

            if mode == 1:  # train mode
                # store ball vert position and angle on contact with left paddle
                store_ball_y = y
                store_ball_angle = angle

        # detect ball collision with right paddle
        if (370 < ball.xcor() < 390) and (
                right_pad.ycor() + 40 > ball.ycor() > right_pad.ycor() - 40):
            # angle modified according to impact position
            angle = 180 - angle - y + right_pad.ycor()
            x = 365

            if mode == 1:  # train mode
                # get right paddle vert pos and store data on file
                store_paddle_y = right_pad.ycor()
                if 'store_ball_y' in vars() and 'store_ball_angle' in vars():
                    string = str(store_ball_y) + ',' + str(store_ball_angle) + ',' + str(store_paddle_y) + '\n'
                    f = open('dataset.csv', 'a+')
                    if os.stat('dataset.csv').st_size == 0:
                        f.write('ball_y,ball_angle,paddle_y\n')
                    f.write(string)
                    f.close()
                    # when dataset size reached, then train model
                    cont += 1
                    if cont == size:
                        print("Dataset complete, training model...")
                        df = pd.read_csv("dataset.csv", header=0)
                        X = df[['ball_y', 'ball_angle']]
                        y = df['paddle_y']
                        spline_model = Pipeline([('spline', RandomForestRegressor(n_estimators=800))])
                        spline_model.fit(X, y)
                        dump(spline_model, 'spline_model.joblib')
                        print("Training completed.\nNow Play!")
                        mode = 2
                        time.sleep(2)
                        break

                '''# restart after right paddle hit - for training purpose
                x = 0
                y = 0
                angle = random.randint(-5, 5)
                direction = -1
                # reset data if already defined
                if 'store_ball_y' in vars():
                    del store_ball_y
                if 'store_ball_angle' in vars():
                    del store_ball_angle
                if 'store_paddle_y' in vars():
                    del store_paddle_y'''

        # if ball over paddle then start new game
        if x > 500 or x < -500:

            if mode == 2:  # play mode
                if x > 500:
                    score_human += 1
                else:
                    score_ai += 1

            x = 0
            y = 0
            angle = random.randint(-5, 5)
            direction = -1
            left_pad.goto(-400, 0)

            if mode == 1:  # train mode
                # reset data if already defined
                if 'store_ball_y' in vars():
                    del store_ball_y
                if 'store_ball_angle' in vars():
                    del store_ball_angle
                if 'store_paddle_y' in vars():
                    del store_paddle_y

            if mode == 2:  # play mode
                sketch.clear()
                sketch.write("HUMAN: " + str(score_human) + spacer + "AI: " + str(score_ai),
                             align="center", font=("helvetica", 24, "normal"))
                time.sleep(1)
