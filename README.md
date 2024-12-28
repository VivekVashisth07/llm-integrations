# FastAPI AI Integration Service

## Overview

This project provides a FastAPI-based service that integrates with multiple AI APIs, including **OpenAI**, **Azure OpenAI**, and **Google Gemini**. The service exposes several endpoints for authentication, response generation, and model handling. It supports both **synchronous** and **streaming** modes for AI responses, and is designed to handle queries related to OpenAI, Azure, and Gemini models.

---

## Features

- **Authentication** for OpenAI, Azure, and Gemini APIs.
- **Response Generation** using OpenAI, Azure, or Gemini models.
- **Streaming Mode** for real-time AI responses.
- **Integration with LangChain** for OpenAI and other AI services.
- Customizable settings such as **temperature** and **model name**.
- Easy-to-use REST API with OpenAPI specifications for clear documentation.

---

## Endpoints

### Authentication Endpoints

1. **OpenAI Authentication** (`GET /openai/authenticate`)
   - **Parameters**: `api_key` (string)
   - **Description**: Verifies the provided OpenAI API key.
   - **Response**: JSON with success or failure status.

2. **Azure Authentication** (`GET /azure/authenticate`)
   - **Parameters**: `azure_endpoint`, `api_key`, `api_version`, `azure_deployment` (all strings)
   - **Description**: Verifies the provided Azure OpenAI API credentials.
   - **Response**: JSON with success or failure status.

3. **Gemini Authentication** (`GET /gemini/authenticate`)
   - **Parameters**: `api_key` (string)
   - **Description**: Verifies the provided Google Gemini API key.
   - **Response**: JSON with success or failure status.

### Generation Endpoints

1. **OpenAI Response Generation** (`POST /openai/generate`)
   - **Request Body**: JSON containing `prompt`, `query`, `context`, `streaming`, `api_key`, `temperature`, and `model_name`.
   - **Description**: Generates a response using OpenAI's models via LangChain.
   - **Response**: JSON with the generated response or an error message.

2. **Azure Response Generation** (`POST /azure/generate`)
   - **Request Body**: JSON containing `prompt`, `query`, `context`, `streaming`, `api_key`, `temperature`, and `model_name`.
   - **Description**: Generates a response using Azure OpenAI models.
   - **Response**: JSON with the generated response or an error message.

3. **Gemini Response Generation** (`POST /gemini/generate`)
   - **Request Body**: JSON containing `prompt`, `query`, `context`, `streaming`, `api_key`, `temperature`, and `model_name`.
   - **Description**: Generates a response using Google Gemini's models.
   - **Response**: JSON with the generated response or an error message.

---

## API Documentation

This project uses **OpenAPI 3.1.0** to define the endpoints, request bodies, responses, and validation. The API documentation is automatically generated and can be accessed via `/docs` (Swagger UI) or `/redoc` (ReDoc UI).

- **Swagger UI**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **ReDoc UI**: [http://localhost:8000/redoc](http://localhost:8000/redoc)

---

## Setup and Installation

### Prerequisites

- **Python 3.10+**
- **pip** (Python package manager)
- **FastAPI** (Web framework)
- **Uvicorn** (ASGI server)
- **LangChain** (Library for chaining LLMs)
- **openai**, **requests**, **gemini** (or your chosen AI SDKs)

### Installation Steps

1. **Clone the Repository:**

```bash
git clone https://github.com/your-username/fastapi-ai-integration.git
cd fastapi-ai-integration
