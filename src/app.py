import os
import subprocess
import base64
import requests
from datetime import datetime

# ARGS
TOKEN = os.environ['TOKEN'] 
# IPO_PULSE_API_BASE_URL = os.environ['IPO_PULSE_API_BASE_URL']


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
    response = requests.get(url, headers={'Authorization': f'token {TOKEN}'})

    if response.status_code == 200:
        # If the file exists, we need to update it
        sha = response.json().get('sha')
        data = {
            'message': f"Update generated HTML file {datetime.now()}",
            'content': encoded_content,
            'sha': sha,
            'branch': BRANCH
        }
        response = requests.put(url, json=data, headers={'Authorization': f'token {TOKEN}'})
    else:
        # If the file does not exist, we can create it
        data = {
            'message': 'Create generated HTML file',
            'content': encoded_content,
            'branch': BRANCH
        }
        response = requests.put(url, json=data, headers={'Authorization': f'token {TOKEN}'})

    if response.status_code in (200, 201):
        print('File uploaded successfully!')
    else:
        print(f'Error uploading file: {response.content}')

if __name__ == '__main__':
    # Run the command to generate the HTML file
    # command_to_run = f'sudo docker run -e BASE_URL={IPO_PULSE_API_BASE_URL} -v $PWD:/app/generated amangoyal8110/ipo-pulse-parser:latest'  # Replace with your actual command
    # run_command(command_to_run)
    
    # Upload the generated file to GitHub
    upload_file_to_github()
