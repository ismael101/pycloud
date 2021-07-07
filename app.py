from flask import Flask
from auth import auth
from file import file


app = Flask(__name__)
app.register_blueprint(auth)
app.register_blueprint(file)

if __name__ == '__main__':
  app.run(debug=True)