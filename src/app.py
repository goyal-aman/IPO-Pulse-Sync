import os
import subprocess
import base64
import requests
from datetime import datetime
from flask import Flask
# ARGS
GHTOKEN = os.environ['GHTOKEN'] 
IPO_PULSE_PARSER_BASE_URL = os.environ["IPO_PULSE_PARSER_BASE_URL"] 

# Constants
GITHUB_API_URL = 'https://api.github.com'
REPO = 'goyal-aman/ipo-pulse-ui'  # Replace with your GitHub username and repository name
GENERATED_FILE_NAME = 'index.html'  # The name of the generated file
BRANCH = 'main'  # Change this to your default branch


def run_command(command):
    """Run a shell command."""
    try:
        subprocess.run(command, check=True, shell=True)
        print(f"Command '{command}' executed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error occurred while executing command: {e}")

def upload_file_to_github():
    """Upload the generated HTML file to the GitHub repository."""
    # Check if the file exists
    if not os.path.isfile(GENERATED_FILE_NAME):
        print(f"{GENERATED_FILE_NAME} does not exist.")
        return

    with open(GENERATED_FILE_NAME, 'rb') as f:
        content = f.read()

    # Encode the file content to Base64
    encoded_content = base64.b64encode(content).decode()

    # API endpoint for creating/updating a file
    url = f'{GITHUB_API_URL}/repos/{REPO}/contents/{GENERATED_FILE_NAME}'

    # Check if the file already exists
    response = requests.get(url, headers={'Authorization': f'token {GHTOKEN}'})

    if response.status_code == 200:
        # If the file exists, we need to update it
        sha = response.json().get('sha')
        data = {
            'message': f"Update generated HTML file {datetime.now()}",
            'content': encoded_content,
            'sha': sha,
            'branch': BRANCH
        }
        response = requests.put(url, json=data, headers={'Authorization': f'token {GHTOKEN}'})
    else:
        # If the file does not exist, we can create it
        data = {
            'message': 'Create generated HTML file',
            'content': encoded_content,
            'branch': BRANCH
        }
        response = requests.put(url, json=data, headers={'Authorization': f'token {GHTOKEN}'})

    if response.status_code in (200, 201):
        print('File uploaded successfully!')
    else:
        print(f'Error uploading file: {response.content}')

def upload_file_to_github_v2(html_str):
    """Upload the generated HTML file to the GitHub repository."""
    # Encode the file content to Base64
    encoded_content = base64.b64encode(html_str.encode('utf-8')).decode()

    # API endpoint for creating/updating a file
    url = f'{GITHUB_API_URL}/repos/{REPO}/contents/{GENERATED_FILE_NAME}'

    # Check if the file already exists
    response = requests.get(url, headers={'Authorization': f'token {GHTOKEN}'})

    if response.status_code == 200:
        # If the file exists, we need to update it
        sha = response.json().get('sha')
        data = {
            'message': f"Update generated HTML file {datetime.now()}",
            'content': encoded_content,
            'sha': sha,
            'branch': BRANCH
        }
        response = requests.put(url, json=data, headers={'Authorization': f'token {GHTOKEN}'})
    else:
        # If the file does not exist, we can create it
        data = {
            'message': 'Create generated HTML file',
            'content': encoded_content,
            'branch': BRANCH
        }
        response = requests.put(url, json=data, headers={'Authorization': f'token {GHTOKEN}'})

    if response.status_code in (200, 201):
        print('File uploaded successfully!')
    else:
        print(f'Error uploading file: {response.content}')
    return "success"

    

app = Flask(__name__)

@app.route('/api/sync', methods=['GET'])
def sync():
    response = response = requests.get(IPO_PULSE_PARSER_BASE_URL+"/api/html")
    return upload_file_to_github_v2(response.json().get('data'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5680)

