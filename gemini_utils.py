import os
from dotenv import load_dotenv
import google.generativeai as genai

# ----------------------------
# Load environment variables
# ----------------------------
load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")
MODEL_NAME = os.getenv("GEMINI_MODEL", "gemini-3.1-flash-lite")

if not API_KEY:
    raise ValueError("GEMINI_API_KEY not found in .env")

genai.configure(api_key=API_KEY)

model = genai.GenerativeModel(MODEL_NAME)


# ----------------------------
# Enhance official FAQ answer
# ----------------------------
def enhance_faq_answer(question, answer, source):
    """
    Improve wording of an official FAQ answer
    without changing any facts.
    """

    prompt = f"""
You are CollegeBuddy, the AI assistant for ITM University Gwalior.

The following answer comes from the OFFICIAL FAQ database.

Student Question:
{question}

Official Answer:
{answer}

Source:
{source}

Rules:
- Do NOT change facts.
- Do NOT invent fees, dates, contacts or policies.
- Keep the meaning exactly the same.
- Improve grammar and readability.
- Keep it concise (2–5 sentences).
- Do not mention that you are an AI.
"""

    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception:
        return answer

# ----------------------------
# best of 3 top responses
# ----------------------------
def select_best_faq(question, candidates):
    """
    Ask Gemini to choose the best official FAQ from the top TF-IDF candidates.
    """

    if not candidates:
        return None

    options = ""

    for i, c in enumerate(candidates, start=1):
        options += f"""
Candidate {i}
Question: {c['question']}
Answer: {c['answer']}
Category: {c['category']}
Source: {c['source']}
Similarity: {c['similarity']:.2f}
"""

    prompt = f"""
You are CollegeBuddy for ITM University Gwalior.

A student asked:

{question}

Below are the TOP 3 official FAQ matches found by TF-IDF.

{options}

Your job:
- Choose ONLY ONE candidate.
- Do NOT invent information.
- Prefer the candidate whose meaning best matches the student's question, even if its similarity score is slightly lower.
- Return ONLY the candidate number (1, 2, or 3).

Example:
2
"""

    try:
        response = model.generate_content(prompt)
        choice = int(response.text.strip())

        if 1 <= choice <= len(candidates):
            return candidates[choice - 1]

    except Exception:
        pass

    return candidates[0]

# ----------------------------
# Gemini fallback
# ----------------------------
def generate_fallback_answer(question):
    """
    Answer only when no suitable FAQ exists.
    """

    prompt = f"""
You are CollegeBuddy for ITM University Gwalior.

A student's question could not be matched with the official FAQ database.

Student Question:
{question}

Rules:
- Answer professionally.
- Do NOT invent ITM-specific facts.
- If official information is unknown, clearly advise the student to verify it from the ITM University website or admission office.
- Keep the response concise (2–5 sentences).
- Do not make unsupported college-specific claims.
"""

    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception:
        return (
            "Sorry, I couldn't find this information in the official FAQ database. "
            "Please verify it from the ITM University website."
        )