import os
import cohere
from dotenv import load_dotenv
from classification.json_utils import extract_clean_json

load_dotenv()
COHERE_API_KEY = os.getenv("COHERE_API_KEY")

co = cohere.Client(COHERE_API_KEY)

def classify_email(subject: str, body: str) -> dict | None:
    """
    Use Cohere to classify the intent and urgency of an email.

    Args:
        subject (str): The subject of the email.
        body (str): The body of the email.

    Returns:
        dict | None: A dictionary with classification details or None on failure.
    """
    prompt = f"""
You are an intelligent email assistant. Given the subject and body of an email, respond with a JSON object containing:
- is_junk: true/false
- is_important: true/false
- has_deadline: true/false
- deadline: "YYYY-MM-DD" or null
- should_draft: true/false
- suggested_reply: A polite reply if needed

Email:
Subject: {subject}
Body: {body}

Respond in pure JSON format.
"""

    try:
        response = co.generate(
            model='command-r-plus',
            prompt=prompt,
            max_tokens=300,
            temperature=0.4
        )

        raw_text = response.generations[0].text
        parsed = extract_clean_json(raw_text)
        return parsed

    except Exception as e:
        print("❌ Error during Cohere classification:", e)
        return None
