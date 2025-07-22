import os
import json
from dotenv import load_dotenv
import requests

load_dotenv()

API_KEY = os.getenv("OPENROUTER_API_KEY")
MODEL = os.getenv("MODEL_NAME")

def query_legal_llm(country: str, issue: str) -> dict:
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    prompt = f"""
You are a legal AI trained to help with small-town or rural disputes.

Based on the following input:
Country: {country}
Issue: {issue}

Return the output in strict JSON format like this:
{{
  "article": "Relevant article here",
  "cases": [{{"name": "...", "year": 2000}}, {{...}}, {{...}}],
  "escalation_paths": ["...", "..."],
  "people_involved": {{
    "complainant": "...",
    "defendant": "...",
    "authority": "..."
  }},
  "suggested_actions": ["...", "..."]
}}

Do NOT add any commentary. Just return valid JSON.
"""

    payload = {
        "model": MODEL,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.4
    }

    response = requests.post(url, headers=headers, json=payload)
    
    if response.status_code != 200:
        raise Exception(f"OpenRouter API error: {response.text}")
    
    content = response.json()["choices"][0]["message"]["content"]

    try:
        return json.loads(content)
    except Exception as e:
        raise ValueError(f"Could not parse model response as JSON: {e}\n\nRaw Output:\n{content}")
