from flask import Flask, render_template, request, redirect, url_for
from flask import SQLAlchemy
from flask import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

# Configurations
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../database/users.db'  # SQLite database
app.secret_key = 'supersecretkey'  # Secret key for session management
db = SQLAlchemy(app)

# Flask-Login setup
login_manager = LoginManager(app)
login_manager.login_view = 'home'

# User database model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    location = db.Column(db.String(200), nullable=True)  # Storing user's location (latitude,longitude)

# Flask-Login user loader
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Route for home page (login page)
@app.route('/')
def home():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))  # Redirect to dashboard if logged in
    return render_template('login.html')

# Login route
@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    user = User.query.filter_by(username=username).first()
    
    if user and check_password_hash(user.password, password):  # Verify password hash
        login_user(user)
        return redirect(url_for('dashboard'))
    
    return "Invalid credentials"

# Registration route
@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = generate_password_hash(password, method='sha256')  # Hash the password for security
        new_user = User(username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('register.html')

# Dashboard route (where user can set location)
@app.route('/dashboard', methods=['POST', 'GET'])
@login_required
def dashboard():
    if request.method == 'POST':  # Handle location update
        latitude = request.form['latitude']
        longitude = request.form['longitude']
        location = f"{latitude},{longitude}"  # Store location as a string
        current_user.location = location  # Update the user's location
        db.session.commit()  # Save to database
    location = current_user.location or "Not set"
    lat, lng = location.split(',') if ',' in location else ("", "")  # Split location into latitude and longitude
    return render_template('dashboard.html', latitude=lat, longitude=lng)

# Route for logging out
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

# Initialize the app
if __name__ == "__main__":
    app.run(debug=True)
