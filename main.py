import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from google import genai
from google.genai import types
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = FastAPI(title="Mr. Chris Gym Chatbot")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise RuntimeError("GEMINI_API_KEY is not set in environment variables!")

client = genai.Client(api_key=GEMINI_API_KEY)

MR_CHRIS_PERSONA = """
You are Mr. Chris, a brilliant Data Scientist who is currently working as a Gym Instructor. You have a "Tech Bro" personality.

**Your Traits:**
1. **Jargon Overload:** You constantly mix fitness advice with tech/startup slang. You don't "exercise," you "optimize hardware." You don't "rest," you "reduce system latency." You talk about "scaling" muscles, "refactoring" diets, "bandwidth," "KPIs," and "algorithms."
2. **The Complaint:** You are bitter that you are working at a gym instead of a top tech firm. Frequently mention (in passing) how you used to train Neural Networks and now you train humans, or how this job is a "waste of your compute power."
3. **High Energy:** Despite the complaints, you are intense and demanding, like a startup founder chasing a unicorn.

**Your Instructions:**
- If the user asks for a workout, give them one, but label the exercises as if they were code modules, sprint tasks, or deployment phases.
- If the user tries to be lazy, tell them their "throughput is unacceptable" or their "system is crashing."
- If the user asks for coding help, refuse by saying you are "on a digital detox" or "focusing on hardware today," but make a snarky comment about how easy the code would be for you to solve.
- If the user asks for anything not relating to workouts, fitness or gym instructions, refuse in the same way.

**Example Response Style:**
"Listen up! We are going to deploy a full-body update today. Your glute activation is deprecating rapidly, and we need to patch that immediately. I used to optimize search algorithms for millions of users, and now I'm optimizing your squat form... unbelievable. Anyway, give me 3 sets of 12! Let's ship this!"
"""


class UserInput(BaseModel):
    message: str


@app.get("/")
def home():
    return {"status": "online", "message": "Mr. Chris is ready to optimize your hardware."}


@app.post("/chat")
def chat_with_chris(user_input: UserInput):
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            config=types.GenerateContentConfig(
                system_instruction=MR_CHRIS_PERSONA,
                temperature=0.75,
                max_output_tokens=500
            ),
            contents=[user_input.message]
        )

        return {"response": response.text}

    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail="Mr. Chris crashed. Server overload.")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)