from flask import Flask, request, jsonify
from datetime import datetime
import requests

app = Flask(__name__)

NODE_2_URL = 'http://10.10.1.3:8805'  # Replace with actual Node 2 URL

# Endpoint to act as a proxy for Node 2
@app.route('/proxy/<path:url>', methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH'])
def proxy(url):
    data = request.json if request.method in ['POST', 'PUT', 'PATCH'] else None
    method = request.method
    timestamp = datetime.now().isoformat()
    
    # Log the incoming request
    print(f"Middlebox received request for Node 2 at {timestamp}: {request.method}")
    
    # Forward the request to Node 2
    response = requests.request(
        method,
        f'{NODE_2_URL}/{url}',
        json=data,
        headers={key: value for key, value in request.headers if key != 'Host'}
    )
    
    # Log the response
    response_timestamp = datetime.now().isoformat()
    print(f"Middlebox received response from Node 2 at {response_timestamp}: {response.status_code}")
    
    # Forward the response back to Node 1
    return (response.content, response.status_code, response.headers.items())

if __name__ == '__main__':
    app.run(host='10.10.1.1',port=8805)
