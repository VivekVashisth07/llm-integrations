import requests

def validate_openai_api_key(api_key: str) -> dict:
    """
    Validates the given OpenAI API key.
    
    Returns a dictionary with:
    - message: Status message of the validation.
    - error: Error details, if any.
    - statusCode: HTTP status code or custom code for exceptions.
    """
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key.strip()}",
    }
    url = "https://api.openai.com/v1/models"
    
    try:
        # Send a request to validate the API key
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            return {
                "message": "Authentication Success",
                "error": None,
                "statusCode": 200
            }
        else:
            error_message = response.json().get("error", {}).get("message", "Unknown error")
            return {
                "message": "Authentication Failed",
                "error": error_message,
                "statusCode": response.status_code
            }
    except requests.ConnectionError as conn_err:
        return {
            "message": "Authentication Failed",
            "error": f"Connection error: {str(conn_err)}",
            "statusCode": 503
        }
    except Exception as err:
        return {
            "message": "Authentication Failed",
            "error": str(err),
            "statusCode": 500
        }
