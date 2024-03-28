import requests
import numpy as np
import pickle
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

model = pickle.load(open("disease_predict.pkl","rb"))



@app.route('/')
def index():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    # Get username and password from the login form
    username = request.form['username']
    password = request.form['password']

    # Perform authentication logic here (you might compare with a database, etc.)
    # For simplicity, we'll use a dummy check with a hardcoded username and password
    if username == 'user1' and password == 'password1':
        return render_template('dashboard.html')
    else:
        return render_template('login.html', error='Invalid username or password')
    
@app.route("/dashboard")  
def dashboard():
    return render_template("dashboard.html")  

@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if request.method == 'POST':
        # Get user input for thyroid prediction
        age = int(request.form['age'])
        t_hormone = float(request.form['TSH'])
        T3_hormones = float(request.form['T3'])
        TT4_hormones = int(request.form['TT4'])
        free_thyroxine= int(request.form['FTI'])
        sex_M = int(request.form['sex_M'])
        T3_measured_t = int(request.form['T3_measured_t'])
        referral_source_SVI = int(request.form['referral_source_SVI'])
        referral_source_other = int(request.form['referral_source_other'])

        # Send the input data to your Flask backend

            # Use predict_proba for binary classification problems
        input_data = (age,t_hormone,T3_hormones,TT4_hormones,free_thyroxine,sex_M,T3_measured_t,referral_source_SVI,referral_source_other)

        #change the input data to a numpy array
        input_data_as_numpy_array = np.asarray(input_data)

        #reshape the numpy array as we are predicting only one instance
        input_data_reshaped = input_data_as_numpy_array.reshape(1, -1)

        prediction = model.predict(input_data_reshaped)
        print(prediction)

        if (prediction[0]==0):
            result = "The person does not have a Thyroid disease"

        else:
            result = "The person has Thyroid Disease\n he/she must take precautions and visit Doctor for proper treatment"
      

        return render_template('prediction_result.html', result = result)

if __name__ == '__main__':
    app.run(debug=True)
