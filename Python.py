
import os
import sys
from dotenv import load_dotenv
import requests_pkcs12

def load_environment():
    """
    Load environment variables from a .env file.
    """
    # Load variables from .env file if it exists
    load_dotenv()

    # Retrieve variables
    pfx_path = os.getenv('PFX_PATH')
    pfx_password = os.getenv('PFX_PASSWORD')
    auth_token = os.getenv('AUTH_TOKEN')
    api_url = os.getenv('API_URL')

    # Validate required variables
    missing_vars = []
    if not pfx_path:
        missing_vars.append('PFX_PATH')
    if not pfx_password:
        missing_vars.append('PFX_PASSWORD')
    if not auth_token:
        missing_vars.append('AUTH_TOKEN')
    if not api_url:
        missing_vars.append('API_URL')

    if missing_vars:
        print(f"Error: Missing environment variables: {', '.join(missing_vars)}")
        sys.exit(1)

    return pfx_path, pfx_password, auth_token, api_url

def make_get_request(pfx_path, pfx_password, auth_token, api_url):
    """
    Make an authenticated GET request using a .pfx client certificate.
    """
    # Define headers
    headers = {
        'Authorization': f'Bearer {auth_token}',
        'Accept': 'application/json',
        'X-Custom-Header': 'CustomValue'  # Replace or add more headers as needed
    }

    try:
        # Make the GET request with client certificate
        response = requests_pkcs12.get(
            api_url,
            headers=headers,
            pkcs12_filename=pfx_path,
            pkcs12_password=pfx_password,
            verify=True  # Set to False to skip SSL verification (not recommended)
        )

        # Check the response status
        if response.status_code == 200:
            print('Success:', response.json())
        else:
            print(f'Error: {response.status_code}')
            print('Response Body:', response.text)

    except requests_pkcs12.exceptions.SSLError as ssl_err:
        print('SSL Error:', ssl_err)
    except requests_pkcs12.exceptions.ConnectionError as conn_err:
        print('Connection Error:', conn_err)
    except Exception as e:
        print('An unexpected error occurred:', e)

def main():
    # Load environment variables
    pfx_path, pfx_password, auth_token, api_url = load_environment()

    # Make the GET request
    make_get_request(pfx_path, pfx_password, auth_token, api_url)

if __name__ == "__main__":
    main()
