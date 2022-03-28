# Import dependencies
from flask import Flask

# Create new Flask instance called app
app = Flask(__name__)

# Create route in Flask
@app.route('/')
def hello_world():
    return "Hello world"