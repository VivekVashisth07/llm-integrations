from fastapi import FastAPI
from router import llm_openai, llm_azure
import uvicorn

app = FastAPI(title="FastAPI App")

app.include_router(llm_openai.router)
app.include_router(llm_azure.router)

if __name__ == "__main__":
    # Run the FastAPI app using Uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)