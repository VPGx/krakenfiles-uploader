import requests
import argparse

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
    
    # Print the URL and server access token
    print(f"url: {serverurl}")
    print(f"serverAccessToken: {server_access_token}")
else:
    print(f'Request failed with status code {response.status_code}')

# Step 2: Upload a file to the server using the server access token

parser = argparse.ArgumentParser(description='Upload a file to the KrakenFiles server.')
parser.add_argument('file_path', metavar='file_path', type=str, help='The path to the file to upload')

args = parser.parse_args()

file_path = args.file_path
file_name = file_path.split('/')[-1] # Extract the filename from the file path
upload_url = f"{serverurl}"

headers = {
    # ADD YOUR AUTHORIZATION TOKEN FROM KRAKENFILES PANEL BELOW :: https://krakenfiles.com/profile/api-access
    'X-AUTH-TOKEN': "AUTH TOKEN"
}

with open(file_path, 'rb') as f:
    files = {'file': (file_name, f)}
    data = {'serverAccessToken': server_access_token}
    response = requests.post(upload_url, headers=headers, data=data, files=files)

if response.status_code == 200:
    print('File upload successful')
else:
    print(f'File upload failed with status code {response.status_code}')
