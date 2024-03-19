
import requests
import base64
import config

# Replace with your actual application credentials
client_id = config.client_id
client_secret = config.client_secret

# Replace with the short-lived access token you have
access_token = config.access_token

# Endpoint for obtaining a new access token
token_endpoint = "https://api.ebay.com/identity/v1/oauth2/token"

# Headers for the request
headers = {
    "Authorization": f"Basic {base64.b64encode(f'{client_id}:{client_secret}'.encode('utf-8')).decode('utf-8')}",
    "Content-Type": "application/x-www-form-urlencoded"
}

# Data for the request body
data = {
    "grant_type": "client_credentials",
    "scope": "https://api.ebay.com/oauth/api_scope"  # Replace with the required scope(s)
}

# Send the POST request to obtain a new access token
response = requests.post(token_endpoint, headers=headers, data=data)

# Check for successful response (200 OK)
# After obtaining the new access token
if response.status_code == 200:
    new_access_token = response.json()["access_token"]
   # print("Successfully obtained a new access token:", new_access_token)
    
    # Update ebay_bearer_token in config.py
    config.ebay_bearer_token = new_access_token
    
    # Read existing configurations
    with open('config.py', 'r') as config_file:
        config_lines = config_file.readlines()
    
    # Update ebay_bearer_token and facebook_access_token in config.py
    with open('config.py', 'w') as config_file:
        for line in config_lines:
            if line.startswith("ebay_bearer_token"):
                config_file.write(f"ebay_bearer_token = '{config.ebay_bearer_token}'\n")
            elif line.startswith("facebook_access_token"):
                config_file.write(f"facebook_access_token = '{config.facebook_access_token}'\n")
            else:
                config_file.write(line)
#else:
    #print("Error obtaining new access token:", response.text)
    
    
    
