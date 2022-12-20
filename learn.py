import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import warnings

from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import cross_val_score

warnings.filterwarnings("ignore", category=UserWarning)

df = pd.read_csv("dataset.csv", header=0)

X = df[['ball_y', 'ball_angle']]
y = df['paddle_y']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

print("Training model...")
spline_model = Pipeline([('spline', RandomForestRegressor(n_estimators=800))])

spline_model.fit(X_train, y_train)
y_pred = spline_model.predict(X_test)

scores = cross_val_score(spline_model, X, y, cv=5)
print("Cross-validation scores:", scores)
print("Mean score:", np.mean(scores))
print("Standard deviation:", np.std(scores))

# select sample angle and draw diagram sample vs model
set_ball_angle = 0
set_ball_y = list(range(90, 270, 5))
predictions = []
for value in set_ball_y:
    test_sample = [[set_ball_angle, value]]
    prediction = spline_model.predict(test_sample)[0]
    predictions.append(prediction)

df = df[df["ball_y"] == set_ball_angle]
df.plot(x='ball_angle', y='paddle_y', kind='scatter', color="orange", label="dataset")
plt.plot(set_ball_y, predictions, label="prediction")
plt.title("Spline prediction vs dataset (ball-y = "+str(set_ball_angle)+")")
plt.legend()
plt.xlim(140, 220)
plt.ylim(-400, 400)
plt.draw()
plt.savefig("plot-spline-"+str(set_ball_angle)+".png")
plt.pause(2)
plt.close()

# sample prediction
spline_model.fit(X, y)
set_ball_y = float(input("\nInsert initial ball position (y = -260/+260): "))
set_ball_angle = float(input("Insert initial ball angle (a = 100/260): "))
prediction_paddle_y = spline_model.predict([[set_ball_y, set_ball_angle]])
print("Predicted vertical paddle position: ", int(prediction_paddle_y[0]))
