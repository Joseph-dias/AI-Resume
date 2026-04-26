import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from dotenv import load_dotenv
from xai_sdk import Client
from resume_chat import ResumeChat

load_dotenv()

app = FastAPI()
client = Client()
resume = ResumeChat(client, collection_id=os.environ["XAI_COLLECTION_ID"])


class ChatRequest(BaseModel):
    message: str


@app.post("/api/chat")
async def chat(req: ChatRequest):
    response = resume.ask(req.message)
    return {"response": response}


app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
def index():
    return FileResponse("static/index.html")
