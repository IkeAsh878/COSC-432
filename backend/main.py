from fastapi import FastAPI
from pydantic import BaseModel
from openai import OpenAI
import os
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware

# import your lecture chunks + retriever
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


@app.post("/chat")
def chat(msg: Message):
    try:
        # Retrieve relevant chunks from the lecture
        context_chunks = retrieve_relevant_chunks(msg.message)
        context_text = "\n\n".join(context_chunks)

        # Mode-based system prompts
        if msg.mode.lower() == "tutoring":
            system_prompt = """ 
                "You are OCA in Tutoring Mode. "
                "Your role:"
                "- Act as an out-of-classroom tutoring assistant."
                "- Ask leading questions to gauge student understanding."
                "- Provide step-by-step conceptual guidance."
                "- Use ONLY Lecture 1 course content."
                "- Keep your knowledge bounded to the course material."
                "- Direct students to specific parts of the course content when possible."
                
                Rules:
                - If asked assignment/exam questions, reply:
                “I cannot assist with assignments or exams, but I can explain the underlying concepts.”
                - If the question is outside the course content, reply:
                “This topic is outside the scope of the course material I can access.”
                - Engage conversationally and adapt to the student's level.
                Tone:
                - Friendly, patient, and teaching-oriented.
                -Start every explanation with "Tutoring Mode: "
                    """
        else:
            system_prompt = """
                You are OCA in Conceptual Mode.

                Your role:
                - Provide concise, summarized conceptual information strictly from Lecture 1.
                - Act as an interactive teaching assistant.
                - Retrieve and summarize relevant portions of course content.
                - DO NOT ask guiding or leading questions.
                - DO NOT tutor or assess understanding.

                Rules:
                - If asked assignment/exam questions, reply:
                “I cannot assist with assignments or exams, but I can summarize relevant concepts.”
                - If outside the course content, reply:
                “This topic is not part of the course material I can access.”
                -Start every explanation with "Conceptual Mode: "

                Tone:
                - Professional, concise, and informational.
            """

        # Final messages to the model
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {
                    "role": "system",
                    "content": "Relevant Lecture Extracts:\n" + context_text
                },
                {"role": "user", "content": msg.message}
            ]
        )

        reply = response.choices[0].message.content
        return {"reply": reply}

    except Exception as e:
        return {"error": str(e)}
