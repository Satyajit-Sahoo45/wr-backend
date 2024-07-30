from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from os import environ
from flask_cors import CORS
import uuid
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_migrate import Migrate
import json
import requests
import jwt
import datetime
from dateutil import parser


app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get("DB_URL")
db = SQLAlchemy(app)
migrate = Migrate(app, db)
SECRET_KEY = environ.get("DB_URL")

class User(db.Model):
    id = db.Column(db.String, primary_key=True, default=lambda: str(uuid.uuid4()))
    username = db.Column(db.String(255), unique=True, nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)

class Retreat(db.Model):
    id = db.Column(db.String, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    location = db.Column(db.String(255), nullable=False)
    price = db.Column(db.Float, nullable=False)
    type = db.Column(db.String(255), nullable=False)
    condition = db.Column(db.String(255), nullable=False)
    image = db.Column(db.String(255), nullable=True)
    tags = db.Column(db.Text, nullable=True)
    duration = db.Column(db.Integer, nullable=False)

    def __init__(self, id, title, description, date, location, price, type, condition, image, tags, duration):
        self.id = id
        self.title = title
        self.description = description
        self.date = datetime.fromtimestamp(date)
        self.location = location
        self.price = price
        self.type = type
        self.condition = condition
        self.image = image
        self.tags = json.dumps(tags)
        self.duration = duration

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'date': self.date.isoformat(),
            'location': self.location,
            'price': self.price,
            'type': self.type,
            'condition': self.condition,
            'image': self.image,
            'tags': json.loads(self.tags),
            'duration': self.duration
        }

class Booking(db.Model):
    id = db.Column(db.String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.String)
    user_name = db.Column(db.String(255))
    user_email = db.Column(db.String(255))
    user_phone = db.Column(db.String(255))
    retreat_id = db.Column(db.String, db.ForeignKey('retreat.id'))
    retreat_title = db.Column(db.String(255))
    retreat_location = db.Column(db.String(255))
    retreat_price = db.Column(db.Numeric)
    retreat_duration = db.Column(db.String(255))
    payment_details = db.Column(db.Text)
    booking_date = db.Column(db.Date)

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'user_name': self.user_name,
            'user_email': self.user_email,
            'user_phone': self.user_phone,
            'retreat_id': self.retreat_id,
            'retreat_title': self.retreat_title,
            'retreat_location': self.retreat_location,
            'retreat_price': self.retreat_price,
            'payment_details': self.payment_details,
            'booking_date': self.booking_date
        }

@app.route('/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    if User.query.filter_by(email=email).first():
        return jsonify({"message": "Email already exists"}), 409
    hashed_password = generate_password_hash(password)
    new_user = User(username=username, email=email, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "User registered successfully!"}), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    print(data)
    email = data.get('email')
    password = data.get('password')
    user = User.query.filter_by(email=email).first()
    if user and check_password_hash(user.password, password):
        token_payload = {
            'user_id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
        }
        access_token = jwt.encode(token_payload, SECRET_KEY, algorithm='HS256')
        user_data = {
            'id': user.id,
            'email': user.email,
            'username': user.username,
        }
        return jsonify({
            'message': 'Login successful!',
            'access_token': access_token,
            'user_data': user_data
        }), 200
    else:
        return jsonify({"message": "Invalid credentials"}), 401

@app.route('/retreats', methods=['GET'])
def get_retreats():
    retreats = Retreat.query.all()
    return jsonify([retreat.to_dict() for retreat in retreats])

@app.route('/retreats/<string:id>', methods=['GET'])
def get_retreat(id):
    retreat = Retreat.query.get(id)
    if retreat:
        return jsonify(retreat.to_dict())
    return jsonify({'message': 'Retreat not found'}), 404

@app.route('/book', methods=['POST'])
def book_retreat():
    data = request.get_json()
    try:
        required_fields = ['user_id', 'user_name', 'user_email', 'user_phone', 'retreat_id', 'retreat_title', 'retreat_location', 'retreat_price', 'retreat_duration', 'payment_details', 'booking_date']
        for field in required_fields:
            if field not in data:
                return jsonify({'message': f'Missing field: {field}'}), 400

        booking = Booking(
            user_id=data['user_id'],
            user_name=data['user_name'],
            user_email=data['user_email'],
            user_phone=data['user_phone'],
            retreat_id=data['retreat_id'],
            retreat_title=data['retreat_title'],
            retreat_location=data['retreat_location'],
            retreat_price=data['retreat_price'],
            retreat_duration=data['retreat_duration'],
            payment_details=data['payment_details'],
            booking_date=parser.parse(data['booking_date']).date()
        )
        db.session.add(booking)
        db.session.commit()
        return jsonify({'message': 'Booking successful'}), 201
    except Exception as e:
        print(f"Error occurred: {e}")
        return jsonify({'message': 'Internal Server Error'}), 500


@app.route('/bookings', methods=['GET'])
def get_user_bookings():
    user_id = request.args.get('user_id')
    bookings = Booking.query.filter_by(user_id=user_id).all()
    return jsonify([booking.to_dict() for booking in bookings])

@app.route('/', methods=['GET'])
def test():
    return jsonify({'message': 'Server Running..'}), 201

if __name__ == '__main__':
    app.run(debug=True)
