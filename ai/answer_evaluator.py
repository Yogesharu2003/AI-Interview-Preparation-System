import os
import json
import time
from dotenv import load_dotenv
from google import genai
from google.genai.errors import ServerError

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


def evaluate_answer(question, answer):

    prompt = f"""
You are an expert technical interviewer.

Evaluate the candidate's answer.

Question:
{question}

Candidate Answer:
{answer}

Return ONLY valid JSON.

{{
  "score": 8,
  "feedback": "Short feedback",
  "correct_answer": "Ideal answer"
}}
"""

    # Retry up to 3 times if Gemini is busy
    for attempt in range(3):
        try:
            response = client.models.generate_content(
                model="gemini-3.5-flash-lite",   # or "gemini-3.6-flash"
                contents=prompt,
            )

            text = response.text.strip()

            if text.startswith("```"):
                text = text.replace("```json", "").replace("```", "").strip()

            return json.loads(text)

        except ServerError:
            print(f"Gemini busy. Retrying ({attempt + 1}/3)...")
            time.sleep(3)

        except Exception as e:
            print("AI Error:", e)
            break

    # Fallback if AI is unavailable
    return {
        "score": 0,
        "feedback": "AI server is temporarily unavailable. Please try again later.",
        "correct_answer": "Unavailable"
    }