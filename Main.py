if __name__ == "__main__":
    pfx_path = "path/to/certificate.p12"
    pfx_password = "yourPFXpassword"
    api_url = "https://your-api-endpoint.com/resource"
    payload = {
        "key1": "value1",
        "key2": "value2"
    }

    result = make_post_request(pfx_path, pfx_password, api_url, payload)
    print(result)
