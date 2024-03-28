# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
import joblib

# Loading the CSV data into a pandas data frame
thyroid_data = pd.read_csv(r"C:/Users/theof/OneDrive\Desktop\disease/final_data (1).csv")

# Splitting the features and result
x = thyroid_data.drop(columns="Result", axis=1)
y = thyroid_data['Result']

# Splitting the data into training and testing data
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, stratify=y, random_state=2)

# Model training (Logistic Regression)
model = LogisticRegression()

# Training the Logistic regression model with Training data
model.fit(x_train, y_train)

# Accuracy score on training data
x_train_prediction = model.predict(x_train)
training_data_accuracy = accuracy_score(x_train_prediction, y_train)
print("Accuracy on training data:", training_data_accuracy)

# Accuracy score on test data
x_test_prediction = model.predict(x_test)
testing_data_accuracy = accuracy_score(x_test_prediction, y_test)
print("Accuracy on testing data:", testing_data_accuracy)

# Building a predictive system
input_data = (23, 4.1, 2, 102, 100, 0, 1, 0, 19)

# Change the input data to a numpy array
input_data_as_numpy_array = np.asarray(input_data)

# Reshape the numpy array as we are predicting only one instance
input_data_reshaped = input_data_as_numpy_array.reshape(1, -1)

# Prediction
prediction = model.predict(input_data_reshaped)
print("Prediction:", prediction)

if prediction[0] == 0:
    print("The person does not have a Thyroid disease")
else:
    print("The person has Thyroid Disease")

# Save the trained model using joblib
joblib.dump(model, 'trained_model.pkl')
