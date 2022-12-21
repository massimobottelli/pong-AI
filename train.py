# Import required library
import turtle
import math
import random
import os

# Initialize screen
sc = turtle.Screen()
sc.title("PONG")
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

# Draw ball
ball = turtle.Turtle()
ball.speed(50)
ball.shape("square")
ball.color("white")
ball.penup()
ball.goto(0, 0)

# initialize ball
x = 0
y = 0
angle = random.randint(-45, 45)
speed = 20
direction = -1


while True:  # loop

    # calculate ball motion
    dx = speed * math.cos(math.radians(angle)) * direction
    dy = speed * math.sin(math.radians(angle)) * direction
    x = int(x + dx)
    y = int(y + dy)
    ball.setx(x)
    ball.sety(y)

    # automatic move left paddle
    left_pad.sety(y + random.randint(-45, 45))

    # automatic move right paddle
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

        # store ball vert position and angle on contact with left paddle
        store_ball_y = y
        store_ball_angle = angle

    # detect ball collision with right paddle
    if (370 < ball.xcor() < 390) and (
            right_pad.ycor() + 40 > ball.ycor() > right_pad.ycor() - 40):
        # angle modified according to impact position
        angle = 180 - angle - y + right_pad.ycor()
        x = 365

        # store right paddle vert pos
        store_paddle_y = right_pad.ycor()

        # if ball already bounced on left paddle then store data on file
        if 'store_ball_y' in vars() and 'store_ball_angle' in vars():
            string = str(store_ball_y) + ',' + str(store_ball_angle) + ',' + str(store_paddle_y) + '\n'
            f = open('dataset.csv', 'a+')
            if os.stat('dataset.csv').st_size == 0:
                f.write('ball_y,ball_angle,paddle_y\n')
            f.write(string)
            f.close()

        # restart after right paddle hit - for training purpose
        x = 0
        y = 0
        angle = random.randint(-45, 45)
        direction = -1
        # reset data if already defined
        if 'store_ball_y' in vars():
            del store_ball_y
        if 'store_ball_angle' in vars():
            del store_ball_angle
        if 'store_paddle_y' in vars():
            del store_paddle_y

    # if ball over paddle then start new game
    if x > 500 or x < -500:
        x = 0
        y = 0
        angle = random.randint(-45, 45)
        direction = -1
        # reset data if already defined
        if 'store_ball_y' in vars():
            del store_ball_y
        if 'store_ball_angle' in vars():
            del store_ball_angle
        if 'store_paddle_y' in vars():
            del store_paddle_y
