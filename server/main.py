from flask import Flask,render_template,jsonify,request
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash,check_password_hash
from sqlalchemy.orm.exc import NoResultFound
from flask_cors import CORS
from sqlalchemy import text,MetaData
from joblib import load
import numpy as np
from datetime import datetime, timezone



app = Flask("__main__")
CORS(app)

model = load("random_forest_model.joblib")

stacked_model = load("stacking_classifier_model.joblib")

def generate_hash(password):
    return generate_password_hash(str(password))




# Database configuration
#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://cvrsdb_owner:yW8bOPEI5Ckr@ep-yellow-scene-a5urfsdy.us-east-2.aws.neon.tech/cvrsdb?sslmode=require'

#app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db_host = 'localhost'
db_port = 8000
db_name = 'cvrsdb'
db_user = 'postgres'
db_password = 'admin'

# SQLAlchemy configuration
app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}'
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







@app.route("/predict", methods=["POST"])
def predict():
    features = request.json

    values = [float(value) for value in features.values()]

    # Use the stacked model for prediction
    prediction = stacked_model.predict([values]).tolist()

    # Get the predicted crop label

    # Get the probability of the predicted crop
    probabilities = stacked_model.predict_proba([values])
    
    probabilities = stacked_model.predict_proba([values])
    
    # Convert probabilities array to a list
    #probabilities_list = probabilities.tolist()
    
    max_probability_index = np.argmax(probabilities)
    max_probability = probabilities[0][max_probability_index] * 10
    
 

    return jsonify({
        "prediction": prediction[0],
        "compactibility":max_probability
    })


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
            if not varieties:
                return jsonify({"error": f"No varieties found for crop '{cropname}'."}), 404
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



@app.route('/user/<int:user_id>', methods=['GET'])
def get_user(user_id):
    try:
        user = User.query.filter_by(user_id=user_id).first()
        if user:
            user_data = {
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email
            }
            return jsonify(user_data), 200
        else:
            return jsonify({'error': 'User not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
    
# Define the UserProfile model
class UserProfile(db.Model):
    __tablename__ = 'users'
    __table_args__ = {'extend_existing': True}
    user_id = db.Column(db.Integer, primary_key=True)
    phone_number = db.Column(db.String(20))
    language = db.Column(db.String(50))

    def __init__(self, phone_number=None, language=None):
        self.phone_number = phone_number
        self.language = language


@app.route('/updateuser/<int:user_id>', methods=['PUT'])
def update_user_profile(user_id):
    try:
        user_profile = UserProfile.query.get(user_id)
        if not user_profile:
            return jsonify({'error': 'User profile not found'}), 404

        data = request.json
        if 'phone_number' in data:
            user_profile.phone_number = str(data['phone_number'])
        if 'language' in data:
            user_profile.language = data['language']

        db.session.commit()
        return jsonify({'message': 'User profile updated successfully'}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
    
    
# Define the Farm model
class Farm(db.Model):
    __tablename__ = 'farms'
    farm_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    farm_name = db.Column(db.String(255))
    location = db.Column(db.String(255))
    size = db.Column(db.String(255))
    soil_type = db.Column(db.String(255))
    climate_zone = db.Column(db.String(255))

    def __init__(self, user_id, farm_name, location, size, soil_type, climate_zone):
        self.user_id = user_id
        self.farm_name = farm_name
        self.location = location
        self.size = size
        self.soil_type = soil_type
        self.climate_zone = climate_zone

# API endpoint to insert data into the "farms" table
@app.route('/farm', methods=['POST'])
def insert_farm_data():
    try:
        data = request.json
        new_farm = Farm(
            user_id=data['user_id'],
            farm_name=data['farm_name'],
            location=data['location'],
            size=data['size'],
            soil_type=data['soil_type'],
            climate_zone=data['climate_zone']
        )
        db.session.add(new_farm)
        db.session.commit()
        return jsonify({'message': 'Farm data inserted successfully'}), 201
    except KeyError as e:
        return jsonify({'error': f'Missing required field: {e}'}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
    
    
    
# API endpoint to get farms belonging to a specific user
@app.route('/farms/<int:user_id>', methods=['GET'])
def get_user_farms(user_id):
    try:
        # Query the database to retrieve farms belonging to the specified user
        user_farms = Farm.query.filter_by(user_id=user_id).all()

        # If no farms are found for the user, return a 404 error
        if not user_farms:
            return jsonify({'error': 'No farms found for the user'}), 404

        # Serialize the farms data
        farms_data = []
        for farm in user_farms:
            farm_data = {
                'farm_id': farm.farm_id,
                'farm_name': farm.farm_name,
                'location': farm.location,
                'size': farm.size,
                'soil_type': farm.soil_type,
                'climate_zone': farm.climate_zone
            }
            farms_data.append(farm_data)

        # Return the farms data as JSON
        return jsonify({'farms': farms_data}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
    

@app.route('/deletefarm/<int:farm_id>', methods=['DELETE'])
def delete_farm(farm_id):
    try:
        farm = Farm.query.get(farm_id)
        if farm:
            db.session.delete(farm)
            db.session.commit()
            return jsonify({'message': 'Farm deleted successfully'}), 200
        else:
            return jsonify({'error': 'Farm not found'}), 404
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
 
 
 
class Feedback(db.Model):
    __tablename__ = 'feedback'
    feedback_Id = db.Column(db.Integer, primary_key=True)
    reccomenadtion_id = db.Column(db.Integer)
    user_id = db.Column(db.Integer)
    feedback_text = db.Column(db.Text)
    feedback_date = db.Column(db.TIMESTAMP, default=lambda: datetime.now(timezone.utc))

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}   
    
    


@app.route('/feedback', methods=['POST', 'OPTIONS'])
def create_feedback():
    if request.method == 'OPTIONS':
        response = app.make_default_options_response()
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
        response.headers['Access-Control-Allow-Methods'] = 'POST'
        return response
    
    data = request.json
    # Remove feedback_date from the request data if present
    data.pop('feedback_date', None)
    
    new_feedback = Feedback(**data)
    try:
        db.session.add(new_feedback)
        db.session.commit()
        return jsonify({'message': 'Feedback created successfully'}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400



if __name__ == "__main__":
    app.run(debug=True,port=8080)
