import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import warnings
from joblib import dump

from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import cross_val_score

warnings.filterwarnings("ignore", category=UserWarning)

print("Training model...")
df = pd.read_csv("dataset.csv", header=0)
X = df[['ball_y', 'ball_angle']]
y = df['paddle_y']

spline_model = Pipeline([('spline', RandomForestRegressor(n_estimators=800))])

# evaluate model
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
spline_model.fit(X_train, y_train)
y_pred = spline_model.predict(X_test)
scores = cross_val_score(spline_model, X, y, cv=5)
print("Cross-validation scores:", scores)
print("Mean score:", np.mean(scores))
print("Standard deviation:", np.std(scores))

# select ball position and draw diagram sample vs model
set_ball_y = 0
set_ball_angle = list(range(90, 270, 5))
predictions = []
for value in set_ball_angle:
    test_sample = [[set_ball_y, value]]
    prediction = spline_model.predict(test_sample)[0]
    predictions.append(prediction)
df = df[df["ball_y"] == set_ball_y]
df.plot(x='ball_angle', y='paddle_y', kind='scatter', color="orange", label="dataset")
plt.plot(set_ball_angle, predictions, label="prediction")
plt.title("Spline prediction vs dataset (ball-y = "+str(set_ball_y)+")")
plt.legend()
plt.xlim(90, 270)
plt.ylim(-400, 400)
plt.draw()
plt.savefig("plot-spline-"+str(set_ball_y)+".png")
plt.pause(2)
plt.close()

# train model on full dataset and store to joblib file
spline_model.fit(X, y)
dump(spline_model, 'spline_model.joblib')

# user input based prediction
set_ball_y = float(input("\nInsert initial ball position (y = -260/+260): "))
set_ball_angle = float(input("Insert initial ball angle (a = 100/260): "))
prediction_paddle_y = spline_model.predict([[set_ball_y, set_ball_angle]])
print("Predicted vertical paddle position: ", int(prediction_paddle_y[0]))
