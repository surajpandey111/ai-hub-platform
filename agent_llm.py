from google import genai
from google.genai import types
import os
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

VALID = ["PDF", "COOKING", "CHATBOT"]

def _clean_intent(text: str) -> str:
    if not text:
        return "UNKNOWN"
    t = text.strip().upper()
    # normalize common variants
    t = t.replace(".", "").replace("\n", " ").strip()
    # map loosely to strict labels
    if "PDF" in t or "DOCUMENT" in t or "EXCEL" in t or "FILE" in t:
        return "PDF"
    if "COOK" in t or "RECIPE" in t or "FOOD" in t:
        return "COOKING"
    if "CHAT" in t or "COLLEGE" in t or "REC" in t or "ADMISSION" in t:
        return "CHATBOT"
    return "UNKNOWN"


def _fallback_intent(query: str) -> str:
    q = query.lower()
    if any(w in q for w in ["pdf", "excel", "document", "file", "analyze"]):
        return "PDF"
    if any(w in q for w in ["cook", "recipe", "food", "ingredient"]):
        return "COOKING"
    if any(w in q for w in ["rec", "college", "azamgarh", "admission"]):
        return "CHATBOT"
    return "UNKNOWN"


def detect_intent_llm(query: str) -> str:
    prompt = f"""
Classify the user query into EXACTLY ONE label:

LABELS:
- PDF
- COOKING
- CHATBOT

GUIDELINES:
- PDF → document/file/excel/analysis
- COOKING → food/recipe/ingredients
- CHATBOT → college/REC/admission/info

Query: {query}

STRICT OUTPUT:
Return ONLY ONE TOKEN: PDF or COOKING or CHATBOT
(No punctuation, no explanation)
"""

    try:
        response = client.models.generate_content(
            model="gemini-3-flash-preview",
            contents=prompt,
            config=types.GenerateContentConfig(
                thinking_config=types.ThinkingConfig(thinking_level="low")
            )
        )

        raw = getattr(response, "text", "") or ""
        intent = _clean_intent(raw)

        if intent in VALID:
            return intent

        # fallback if LLM output is messy
        fb = _fallback_intent(query)
        return fb if fb != "UNKNOWN" else "UNKNOWN"

    except Exception as e:
        print("LLM routing error:", e)
        # hard fallback to keep app alive
        return _fallback_intent(query)


# optional quick test
if __name__ == "__main__":
    print(detect_intent_llm("How to make paneer butter masala?"))