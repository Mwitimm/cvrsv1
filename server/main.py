from flask import Flask,render_template,jsonify,request
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash,check_password_hash
from sqlalchemy.orm.exc import NoResultFound
from flask_cors import CORS
from sqlalchemy import text
from joblib import load




app = Flask("__main__")
CORS(app)

model = load("random_forest_model.joblib")

def generate_hash(password):
    return generate_password_hash(str(password))




# Database configuration
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
        
  




@app.route("/")
def loadHome():
    return render_template("home.html")



@app.route("/predict",methods=["POST"])
def predit():
    features = request.json
    
    values=list(features.values())
    predict = model.predict([values])
    return jsonify({"prediction": predict[0]})


@app.route('/users/add', methods=['POST'])
def add_user():
    data = request.get_json()
    new_user = User(
        username=data['username'],
        password=data['password'],
        first_name=data['first_name'],
        last_name=data['last_name'],
        email=data['email'],
        phone_number=data['phone_number'],
        language=data['language']
    )
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User added successfully'})



@app.route('/signup', methods=['POST',"OPTIONS"])
def signup():
    if request.method == 'OPTIONS':
        # Respond to the CORS preflight request
        return '', 204
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

    return jsonify({'message': 'Login successful', 'user_id': user.user_id,'username':user.username})


class Variety(db.Model):
    __tablename__ = 'varieties'

    variety_id = db.Column(db.Integer, primary_key=True)
    cropname = db.Column(db.String(50))
    varietyname = db.Column(db.String(50))
    yearofrelease = db.Column(db.Integer)
    maintainerseedlingsource = db.Column(db.String(100))
    optimalproductionaltitude = db.Column(db.String(50))
    durationtomaturitymonths = db.Column(db.Integer)
    yieldpertreeperyear = db.Column(db.String(20))
    specialattributes = db.Column(db.Text)
    economicproductionlifeyears = db.Column(db.Integer)

    def to_dict(self):
        return {
            'variety_id': self.variety_id,
            'cropname': self.cropname,
            'varietyname': self.varietyname,
            'yearofrelease': self.yearofrelease,
            'maintainerseedlingsource': self.maintainerseedlingsource,
            'optimalproductionaltitude': self.optimalproductionaltitude,
            'durationtomaturitymonths': self.durationtomaturitymonths,
            'yieldpertreeperyear': self.yieldpertreeperyear,
            'specialattributes': self.specialattributes,
            'economicproductionlifeyears': self.economicproductionlifeyears
        }



varieties_by_crop = {}

@app.route('/varieties', methods=['GET'])
def get_varieties():
    try:
        cropname = request.args.get('cropname')
        
        if cropname:
            varieties = Variety.query.filter_by(cropname=cropname).all()
        else:
            return jsonify({"error": "Cropname parameter is missing."}), 400
        for variety in varieties:
            cropname = variety.cropname
            if cropname not in varieties_by_crop:
                varieties_by_crop[cropname] = []
            varieties_by_crop[cropname].append(variety.to_dict())
        return jsonify(varieties_by_crop)
    except Exception as e:
        print(str(e))
        return jsonify({"error": str(e)}), 500
    
    
def get_varieties_by_altitude_and_maturity(data, altitude_range, maturity_duration):
    """
    Returns a list of variety dictionaries that match the given altitude range and maturity duration.
    
    Args:
        data (dict): A dictionary where the keys are cropnames, and the values are lists of variety dictionaries.
        altitude_range (str): A string representing the desired altitude range (e.g., "1300-1800").
        maturity_duration (int): An integer representing the desired duration to maturity in months.
        
    Returns:
        list: A list of variety dictionaries that match the given criteria.
    """
    matched_varieties = []
    
    for crop, varieties in data.items():
        for variety in varieties:
            if (
                variety["optimalproductionaltitude"] == altitude_range
                and variety["durationtomaturitymonths"] == maturity_duration
            ):
                matched_varieties.append(variety)
    
    return matched_varieties


@app.route('/varieties/specific', methods=['GET'])
def get_specific_varieties():
    data = varieties_by_crop
    
    altitude_range = request.args.get('altitude_range')
    maturity_duration = request.args.get('maturity_duration', type=int)
    
    if not altitude_range or not maturity_duration:
        return jsonify({'error': 'Missing required parameters'}), 400
    
    matching_varieties = get_varieties_by_altitude_and_maturity(data, altitude_range, maturity_duration)
    
    if not matching_varieties:
        return jsonify({'message': 'No varieties found matching the specified criteria'}), 404
    
    return jsonify(matching_varieties)
    


if __name__ == "__main__":
    app.run(debug=True,port=8080)