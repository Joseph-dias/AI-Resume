from dotenv import load_dotenv
from xai_sdk import Client
from xai_sdk.chat import system, user

load_dotenv()

client = Client()

chat = client.chat.create(model="grok-3")
chat.append(system("You are a helpful assistant."))
chat.append(user("Hello! What can you help me with?"))

response = chat.sample()
print(response.content)
