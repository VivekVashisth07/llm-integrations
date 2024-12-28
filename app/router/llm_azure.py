from fastapi import APIRouter
from fastapi import APIRouter, HTTPException, Query, Body 
from fastapi.responses import StreamingResponse
from utils.openai_utils import OpenAIChat

from utils.llm_auth_utils import validate_azure_api_key
router = APIRouter()

@router.get("/azure/authenticate")
async def authenticate_openai(
        azure_endpoint: str = Query(..., description="Azure OpenAI Endpoint"),
        api_key: str = Query(..., description="Azure OpenAI API Key"),
        api_version: str = Query(..., description="Azure OpenAI API Version"),
        azure_deployment: str = Query(..., description="Azure OpenAI Deployment Name")
    ):
    """
    Endpoint to authenticate OpenAI API.
    
    Parameters:
    - api_key (dict):
        - azure_endpoint: The endpoint URL of your Azure OpenAI resource.
        - api_key: The API key for your Azure OpenAI resource.
        - api_version: The API version to use.
        - azure_deployment: The name of your Azure OpenAI deployment.

    
    Returns:
    - A confirmation if azure is correct or not.
    """
    if azure_endpoint and api_key and api_version and azure_deployment:
        return validate_azure_api_key({
        "azure_endpoint": azure_endpoint,
        "api_key": api_key,
        "api_version": api_version,
        "azure_deployment": azure_deployment
    })
    else:
        return {
            "error": "API key is required to authenticate Azure OpenAI API.",
            "status": 400,
            "message": "Failed"
        }

@router.post("/azure/generate")
async def generate_response(
    prompt: str = Body( description="The system prompt to guide the AI.", default= "You have to answer the query by using or without using context"),
    query: str = Body( description="The user's query or input.", default= "Who is Magnus Carlson"),
    context: str = Body( description="Additional context for the query.", default= "Chess is the best sport in the world"),
    streaming: bool = Body(False, description="Enable or disable streaming mode."),
    api_key: dict = Body({"azure_endpoint":"","api_key":"","api_version":"","azure_deployment":""}, description="The correct Azure Key."),
):
    """
    Endpoint to generate a response using Azure via LangChain.
    """
    try:

        # validating the Azure key 
        # key_valid = validate_azure_api_key(api_key)
        # if key_valid["statusCode"]!=200:
        #     return key_valid
        
        # Initialize Azure instance and authenticate
        openai_chat = OpenAIChat(api_key=api_key)
        if streaming:
            # Streaming mode: Use a generator wrapped in StreamingResponse
            response_generator = openai_chat.generate_response(prompt, query, context, streaming=True)
            return StreamingResponse(
                response_generator, media_type="text/plain"
            )
        else:
            # Non-streaming mode: Return the full response
            result = openai_chat.generate_response(prompt, query, context, streaming=False)
            return {"response": result}
    except Exception as e:
        return {
            "statusCode": 500,
            "message": str(e) 
        }