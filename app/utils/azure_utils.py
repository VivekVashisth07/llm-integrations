from langchain.chat_models import AzureChatOpenAI
from langchain.prompts.chat import ChatPromptTemplate
from typing import Generator

class AzureChatOpenAIService:
    def __init__(self, api_key: dict):
        """
        Initialize the AzureChatOpenAIService instance.

        Args:
            api_key (str): The API key for Azure OpenAI.
            endpoint (str): The endpoint URL for Azure OpenAI.
            deployment_name (str): The deployed model name.
        """
        self.api_key = api_key.get("api_key")
        self.endpoint = api_key.get("azure_endpoint")
        self.deployment_name = api_key.get("azure_deployment")
        self.api_version = api_key.get("api_version")
        self.chat_model = AzureChatOpenAI(
            openai_api_key=self.api_key,
            azure_endpoint=self.endpoint,
            azure_deployment=self.deployment_name,
            openai_api_version=self.api_version,  # Use the correct API version
            temperature=0
        )


    def generate_response(
        self, prompt: str, query: str, context: str, streaming: bool = False
    ) -> Generator[str, None, None] or str:
        """
        Generate a response using Azure OpenAI Chat Model.

        Args:
            prompt (str): The initial system prompt to guide the AI.
            query (str): The user's input or query.
            context (str): Additional context for the AI.
            streaming (bool): Whether to return the result in a streaming format.

        Returns:
            str or generator: The generated response. If streaming is True, returns a generator.
        """
        try:
            # Create the chat prompt template
            chat_prompt = ChatPromptTemplate.from_messages([
                ("system", prompt),
                ("user", f"Context: {context}\n\nQuery: {query}")
            ])

            # Generate messages based on the prompt template
            messages = chat_prompt.format_messages()

            if streaming:
                # Streaming: Return a generator
                response = self.chat_model.stream(messages)
                for chunk in response:
                    yield chunk.content
            else:
                # Non-streaming: Return the full response
                response = self.chat_model(messages)
                return response.content
        except Exception as e:
            return {
            "statusCode": 500,
            "message": str(e) 
        }