from flask import Flask, request, jsonify
from flask_cors import CORS
import random

# Create Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Mock database of marks for 100 students
students_marks = {f"Student_{i}": random.randint(0, 100) for i in range(1, 101)}

@app.route('/api', methods=['GET'])
def get_marks():
    names = request.args.getlist('name')  # Get list of names from query parameters
    marks = []

    # For each name in the request, get their marks
    for name in names:
        marks.append(students_marks.get(name, 'Not found'))

    return jsonify({"marks": marks})

if __name__ == "__main__":
    app.run(debug=True)
