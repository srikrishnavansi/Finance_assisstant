import logging
import yfinance as yf

logger = logging.getLogger("scraping_agent")
logger.setLevel(logging.INFO)

def get_news(query, count=10, logs=None):
    try:
        news = yf.Search(query, news_count=count).news
        logger.info("Fetched news for '%s' (scraping_agent)", query)
        if logs is not None:
            logs.append(f"Fetched news for '{query}' (scraping_agent)")
        return news
    except Exception as e:
        logger.error("Failed to fetch news for '%s': %s", query, e)
        if logs is not None:
            logs.append(f"Failed to fetch news for '{query}': {e}")
        return []
