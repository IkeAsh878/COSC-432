from fastapi import FastAPI
from pydantic import BaseModel
from openai import OpenAI
import os
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware

from lecture_data import retrieve_relevant_chunks

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

class Message(BaseModel):
    message: str
    mode: str = "Tutoring"


ASSISTANT_ID = "asst_rD5xeEalkthJwUFL2iScqDNx"

# ---------------------------------------------------------
# ✅ Create ONE persistent thread at app startup
# ---------------------------------------------------------
THREAD_ID = client.beta.threads.create().id
print("Using persistent thread:", THREAD_ID)


@app.post("/chat")
def chat(msg: Message):
    try:
        # Retrieve relevant lecture content
        context_chunks = retrieve_relevant_chunks(msg.message)
        context_text = "\n\n".join(context_chunks)

        # Build system prompt based on mode
        if msg.mode.lower() == "tutoring":
            system_prompt = f"""
You are OCA in Tutoring Mode.

Rules:
- Act as an out-of-classroom tutoring assistant.
- Ask leading questions.
- Use ONLY Lecture 1 course material.
- For assignments/exams → “I cannot assist with assignments or exams…”
- For out-of-scope → “This topic is outside the scope…”
Start every explanation with "Tutoring Mode: "

Relevant Lecture Extracts:
{context_text}
            """
        else:
            system_prompt = f"""
You are OCA in Conceptual Mode.

Rules:
- Summaries only.
- No leading questions.
- Use ONLY Lecture 1 content.
Start every explanation with "Conceptual Mode: "

Relevant Lecture Extracts:
{context_text}
            """

        # ---------------------------------------------------------
        # ✅ Append user message to THE SAME THREAD
        # ---------------------------------------------------------
        client.beta.threads.messages.create(
            thread_id=THREAD_ID,
            role="user",
            content=system_prompt + "\n\nUser: " + msg.message
        )

        # ---------------------------------------------------------
        # ✅ Run the assistant against the SAME thread
        # ---------------------------------------------------------
        run = client.beta.threads.runs.create(
            thread_id=THREAD_ID,
            assistant_id=ASSISTANT_ID
        )

        # Wait for completion
        while True:
            run_status = client.beta.threads.runs.retrieve(
                thread_id=THREAD_ID,
                run_id=run.id
            )
            if run_status.status == "completed":
                break

        # Retrieve messages
        messages = client.beta.threads.messages.list(thread_id=THREAD_ID)

        # Return latest assistant message
        for m in messages.data:
            if m.role == "assistant":
                return {"reply": m.content[0].text.value}

        return {"reply": "No assistant message found."}

    except Exception as e:
        return {"error": str(e)}
