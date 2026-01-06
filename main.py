import requests
from google import genai
from dotenv import load_dotenv
from pydantic import BaseModel

load_dotenv()

client = genai.Client()
light_llm_model = "gemini-2.0-flash-lite"

reponse = client.models.generate_content(
    model=light_llm_model, contents="Hi again! Just testing for now, giving you some prompts later :)"
)

print(reponse.text)

class SessionData(BaseModel):
    session_id: str
    user_id: str
    data: dict

session_store = {}

def intent_feedback_handler(query: str, session_id) -> str:
    return "Handled feedback intent."

def intent_new_question_handler(query: str) -> str:
    return "Handled new question intent."

def classify_intent(query: str) -> str:
    sys_instruct = f"""
Classify calculus tutor intent.
Categories: feedback, new_question, bogus
Rules: lowercase, no punctuation/quotes.
Scope: derivatives (power/chain/opt), integrals (sub/parts/partial).
Examples:
"How did you do step 3?" -> feedback
"Solve: integrate x^2 dx" -> new_question
"What is integration by parts?" -> new_question
"What's the weather?" -> bogus"""
    
    response = client.models.generate_content(
        model=light_llm_model,
        contents=f"{query}",
        config={
            "system_instruction": sys_instruct,
            "max_output_tokens": 5,
            "temperature": 0.0,
            "stop_sequences": ["\n", " "]
        }
    )
    return response.text.strip()
    
test_cases = [
    "Can you explain step 4?",
    "Solve: ∫ sin(x) dx",
    "What's the capital of France?",
    "i dont get how u got u=x^2",
    "what's int(x^3)dx",
    "sin^2(x) derivative",
    "explain l'hopital's rule",
    "what is mclaurin series",
]

for case in test_cases:
    intent = classify_intent(case)
    print(f'User message: "{case}" -> Classified intent: {intent}')