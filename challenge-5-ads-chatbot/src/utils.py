import re
import json

def extract_json(text):
    """
    Extracts the JSON object found in the input text string.

    Parameters:
        text (str): The string containing a JSON object.

    Returns:
        dict or None: Parsed JSON object as a Python dictionary if successful,
                      None if no valid JSON is found or parsing fails.
    """
    # Regular expression to find the first JSON object in the text
    match = re.search(r'\{.*?\}', text, re.DOTALL)
    if match:
        try:
            return json.loads(match.group())
        except json.JSONDecodeError:
            print("Invalid JSON format")
            return None
    else:
        print("No JSON found")
        return None