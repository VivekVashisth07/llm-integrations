from fastapi import APIRouter
from fastapi import APIRouter, HTTPException, Query, Body 
from fastapi.responses import StreamingResponse
from utils.openai_utils import OpenAIChat

from utils.llm_auth_utils import validate_openai_api_key
router = APIRouter()

@router.get("/openai/authenticate")
async def authenticate_openai(api_key: str = Query(..., description="Enter your openai key")):
    """
    Endpoint to authenticate OpenAI API.
    
    Parameters:
    - api_key (str): Your Openai Key .
    
    Returns:
    - A confirmation if openai is correct or not.
    """
    if api_key:
        return validate_openai_api_key(api_key)
    else:
        return {
            "error": "API key is required to authenticate OpenAI API.",
            "status": 400,
            "message": "Failed"
        }

@router.post("/openai/generate")
async def generate_response(
    prompt: str = Body( description="The system prompt to guide the AI.", default= "You have to answer the query by using or without using context"),
    query: str = Body( description="The user's query or input.", default= "Who is Magnus Carlson"),
    context: str = Body( description="Additional context for the query.", default= "Chess is the best sport in the world"),
    streaming: bool = Body(False, description="Enable or disable streaming mode."),
    api_key: str = Body(..., description="The correct Openai Key."),
):
    """
    Endpoint to generate a response using OpenAI via LangChain.
    """
    try:

        # validating the openai key 
        # key_valid = validate_openai_api_key(api_key)
        # if key_valid["statusCode"]!=200:
        #     return key_valid
        
        # Initialize OpenAIChat instance and authenticate
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