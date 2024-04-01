

from werkzeug.security import generate_password_hash, check_password_hash

def generate_hash(password):
    return generate_password_hash(str(password))

stored_password = generate_hash(123)

def checkHash(password):
    return check_password_hash(stored_password, str(password))

print(stored_password)
print(checkHash(123))




from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://cvrsdb_owner:yW8bOPEI5Ckr@ep-yellow-scene-a5urfsdy.us-east-2.aws.neon.tech/cvrsdb?sslmode=require'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Define the User model
class User(db.Model):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    first_name = db.Column(db.String(255))
    last_name = db.Column(db.String(255))
    email = db.Column(db.String(255), unique=True)

    def __init__(self, username, password, first_name, last_name, email):
        self.username = username
        self.password = generate_hash(password)  # Hashing the password
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        
        
        
@app.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    if not all(key in data for key in ['username', 'password', 'first_name', 'last_name', 'email']):
        return jsonify({'message': 'Missing parameters'}), 400

    username = data['username']
    password = data['password']
    first_name = data['first_name']
    last_name = data['last_name']
    email = data['email']

    if User.query.filter_by(username=username).first():
        return jsonify({'message': 'Username already exists'}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({'message': 'Email already registered'}), 400

    new_user = User(username=username, password=password, first_name=first_name, last_name=last_name, email=email)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'User registered successfully'})


@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if not all(key in data for key in ['email', 'password']):
        return jsonify({'message': 'Missing parameters'}), 400

    email = data['email']
    password = data['password']

    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({'message': 'User not found'}), 404

    if not check_password_hash(user.password, password):
        return jsonify({'message': 'Invalid password'}), 401

    return jsonify({'message': 'Login successful'})  



if __name__ == '__main__':
    app.run(debug=True)
