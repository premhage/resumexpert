from flask import Flask
from flask_cors import CORS
from flask_restful import Api
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

app = Flask(__name__)
# Enable CORS for all domains
CORS(app)
api = Api(app)

# Placeholder for route registration
@app.route('/')
def home():
    return {"message": "ResumeXpert API is running"}

if __name__ == '__main__':
    app.run(debug=True, port=5000)
