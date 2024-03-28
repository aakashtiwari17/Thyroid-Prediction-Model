import requests
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Replace this URL with the actual URL of your Google Colab backend
colab_backend_url = "https://colab.research.google.com/drive/1O5dJvqLs5Xf3NlI1BlEivkGMYBLqTwct#scrollTo=MckFCc_O1JqA"

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
        return redirect(url_for('dashboard', username=username))
    else:
        return render_template('login.html', error='Invalid username or password')

@app.route('/dashboard/<username>', methods=['GET', 'POST'])
def dashboard(username):
    if request.method == 'POST':
        # Get user input for thyroid prediction
        age = request.form['age']
        TSH = request.form['TSH']
        T3 = request.form['T3']
        TT4 = request.form['TT4']
        FTI = request.form['FTI']
        sex_M = request.form['sex_M']
        T3_measured_t = request.form['T3_measured_t']
        referral_source_SVI = request.form['referral_source_SVI']
        referral_source_other = request.form['referral_source_other']
        result = request.form['result']

        # Send the input data to your Google Colab backend
        try:
            input_data = {
                'age': age,
                'TSH': TSH,
                'T3': T3,
                'TT4': TT4,
                'FTI': FTI,
                'sex_M': sex_M,
                'T3_measured_t': T3_measured_t,
                'referral_source_SVI': referral_source_SVI,
                'referral_source_other': referral_source_other,
                'result': result
            }
            response = requests.post(colab_backend_url, json=input_data)
            response.raise_for_status()  # Raise an HTTPError for bad responses (4xx and 5xx)
            result = response.json()
            return render_template('prediction_result.html', result=result['prediction'])
        except requests.exceptions.HTTPError as errh:
            print("HTTP Error:", errh)
        except requests.exceptions.ConnectionError as errc:
            print("Error Connecting:", errc)
        except requests.exceptions.Timeout as errt:
            print("Timeout Error:", errt)
        except requests.exceptions.RequestException as err:
            print("Something went wrong:", err)

    return render_template('dashboard.html', username=username)

if __name__ == '__main__':
    app.run(debug=True)
