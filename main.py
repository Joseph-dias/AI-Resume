import os
from dotenv import load_dotenv
from xai_sdk import Client
from resume_chat import ResumeChat

load_dotenv()

client = Client()
resume = ResumeChat(client, collection_id=os.environ["XAI_COLLECTION_ID"])
resume.run()
