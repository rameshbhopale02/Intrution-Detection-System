import numpy as np
from flask import Flask, request, jsonify, render_template, redirect, url_for, flash, session
import joblib
from pymongo import MongoClient
from functools import wraps
import bcrypt
from werkzeug.security import generate_password_hash, check_password_hash

# Initialize Flask application
app = Flask(__name__)
app.secret_key = 'p26b5LZUEGuPkvekv6ZzkwInufEDyjfT'

# Load the prediction model
model = joblib.load('model.pkl')

# MongoDB setup
client = MongoClient('mongodb://localhost:27017/')
db = client['intrusion']
collection = db['security']

# Function to check if the user is logged in as an admin
def is_admin_logged_in():
    return session.get('admin_logged_in', False)

# Decorator to restrict access to admin pages
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not is_admin_logged_in():
            flash('Access denied. Administrative login required.', 'error')
            return redirect(url_for('admin_login'))  # Redirect to the admin login page
        return f(*args, **kwargs)
    return decorated_function

# Home route - Login page
@app.route('/')
def home():
    return render_template('index.html')

# Home route - Login page
@app.route('/home')
def goHome():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']

        # Check if user already exists
        if collection.find_one({'email': email}):
            flash('Email already registered. Please use a different email.', 'error')
            return redirect(url_for('register'))

        # Hash the password for security
        hashed_password = generate_password_hash(password)

        # Insert the user data into MongoDB
        collection.insert_one({
            'name': name,
            'email': email,
            'password': hashed_password
        })

        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']  # Retrieve the email from the form
        password = request.form['password']  # Retrieve the password from the form

        # Find the user by email in the MongoDB collection
        user = collection.find_one({'email': email})

        # Check if user exists and the password matches
        if user and check_password_hash(user['password'], password):
            flash('Logged in successfully!', 'success')
            # Store the user session or redirect to a user dashboard
            session['user_logged_in'] = True
            session['user_email'] = email
            return render_template('predict.html')  # Redirect to the home page or user dashboard
        else:
            flash('Invalid email or password. Please try again.', 'error')
            return redirect(url_for('login'))  # Reload the login page on failure

    return render_template('login.html')  # when relo


@app.route('/predPage')
def predPage():
     return render_template('predict.html')

# Home route - Login page
@app.route('/upload')
def upload():
    return render_template('upload.html')

# Prediction handling route
@app.route('/predict', methods=['POST'])
def predict():
    int_features = [float(x) for x in request.form.values()]

    if int_features[0] == 0:
        f_features = [0, 0, 0] + int_features[1:]
    elif int_features[0] == 1:
        f_features = [1, 0, 0] + int_features[1:]
    elif int_features[0] == 2:
        f_features = [0, 1, 0] + int_features[1:]
    else:
        f_features = [0, 0, 1] + int_features[1:]

    if f_features[6] == 0:
        fn_features = f_features[:6] + [0, 0] + f_features[7:]
    elif f_features[6] == 1:
        fn_features = f_features[:6] + [1, 0] + f_features[7:]
    else:
        fn_features = f_features[:6] + [0, 1] + f_features[7:]

    final_features = [np.array(fn_features)]
    prediction = model.predict(final_features)

    if prediction == 0:
        output = 'Normal'
    elif prediction == 1:
        output = 'DOS'
    elif prediction == 2:
        output = 'PROBE'
    elif prediction == 3:
        output = 'R2L'
    else:
        output = 'U2R'

    return render_template('predict.html', output=output)

@app.route('/upload2', methods=['POST'])
def upload2():
    data = request.get_json()
    
    # Extract values from the JSON data
    int_features = [
        data['attackType'], data['count'], data['dstHostDiffSrvRate'],
        data['dstHostSameSrcPortRate'], data['dstHostSameSrvRate'],
        data['dstHostSrvCount'], data['flag'], data['lastFlag'],
        data['loggedIn'], data['sameSrvRate'], data['serrorRate'],
        data['serviceHttp']
    ]

    # Prepare features based on the initial attack type
    if int_features[0] == 0:
        f_features = [0, 0, 0] + int_features[1:]
    elif int_features[0] == 1:
        f_features = [1, 0, 0] + int_features[1:]
    elif int_features[0] == 2:
        f_features = [0, 1, 0] + int_features[1:]
    else:
        f_features = [0, 0, 1] + int_features[1:]

    # Adjust features based on the connection status
    if f_features[6] == 0:
        fn_features = f_features[:6] + [0, 0] + f_features[7:]
    elif f_features[6] == 1:
        fn_features = f_features[:6] + [1, 0] + f_features[7:]
    else:
        fn_features = f_features[:6] + [0, 1] + f_features[7:]

    final_features = [np.array(fn_features)]
    predict = model.predict(final_features)

    # Determine output class
    if predict == 0:
        output = 'Normal'
    elif predict == 1:
        output = 'DOS'
    elif predict == 2:
        output = 'PROBE'
    elif predict == 3:
        output = 'R2L'
    else:
        output = 'U2R'

    return jsonify(output)


# API endpoint for results
@app.route('/results', methods=['POST'])
def results():
    data = request.get_json(force=True)
    prediction = model.predict([np.array(list(data.values()))])

    if prediction == 0:
        output = 'Normal'
    elif prediction == 1:
        output = 'DOS'
    elif prediction == 2:
        output = 'PROBE'
    elif prediction == 3:
        output = 'R2L'
    else:
        output = 'U2R'

    return jsonify(output)

# Redirecting to logout.html
@app.route('/logout')
def logout():
    session['admin_logged_in']= False
    flash('Logout successful.', 'danger')
    return render_template('login.html')

if __name__ == "__main__":
    app.run(debug=True)
