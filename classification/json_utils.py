import json
import re

def extract_clean_json(text):
    """
    Extract the first valid JSON object from a text string.
    This removes any extra text around the JSON response.
    """
    try:
        json_pattern = re.compile(r'{.*?}', re.DOTALL)
        match = json_pattern.search(text)
        if match:
            json_str = match.group(0)
            return json.loads(json_str)
    except json.JSONDecodeError:
        pass

    return {
        "should_draft": False,
        "is_junk": False,
        "is_important": False,
        "has_deadline": False,
        "deadline": None,
        "suggested_reply": "No valid JSON found."
    }
