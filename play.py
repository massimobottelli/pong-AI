# Import required library
import turtle
import math
import random
import warnings
from joblib import load

warnings.filterwarnings("ignore", category=UserWarning)

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
    left_pad.sety(left_pad.ycor() + 20)


def paddle_a_down():
    left_pad.sety(left_pad.ycor() - 20)


# Functions to move right paddle vertically
def paddle_b_up():
    right_pad.sety(right_pad.ycor() + 20)


def paddle_b_down():
    right_pad.sety(right_pad.ycor() - 20)


# import the machine learning model
spline_model = load('spline_model.joblib')

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

# get key press
sc.listen()
sc.onkeypress(paddle_b_up, "Up")
sc.onkeypress(paddle_b_down, "Down")
sc.onkeypress(paddle_a_up, "e")
sc.onkeypress(paddle_a_down, "x")

sketch.clear()
sketch.write("HUMAN: " + str(score_human) + spacer + "AI: " + str(score_ai), align="center", font=("helvetica", 24, "normal"))

while True:  # loop
    sc.update()

    # calculate ball motion
    dx = speed * math.cos(math.radians(angle)) * direction
    dy = speed * math.sin(math.radians(angle)) * direction
    x = int(x + dx)
    y = int(y + dy)
    ball.setx(x)
    ball.sety(y)

    # automatic move right paddle
    if 'store_ball_y' in vars() and 'store_ball_angle' in vars():
        prediction_paddle_y = spline_model.predict([[store_ball_y, store_ball_angle]])
        right_pad.sety(int(prediction_paddle_y)+random.randint(-5,5))

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

    # if ball over paddle then start new game
    if x > 500 or x < -500:
        if x > 500:
            score_human+=1
        else:
            score_ai+=1
        x = 0
        y = 0
        angle = random.randint(-5, 5)
        direction = -1
        sketch.clear()
        sketch.write("HUMAN: " + str(score_human) + spacer + "AI: " + str(score_ai), align="center",
                     font=("helvetica", 24, "normal"))


