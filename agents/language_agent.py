import re
import json
import logging
import google.generativeai as genai

logger = logging.getLogger("language_agent")
logger.setLevel(logging.INFO)

def extract_entities(query, gemini_api_key):
    if not gemini_api_key:
        logger.error("GEMINI_API_KEY not provided.")
        raise RuntimeError("GEMINI_API_KEY not provided.")
    genai.configure(api_key=gemini_api_key)
    from google.generativeai import GenerativeModel
    gemini = GenerativeModel("gemini-1.5-flash")
    prompt = f"""
Extract the following entities from the user query for financial analysis:
- ticker (list or str)
- index_name
- sector
- industry
- region (list or str)
- asset_type
- market
- from_currency
- to_currency

Return a JSON object with these fields (use null if not found).
Query: "{query}"
"""
    resp = gemini.generate_content(prompt)
    try:
        match = re.search(r"\{.*\}", resp.text, re.DOTALL)
        result = json.loads(match.group(0)) if match else {}
        logger.info("Extracted entities: %s", result)
    except Exception as e:
        logger.error("Failed to extract entities: %s", e)
        result = {}
    return result
