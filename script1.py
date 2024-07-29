import requests
from datetime import datetime
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import uuid
import json

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://wrDB_owner:qEG4P1mKAVZl@ep-falling-tree-a5x4yzg3.us-east-2.aws.neon.tech/wrDB?sslmode=require"
db = SQLAlchemy(app)
migrate = Migrate(app, db)

class Retreat(db.Model):
    id = db.Column(db.String, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    location = db.Column(db.String(255), nullable=False)
    price = db.Column(db.Float, nullable=False)
    type = db.Column(db.String(50), nullable=False)
    condition = db.Column(db.String(50), nullable=False)
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

def fetch_and_add_retreats(api_url):
    response = requests.get(api_url)
    retreats = response.json()
    
    for retreat in retreats:
        new_retreat = Retreat(
            id=retreat["id"],
            title=retreat["title"],
            description=retreat["description"],
            date=retreat["date"],
            location=retreat["location"],
            price=retreat["price"],
            type=retreat["type"],
            condition=retreat["condition"],
            image=retreat["image"],
            tags=retreat["tag"],
            duration=retreat["duration"]
        )
        db.session.add(new_retreat)
    
    db.session.commit()
    print("Retreats added successfully!")

if __name__ == "__main__":
    with app.app_context():
        api_url = "https://669f704cb132e2c136fdd9a0.mockapi.io/api/v1/retreats"
        fetch_and_add_retreats(api_url)
