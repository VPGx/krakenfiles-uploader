import requests
import argparse
import os
import configparser

# Step 1: Send a GET request to the API endpoint to check server availability

headers = {
    'Accept': 'application/json'
}

response = requests.get('https://krakenfiles.com/api/server/available', headers=headers)

if response.status_code == 200:
    data = response.json()

    # Extract the URL and server access token from the API response
    serverurl = data['data']['url']
    server_access_token = data['data']['serverAccessToken']

else:
    print(f'Request failed with status code {response.status_code}')

# Step 2: Upload a file to the server using the server access token

parser = argparse.ArgumentParser(description='Upload a file to the KrakenFiles server.')
parser.add_argument('file_path', metavar='file_path', type=str, help='The path to the file to upload')

args = parser.parse_args()

file_path = args.file_path

if not os.path.exists(file_path):
    print(f'Error: File not found at path {file_path}')
    exit(1)

file_name = file_path.split('/')[-1] # Extract the filename from the file path
upload_url = f"{serverurl}"

config = configparser.ConfigParser()
if os.path.exists('config.ini'):
    config.read('config.ini')
if 'krakenfiles' in config and 'X-AUTH-TOKEN' in config['krakenfiles']:
    auth_token = config['krakenfiles']['X-AUTH-TOKEN']
else:
    auth_token = input('Please enter your KrakenFiles X-AUTH-TOKEN: ')
    config['krakenfiles'] = {'X-AUTH-TOKEN': auth_token}
    with open('config.ini', 'w') as configfile:
        config.write(configfile)

if not auth_token:
    print('Error: X-AUTH-TOKEN not set.')
    exit(1)

headers = {
    'X-AUTH-TOKEN': auth_token
}

with open(file_path, 'rb') as f:
    files = {'file': (file_name, f)}
    data = {'serverAccessToken': server_access_token}
    response = requests.post(upload_url, headers=headers, data=data, files=files)
    uploaddata = response.json()

if response.status_code == 200:
    fileurl = uploaddata['data']['url']
    filesize = uploaddata['data']['size']
    file_size_mb = round(float(filesize) / (1024 * 1024), 2)
    print(f"File Uploaded at: {fileurl} with {file_size_mb} MB")

    with open("uploaded_files.txt", "a") as f:
        f.write(f"{file_name}, {fileurl}, {file_size_mb} MB\n")

else:
    print(f'File upload failed with status code {response.status_code}')
