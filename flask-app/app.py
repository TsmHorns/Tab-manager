from flask import Flask, jsonify, request
from flask_cors import CORS  # Import CORS
import json
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Function to load URLs from the JSON file
def load_urls_from_file():
    try:
        with open('tabs.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return []

# Function to write URLs to a JSON file (recreating the file each time)
def write_urls_to_file(urls):
    with open('tabs.json', 'w') as f:
        json.dump(urls, f)

# Initialize the open_tab_urls list with URLs from the JSON file
open_tab_urls = load_urls_from_file()

# Route to get all stored URLs
@app.route('/api/get-urls', methods=['GET'])
def get_urls():
    """
    Endpoint to fetch all URLs stored in Chrome storage.
    """
    current_urls = load_urls_from_file()
    return jsonify(current_urls)

# Route to save URLs received from Chrome extension
@app.route('/api/save-urls', methods=['POST'])
def save_urls():
    """
    Endpoint to receive and save URLs from Chrome extension.
    """
    data = request.json
    new_urls = data.get('urls', [])
    
    # Load current state of open_tab_urls from file
    current_urls = load_urls_from_file()
    
    # Append new URLs to the list if they are not already present
    for url in new_urls:
        if url not in current_urls:
            open_tab_urls.append(url)
    
    # Write updated URLs to JSON file (recreating the file)
    write_urls_to_file(open_tab_urls)
    
    return jsonify({"message": "URLs saved successfully"})

# Route to handle tab closure events
@app.route('/api/tab-closed/<int:tab_id>', methods=['DELETE'])
def tab_closed(tab_id):
    """
    Endpoint to handle tab closure events.
    """
    global open_tab_urls
    
    # Load current state of open_tab_urls from file
    current_urls = load_urls_from_file()
    
    # Remove the closed tab's URL from open_tab_urls if present
    open_tab_urls = [url for url in current_urls if url.get('tabId') != tab_id]
    
    # Write updated URLs to JSON file (recreating the file)
    write_urls_to_file(open_tab_urls)
    
    return jsonify({"message": f"Tab ID {tab_id} closed successfully"})

if __name__ == '__main__':
    app.run(debug=True)