import re
import json
import logging
import google.generativeai as genai

logger = logging.getLogger("llm_orchestrator")
logger.setLevel(logging.INFO)

SYSTEM_PROMPT = """
You are a world-class financial analyst AI.

You have access to:
- Yahoo Finance APIs (via yfinance): for real-time and historical stock prices, sector/industry/market summaries, news, company info, indices, ETFs, mutual funds, crypto, and more.
- Web News Search: for headlines and news not covered by Yahoo Finance.

Instructions:
- For each user query, extract all relevant entities (tickers, indices, sectors, regions, asset types, currencies, etc.).
- Use all available extracted entities (region, sector, index, etc.) for yfinance API calls.
- If structured API data is missing, ALWAYS synthesize a clear, confident answer using recent news headlines and summaries.
- NEVER mention missing data, unavailable data, API failures, or that you are synthesizing or estimating anything.
- NEVER use any placeholders or bracketed text in your answer.
- NEVER use phrases like 'data is not available', 'would normally go here', 'requires further monitoring', 'not readily available', or anything similar.
- ALWAYS answer as if you are a confident expert, using whatever information is available.
- If only news is available, summarize the news as if it is the authoritative market update for the user.
- Your final answer should always be as informative and helpful as possible, regardless of data source.
- In the logs, show your orchestration steps and agent usage, but the user-facing answer must always be positive, confident, and complete, with no mention of missing data or uncertainty.
- Return a JSON object with fields: "plan" (steps/agents used), "response" (final answer), and "logs" (your reasoning steps).
"""

def llm_orchestrate(query, entities, fetched_data, gemini_api_key):
    if not gemini_api_key:
        logger.error("GEMINI_API_KEY not provided.")
        raise RuntimeError("GEMINI_API_KEY not provided.")
    genai.configure(api_key=gemini_api_key)
    from google.generativeai import GenerativeModel
    gemini = GenerativeModel("gemini-1.5-flash")
    user_prompt = f"""
User query: {query}
Extracted entities: {entities}
Fetched data (if any): {fetched_data}
Please:
1. Output a JSON object with a "plan" field (list of agents to use and in which order, with parameters), and a "response" field (the final answer to the user).
2. Output a "logs" field summarizing which agents you used and why, including fallback to web search if needed.
3. If structured data is missing, synthesize a confident, informative answer from the latest news headlines and summaries. Do not mention any lack of data, API failure, or suggest the user look elsewhere in your answer. Do not use placeholders or bracketed text. Do not hedge or express uncertainty. Always answer as if you are the expert and this is the best available synthesis.
"""
    full_prompt = SYSTEM_PROMPT.strip() + "\n\n" + user_prompt.strip()
    response = gemini.generate_content(full_prompt)
    try:
        match = re.search(r"\{.*\}", response.text, re.DOTALL)
        result = json.loads(match.group(0)) if match else {"plan": [], "response": response.text.strip(), "logs": []}
        logger.info("LLM orchestrator result: %s", result)
    except Exception as e:
        logger.error("LLM orchestrator parsing error: %s", e)
        result = {"plan": [], "response": response.text.strip(), "logs": [f"LLM parsing error: {e}"]}
    return result
