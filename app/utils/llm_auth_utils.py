import requests
import json
from openai import AzureOpenAI
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


def validate_azure_api_key(api_key: dict) -> dict:
    try:
        # Make a simple request to validate the authentication
        client = AzureOpenAI(
                    azure_endpoint = api_key.get("azure_endpoint"),
                    api_key = api_key.get("api_key"),
                    api_version = api_key.get("api_version"),
                    azure_deployment=api_key.get("azure_deployment")
                )
        resp = client.chat.completions.create(model= api_key.get("azure_deployment"),
            messages=[{"role":"user","content":"Crack a joke"}]
        )
        resp = json.loads(resp.json())
        if resp:
            {
                "message": "Authentication Success",
                "error": None,
                "statusCode": 200
            }
        else:
            {
                "message": "Authentication Failed",
                "error": resp.json(),
                "statusCode": 401
            }
    except Exception as err:
        return {
            "message": "Authentication Failed",
            "error": str(err),
            "statusCode": 500
        }