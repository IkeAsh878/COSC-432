from fastapi import FastAPI
from pydantic import BaseModel
from openai import OpenAI
import os
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware

# Load API key from .env
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

app = FastAPI()

# Enable CORS so your frontend (localhost) can talk to backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For development only; restrict in production
    allow_methods=["*"],
    allow_headers=["*"]
)

# Pydantic model for incoming messages
class Message(BaseModel):
    message: str
    mode: str = "Tutoring"  # default mode

@app.post("/chat")
def chat(msg: Message):
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "user", "content": msg.message}
            ]
        )

        reply = response.choices[0].message.content
        return {"reply": reply}

    except Exception as e:
        return {"error": str(e)}
