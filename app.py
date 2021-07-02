
from enum import unique
from flask import Flask, request, jsonify
from datetime import datetime
import bcrypt
from flask_sqlalchemy import SQLAlchemy , sqlalchemy
from sqlalchemy.exc import IntegrityError
from flask_marshmallow import Marshmallow 
import os

# Init app
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
# Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Init db
db = SQLAlchemy(app)
# Init ma
ma = Marshmallow(app)


class File(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    size = db.Column(db.Text, nullable=False)
    created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('file', lazy=True))

    def __init__(self, name, size, user_id):
        self.name = name
        self.size = size
        self.user_id = user_id

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(50), nullable=False)

    def __init__(self, username, password):
        self.username = username
        self.password = password
    

db.create_all()

# Product Schema
class FileSchema(ma.Schema):
  class Meta:
    fields = ('id', 'name',  'size', 'created')

class UserSchema(ma.Schema):
  class Meta:
    fields = ('id', 'username',  'password')


# Init schema
file_schema = FileSchema()
files_schema = FileSchema(many=True)

user_schema = FileSchema()


@app.route('/api/signup', methods=['POST'])
def signup():
    try:
        username = request.json['username']
        password = request.json['password']
        hashed_password = bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt())
        new_user = User(username, hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return user_schema.jsonify(new_user)
    except IntegrityError:
        return jsonify({'error':'User Already Exists'})


# Run Server
if __name__ == '__main__':
  app.run(debug=True)