"""class User(db.Model):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    first_name = db.Column(db.String(255))
    last_name = db.Column(db.String(255))
    email = db.Column(db.String(255), unique=True)
   

    def __init__(self, username, password, first_name, last_name, email):
        self.username = username
        self.password = generate_password_hash(password)
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
    """ 


"""
@app.route('/signup', methods=['POST', 'OPTIONS'])
def signup():
    if request.method == 'OPTIONS':
        # Respond to the CORS preflight request
        return '', 204

    data = request.get_json()
    if not all(key in data for key in ['username', 'password', 'first_name', 'last_name', 'email']):
        return jsonify({'message': 'Missing parameters'}), 400

    if User.query.filter_by(username=data['username']).first():
        return jsonify({'message': 'Username already exists'}), 400

    if User.query.filter_by(email=data['email']).first():
        return jsonify({'message': 'Email already registered'}), 400
    #hashed_password = generate_password_hash(data['password'])
    hashed_password = generate_password_hash(str(data['password']))
    new_user = User(
        username=data['username'],
        password= hashed_password,
        first_name=data['first_name'],
        last_name=data['last_name'],
        email=data['email']
    )
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User registered successfully'})



"""

"""
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    
    if not all(key in data for key in ['email', 'password']):
        return jsonify({'message': 'Missing parameters'}), 400

    # Attempt to retrieve the user based on email
    user = User.query.filter_by(email=data['email']).first()
    
    print("user found")

    if not user:
        # User not found
        print("Invalid User Name")
        return jsonify({'message': 'User not found'}), 404
    
    # Debug print statements
    print("Stored Password:", user.password)
    print("Entered Password:", str(data['password']))

    if not check_password_hash(user.password, str(data['password'])):
        # Incorrect password
        print("Invalid Password")
        return jsonify({'message': 'Invalid password'}), 401

    # Login successful
    return jsonify({'message': 'Login successful', 'user_id': user.user_id})




"""

"""
@app.route('/varieties', methods=['GET'])
def get_varieties():
    crop_name = request.args.get('cropname')
    duration_to_maturity = request.args.get('durationtomaturitymonths')
    optimal_production_altitude = request.args.get('optimalproductionaltitude')

    if not all([crop_name, duration_to_maturity, optimal_production_altitude]):
        return jsonify({'error': 'Missing required parameters'}), 400

    try:
        altitude_range = optimal_production_altitude.split('-')
        lower_altitude = int(altitude_range[0])
        upper_altitude = int(altitude_range[1])

        varieties = Variety.query.filter(
            Variety.cropname == crop_name,
            Variety.durationtomaturitymonths == int(duration_to_maturity),
            db.func.cast(db.func.substring(Variety.optimalproductionaltitude, 1, db.func.strpos(Variety.optimalproductionaltitude, '-') - 1), db.Integer) >= lower_altitude,
            db.func.cast(db.func.substring(Variety.optimalproductionaltitude, db.func.strpos(Variety.optimalproductionaltitude, '-') + 1), db.Integer) <= upper_altitude
        ).all()

        return jsonify([variety.to_dict() for variety in varieties])

    except Exception as e:
        return jsonify({'error': str(e)}), 500




"""

"""
    
@app.route('/varieties', methods=['GET'])
def get_varieties():
    try:
        
        varieties = Variety.query.all()

        
        for variety in varieties:
            cropname = variety.cropname
            if cropname not in varieties_by_crop:
                varieties_by_crop[cropname] = []
            varieties_by_crop[cropname].append(variety.to_dict())

        return jsonify(varieties_by_crop)
    except Exception as e:
        return jsonify({"error":str(e)}),500



"""