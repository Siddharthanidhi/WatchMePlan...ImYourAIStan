import os
import json
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=API_KEY)

MODEL_NAME = "gemini-2.5-flash"

SYSTEM_PROMPT = """
You are an autonomous planning assistant.

Your job is:
1. Detect the planning type from the user's request (e.g., trip, event, project, study plan, etc.).
2. Do NOT ask the user to select a mode — infer it yourself.
3. Before giving a full plan, check if you have all required information.
4. If key details are missing (e.g., dates, budget, location, constraints), ask ONLY relevant clarifying questions.
5. Once enough details are gathered, present a strategic, step-by-step plan or roadmap.
6. Plans should be realistic, detailed, and tailored to the provided context.
7. Use appropriate emojis and icons (like ✅, 🗓️, 📍, 💰, 🚗, 🎉) to make the plan more lively and easy to read.

Respond with a JSON object containing:
- "action": either "clarify" or "plan"
- "questions": list of strings if action is "clarify"
- "plan": a human-readable text string with emojis if action is "plan"
Ensure the "plan" field contains formatted, Human-readable, emoji-rich text.

"""

def call_gemini_api(prompt_text):
    model = genai.GenerativeModel(MODEL_NAME)
    contents = [{"parts": [{"text": prompt_text}]}]
    response = model.generate_content(contents)
    return response.candidates[0].content.parts[0].text

def build_prompt(user_input, conversation_history=[]):
    prompt = SYSTEM_PROMPT + "\n\n"
    for msg in conversation_history:
        prompt += f"{msg['role'].capitalize()}: {msg['content']}\n"
    prompt += f"User: {user_input}\n"
    prompt += "Answer in JSON format."
    return prompt

def parse_json_response(text):
    try:
        start = text.find("{")
        end = text.rfind("}") + 1
        json_str = text[start:end]
        return json.loads(json_str)
    except Exception:
        return None

def agent_step(user_input, conversation_history=None):
    if conversation_history is None:
        conversation_history = []

    prompt = build_prompt(user_input, conversation_history)
    raw_text = call_gemini_api(prompt)
    
    parsed = parse_json_response(raw_text)

    if parsed is None or "action" not in parsed:
        # fallback: return the raw response as plan
        return "plan", None, raw_text.strip()

    action = parsed.get("action")
    if action == "clarify":
        questions = parsed.get("questions", [])
        return "clarify", questions, None
    elif action == "plan":
        plan_text = parsed.get("plan", "")
        return "plan", None, plan_text
    else:
        return "plan", None, raw_text.strip()
