# Basic Render-compatible backend server
from flask import Flask
app = Flask(__name__)

@app.route('/')
def home():
    return 'Hello from base backend!'