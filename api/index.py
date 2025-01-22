import json
import os
from http.server import BaseHTTPRequestHandler

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Read the query parameters
        query = self.path.split('?')[1] if '?' in self.path else ''
        params = dict(q.split('=') for q in query.split('&')) if query else {}
        
        # Read the JSON data from the file
        try:
            with open(os.path.join(os.path.dirname(__file__), '..', 'q-vercel-python.json'), 'r') as file:
                marks_data = json.load(file)
        except FileNotFoundError:
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"error": "Data file not found"}).encode('utf-8'))
            return

        # Extract the names from the query parameters
        names = params.get('name', '').split(',')

        # Find the marks for each name
        result = {"marks": []}
        for name in names:
            # Search for the name in the marks_data
            match = next((entry for entry in marks_data if entry['name'] == name), None)
            result["marks"].append(match['marks'] if match else 'Not Found')

        # Send the response
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')  # Allow all origins (CORS)
        self.end_headers()
        
        # Send the JSON response
        self.wfile.write(json.dumps(result).encode('utf-8'))
