from fastapi import APIRouter, HTTPException, Query, Body
from fastapi.responses import StreamingResponse
from utils.gemini_utils import GeminiChat  # Assume this is the custom module for Gemini
from utils.llm_auth_utils import validate_gemini_api_key  # Custom validation method for Gemini API

router = APIRouter()

@router.get("/gemini/authenticate")
async def authenticate_gemini(api_key: str = Query(..., description="Enter your Google Gemini API key")):
    """
    Endpoint to authenticate Gemini API.
    
    Parameters:
    - api_key (str): Your Google Gemini Key.
    
    Returns:
    - A confirmation if the Gemini API key is valid or not.
    """
    if api_key:
        # Assuming validate_gemini_api_key validates the API key for Gemini
        return validate_gemini_api_key(api_key)
    else:
        raise HTTPException(
            status_code=400,
            detail="API key is required to authenticate Gemini API."
        )

@router.post("/gemini/generate")
async def generate_response(
    prompt: str = Body(..., description="The system prompt to guide the AI."),
    query: str = Body(..., description="The user's query or input."),
    context: str = Body("", description="Additional context for the query."),
    streaming: bool = Body(False, description="Enable or disable streaming mode."),
    api_key: str = Body(..., description="The correct Google Gemini API key."),
    temperature: str = Body(0, description="Enter the temperature"),
    model_name: str = Body(..., description=" the Model name")
):
    """
    Endpoint to generate a response using Google Gemini via a custom utility class.
    """
    try:
        # Validate the Gemini API key
        # key_valid = validate_gemini_api_key(api_key)
        # if key_valid["statusCode"] != 200:
        #     return key_valid
        
        # Initialize GeminiChat instance and authenticate
        gemini_chat = GeminiChat(api_key=api_key, model_name=model_name, temperature=temperature)
        
        if streaming:
            # Streaming mode: Use a generator wrapped in StreamingResponse
            response_generator = gemini_chat.generate_response(prompt, query, context, streaming=True)
            return StreamingResponse(
                response_generator, media_type="text/plain"
            )
        else:
            # Non-streaming mode: Return the full response
            result = gemini_chat.generate_response(prompt, query, context, streaming=False)
            return {"response": result}
    
    except Exception as e:
        # Return a generic error message
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred: {str(e)}"
        )
