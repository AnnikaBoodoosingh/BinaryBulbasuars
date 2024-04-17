from werkzeug.security import check_password_hash, generate_password_hash
from App.database import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username =  db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String(120), nullable=False)

    def __init__(self, username, password):
        self.username = username
        self.set_password(password)

    def get_json(self):
        return{
            'id': self.id,
            'username': self.username
        }

    def set_password(self, password):
        """Create hashed password."""
        self.password = generate_password_hash(password)
    
    def check_password(self, password):
        """Check hashed password."""
        return check_password_hash(self.password, password)

class Workout(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title =  db.Column(db.String)
    description = db.Column(db.String)
    type = db.Column(db.String)
    body_part = db.Column(db.String)
    equipment = db.Column(db.String)
    level = db.Column(db.Float)
    rating = db.Column(db.Float)
    rating_desc = db.Column(db.String)

    def __init__(self, id, title, description, type, body_part, equipment, level, rating, rating_desc):
        self.id = id
        self.title = title
        self.description = description
        self.type = type
        self.body_part = body_part
        self.equipment = equipment
        self.level = level
        self.rating = rating
        self.rating_desc = rating_desc

