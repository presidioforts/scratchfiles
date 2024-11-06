
import os
import sys
import json
from dotenv import load_dotenv
import requests_pkcs12
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm

def load_environment():
    """
    Load environment variables from a .env file and read endpoints from a file.
    """
    # Load variables from .env file if it exists
    load_dotenv()

    # Retrieve variables
    pfx_path = os.getenv('PFX_PATH')
    pfx_password = os.getenv('PFX_PASSWORD')
    auth_token = os.getenv('AUTH_TOKEN')
    endpoints_file = os.getenv('ENDPOINTS_FILE')
    output_file = os.getenv('OUTPUT_FILE', 'responses.json')  # Default to 'responses.json' if not set

    # Validate required variables
    missing_vars = []
    if not pfx_path:
        missing_vars.append('PFX_PATH')
    if not pfx_password:
        missing_vars.append('PFX_PASSWORD')
    if not auth_token:
        missing_vars.append('AUTH_TOKEN')
    if not endpoints_file:
        missing_vars.append('ENDPOINTS_FILE')

    if missing_vars:
        print(f"Error: Missing environment variables: {', '.join(missing_vars)}")
        sys.exit(1)

    # Read endpoints from the file
    try:
        with open(endpoints_file, 'r') as f:
            endpoints = [line.strip() for line in f if line.strip() and not line.startswith('#')]
    except FileNotFoundError:
        print(f"Error: The endpoints file '{endpoints_file}' was not found.")
        sys.exit(1)
    except Exception as e:
        print(f"Error reading endpoints file: {e}")
        sys.exit(1)

    return pfx_path, pfx_password, auth_token, endpoints, output_file

def make_get_request(pfx_path, pfx_password, auth_token, api_url):
    """
    Make an authenticated GET request using a .pfx client certificate.
    Returns a tuple of (url, status_code, response_data or error_message).
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
            return (api_url, response.status_code, response.json())
        else:
            return (api_url, response.status_code, response.text)

    except requests_pkcs12.exceptions.SSLError as ssl_err:
        return (api_url, 'SSL Error', str(ssl_err))
    except requests_pkcs12.exceptions.ConnectionError as conn_err:
        return (api_url, 'Connection Error', str(conn_err))
    except Exception as e:
        return (api_url, 'Unexpected Error', str(e))

def save_responses(responses, output_file='responses.json'):
    """
    Save the responses dictionary to a JSON file.
    """
    try:
        with open(output_file, 'w') as f:
            json.dump(responses, f, indent=4)
        print(f"\nAll responses have been saved to '{output_file}'.")
    except Exception as e:
        print(f"Error saving responses to file: {e}")

def main():
    # Load environment variables and endpoints
    pfx_path, pfx_password, auth_token, endpoints, output_file = load_environment()

    # Dictionary to store responses
    responses = {}

    # Define the number of workers (threads). Adjust based on your system and API rate limits.
    max_workers = 10

    print(f"Starting requests to {len(endpoints)} endpoints with {max_workers} workers...\n")

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Submit all requests to the executor
        future_to_url = {
            executor.submit(make_get_request, pfx_path, pfx_password, auth_token, url): url
            for url in endpoints
        }

        # Use tqdm to display a progress bar
        for future in tqdm(as_completed(future_to_url), total=len(future_to_url), desc="Processing"):
            url = future_to_url[future]
            try:
                api_url, status, data = future.result()
                responses[api_url] = {
                    'status': status,
                    'data': data
                }
                print(f"Completed: {api_url} - Status: {status}")
            except Exception as e:
                responses[url] = {
                    'status': 'Exception',
                    'data': str(e)
                }
                print(f"Exception for {url}: {e}")

    # After all requests are done, save the responses
    save_responses(responses, output_file)

if __name__ == "__main__":
    main()
