import asyncio
import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, StreamingResponse
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


# Receive a chat message and return the AI's response
@app.post("/api/chat")
async def chat(req: ChatRequest):
    response = resume.ask(req.message)
    return {"response": response}


# Receive a chat message and return the AI's response as a stream of chunks for real-time display
@app.post("/api/chat/stream")
async def chat_stream(req: ChatRequest):
    async def generate():
        loop = asyncio.get_running_loop()
        queue: asyncio.Queue = asyncio.Queue()

        def run_stream():
            try:
                for chunk in resume.stream(req.message):
                    loop.call_soon_threadsafe(queue.put_nowait, chunk)
            finally:
                loop.call_soon_threadsafe(queue.put_nowait, None)

        loop.run_in_executor(None, run_stream)
        while True:
            chunk = await queue.get()
            if chunk is None:
                break
            escaped = chunk.replace('\n', '\\n')
            yield f"data: {escaped}\n\n"
        yield "data: [DONE]\n\n"
    return StreamingResponse(generate(), media_type="text/event-stream")


@app.post("/api/reset")
async def reset():
    resume.reset()
    return {}


@app.get("/VERSION")
def get_version():
    return FileResponse("VERSION", media_type="text/plain")


app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
def index():
    return FileResponse("static/index.html")
