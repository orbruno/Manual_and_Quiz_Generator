import os
import re
import json
import yaml
from typing import List, Dict
from openai import OpenAI, OpenAIError

# load prompts.yml once at import time
BASE_DIR = os.path.dirname(os.path.dirname(__file__))  # backend/app → backend
with open(os.path.join(BASE_DIR, "prompts.yml"), "r", encoding="utf-8") as f:
    _PROMPTS = yaml.safe_load(f)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY", ""))

# we’ll re-use MAX_CHARS from your manual function
MAX_CHARS = 15_000

def summarize_and_structure(texts: List[str], prompt: str) -> str:
    combined = "\n\n".join(texts)[:MAX_CHARS]
    try:
        resp = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": _PROMPTS["manual"]["system"]},
                {"role": "user", "content": prompt + "\n\n" + combined},
            ],
            temperature=0.2,
        )
    except OpenAIError as e:
        raise Exception(f"OpenAI API error: {e}")
    return resp.choices[0].message.content

def generate_quiz_from_manual(manual: str) -> List[Dict]:
    # 1) build prompt
    snippet = manual[:MAX_CHARS]
    quiz_prompt = (
        _PROMPTS["quiz"]["user"]
         + "\n\n"
        + snippet
    )

    # 2) call OpenAI
    try:
        resp = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": _PROMPTS["quiz"]["system"]},
                {"role": "user",   "content": quiz_prompt},
            ],
            temperature=0.2,
        )
    except OpenAIError as e:
        raise Exception(f"OpenAI API error during quiz generation: {e}")

    raw = (resp.choices[0].message.content or "").strip()
    print("🔍 [generate_quiz_from_manual] raw AI reply:", repr(raw))

    if not raw:
        raise Exception("Quiz generation failed: empty response from OpenAI")

    # 3) strip any wrapping single or double quotes
    if (raw.startswith("'") and raw.endswith("'")) or (
        raw.startswith('"') and raw.endswith('"')
    ):
        raw = raw[1:-1].strip()
        print("stripped outer quotes, now:", repr(raw))

    # 4) strip triple-backtick fences, with optional language tag
    m = re.match(r"^```[^\n]*\n([\s\S]*)\n```$", raw)
    content = m.group(1) if m else raw

    # 5) finally parse JSON
    try:
        return json.loads(content)
    except json.JSONDecodeError:
        raise Exception(f"Invalid JSON from OpenAI after stripping:\n{content!r}")