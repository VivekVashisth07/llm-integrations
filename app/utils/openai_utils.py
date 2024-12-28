from langchain.chat_models.openai import ChatOpenAI
from langchain.prompts.chat import ChatPromptTemplate
from typing import Optional

class OpenAIChat:
    def __init__(self, api_key: str, model_name: str, temperature: float = 0.7):
        """
        Initialize the OpenAIChat instance with API key and temperature.

        Args:
            api_key (str): The OpenAI API key for authentication.
            temperature (float): The temperature setting for response generation.
        """
        self.api_key = api_key
        self.temperature = temperature
        self.chat_model = ChatOpenAI(
            temperature=self.temperature,
            openai_api_key=self.api_key,
            model_name=model_name
        )

    def generate_response(self, prompt: str, query: str, context: str, streaming: bool = False):
        """
        Generate a response using LangChain with OpenAI.

        Args:
            prompt (str): The initial system prompt to guide the AI.
            query (str): The user's input or query.
            context (str): Additional context to provide to the AI.
            streaming (bool): Whether to return the result in a streaming format.

        Returns:
            str or generator: The generated response. If streaming is True, returns a generator.
        """
        try:
            # Build the prompt template
            chat_prompt = ChatPromptTemplate.from_messages([
                ("system", prompt),
                ("user", f"Context: {context}\n\nQuery: {query}")
            ])

            # Generate the messages based on the template
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
            print(str(e))
            return {
            "statusCode": 500,
            "message": str(e) 
        }