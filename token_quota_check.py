from groq import Groq
from google import genai
import config
import requests
def token_usage_groq():
    headers = {
        "Authorization": "Bearer " + config.llm_API_key_groq,
        "Content-Type": "application/json"
    }

    r = requests.post(
        "https://api.groq.com/openai/v1/chat/completions",
        headers=headers,
        json={
            "model": config.API_MODEL,
            "messages": [{"role": "user", "content": "Hello"}]
        }
    )

    if r.status_code != 200:
        print("Groq API Error:", r.status_code)
        print(r.text)
        return

    h = r.headers

    print(f"Now you are use this Model: {config.API_MODEL_groq}")
    print("RPM :", h.get("x-ratelimit-limit-requests", "N/A"))
    print("Remaining Requests :", h.get("x-ratelimit-remaining-requests", "N/A"))
    print("TPM :", h.get("x-ratelimit-limit-tokens", "N/A"))
    print("Remaining Tokens :", h.get("x-ratelimit-remaining-tokens", "N/A"))
    print("Requests Reset :", h.get("x-ratelimit-reset-requests", "N/A"))
    print("Tokens Reset :", h.get("x-ratelimit-reset-tokens", "N/A"))
    print("Hint:\nRPM (Requests Per Minute)\nTPM (Tokens Per Minute)\nTPD (Tokens Per Day)\nTPD (Tokens Per Day)\nMore detail visit here:https://console.groq.com/settings/limits")


def token_usage_gemini():
    print("More detail visit here:https://aistudio.google.com/rate-limit")
def token_usage_github_models():
    print("More detail visit here:https://docs.github.com/en/github-models/use-github-models/prototyping-with-ai-models#rate-limits")
