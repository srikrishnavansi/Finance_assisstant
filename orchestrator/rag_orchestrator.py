import logging
from agents import api_agent, scraping_agent, llm_orchestrator, voice_agent

logger = logging.getLogger("rag_orchestrator")
logger.setLevel(logging.INFO)

def orchestrate(query, gemini_api_key, elevenlabs_api_key, voice_id="tnSpp4vdxKPjI9w0GnoV", logs=None):
    if logs is None:
        logs = []
    logs.append(f"Received query: {query}")
    logger.info("Received query: %s", query)

    entities = api_agent.extract_market_entities(query, gemini_api_key, logs)
    logs.append(f"Entities extracted: {entities}")
    logger.info("Entities extracted: %s", entities)

    fetched_data = {}

    ticker = entities.get("ticker")
    if ticker:
        if isinstance(ticker, list):
            fetched_data["ticker_data"] = api_agent.fetch_multiple_tickers_data(ticker, logs)
        else:
            fetched_data["ticker_data"] = api_agent.fetch_ticker_data(ticker, logs)

    sector = entities.get("sector")
    if sector:
        fetched_data["sector_data"] = api_agent.fetch_sector_data(sector, logs)

    industry = entities.get("industry")
    if industry:
        fetched_data["industry_data"] = api_agent.fetch_industry_data(industry, logs)

    region = entities.get("region")
    if region:
        if isinstance(region, list):
            for reg in region:
                fetched_data[f"market_{reg}"] = api_agent.fetch_market_summary(reg, logs)
        else:
            fetched_data["market_summary"] = api_agent.fetch_market_summary(region, logs)

    news_queries = [query]
    if ticker:
        if isinstance(ticker, list):
            news_queries.extend(ticker)
        else:
            news_queries.append(ticker)
    if sector:
        news_queries.append(sector)
    if industry:
        news_queries.append(industry)
    if region:
        if isinstance(region, list):
            news_queries.extend(region)
        else:
            news_queries.append(region)
    news = []
    for nq in set(news_queries):
        news.extend(scraping_agent.get_news(nq, count=10, logs=logs))
    fetched_data["news"] = news

    llm_result = llm_orchestrator.llm_orchestrate(query, entities, fetched_data, gemini_api_key)
    logs.extend(llm_result.get("logs", []))

    response_text = llm_result.get("response", "Here are the latest insights based on available data and news.")
    audio_bytes = voice_agent.text_to_speech(response_text, elevenlabs_api_key, voice_id)
    if audio_bytes:
        logs.append("Audio generated successfully.")
        logger.info("Audio generated successfully.")
    else:
        logs.append("Audio generation failed.")
        logger.error("Audio generation failed.")

    return {
        "text": response_text,
        "audio_bytes": audio_bytes,
        "logs": logs,
        "plan": llm_result.get("plan", []),
        "data": fetched_data
    }
