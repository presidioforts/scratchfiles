


import json
import requests_pkcs12

def make_post_request(pfx_path, pfx_password, api_url, payload):
    """
    Make a POST request using a PFX (PKCS#12) client certificate.
    Returns a dict with (url, status_code, response_data) or (url, status_code, error_message).
    """

    # Define the headers you need (two in this example)
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    }

    try:
        # Make the POST request with client certificate
        response = requests_pkcs12.post(
            url=api_url,
            headers=headers,
            data=json.dumps(payload),          # or use json=payload if your library supports it
            pkcs12_filename=pfx_path,
            pkcs12_password=pfx_password,
            verify=True    # set to False to skip SSL verification (not recommended)
        )

        # Check the response status
        if response.status_code in (200, 201):
            return {
                'url': response.url,
                'status_code': response.status_code,
                'response_data': response.json()  # or response.text, depending on the API
            }
        else:
            return {
                'url': response.url,
                'status_code': response.status_code,
                'error_message': response.text
            }

    except requests_pkcs12.exceptions.SSLError as ssl_err:
        return {'error': f'SSL Error: {str(ssl_err)}'}

    except requests_pkcs12.exceptions.ConnectionError as conn_err:
        return {'error': f'Connection Error: {str(conn_err)}'}

    except Exception as e:
        return {'error': f'Unexpected Error: {str(e)}'}
