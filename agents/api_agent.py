import logging
import yfinance as yf
from agents.language_agent import extract_entities

logger = logging.getLogger("api_agent")
logger.setLevel(logging.INFO)

def extract_market_entities(query, gemini_api_key, logs=None):
    entities = extract_entities(query, gemini_api_key)
    logger.info("Entities extracted: %s", entities)
    if logs is not None:
        logs.append(f"Entities extracted: {entities}")
    return entities

def fetch_ticker_data(ticker, logs=None):
    try:
        t = yf.Ticker(ticker)
        info = t.info
        hist = t.history(period='1d', interval='1m')
        price = hist['Close'][-1] if not hist.empty else info.get('regularMarketPrice')
        logger.info("Fetched yfinance data for %s: price=%s", ticker, price)
        if logs is not None:
            logs.append(f"Fetched yfinance data for {ticker}: price={price}")
        return {
            "info": info,
            "latest_price": price,
            "history": hist.reset_index().to_dict("records") if not hist.empty else [],
            "news": t.news,
        }
    except Exception as e:
        logger.error("Failed to fetch yfinance data for %s: %s", ticker, e)
        if logs is not None:
            logs.append(f"Failed to fetch yfinance data for {ticker}: {e}")
        return {}

def fetch_multiple_tickers_data(tickers, logs=None):
    data = {}
    for ticker in tickers:
        data[ticker] = fetch_ticker_data(ticker, logs)
    return data

def fetch_sector_data(sector_key, logs=None):
    try:
        sector = yf.Sector(sector_key)
        overview = sector.overview
        top_etfs = sector.top_etfs
        top_mutual_funds = sector.top_mutual_funds
        industries = sector.industries
        top_companies = sector.top_companies
        logger.info("Fetched sector data for %s", sector_key)
        if logs is not None:
            logs.append(f"Fetched sector data for {sector_key}")
        return {
            "overview": overview,
            "top_etfs": top_etfs,
            "top_mutual_funds": top_mutual_funds,
            "industries": industries,
            "top_companies": top_companies,
        }
    except Exception as e:
        logger.error("Failed to fetch sector data for %s: %s", sector_key, e)
        if logs is not None:
            logs.append(f"Failed to fetch sector data for {sector_key}: {e}")
        return {}

def fetch_industry_data(industry_key, logs=None):
    try:
        industry = yf.Industry(industry_key)
        overview = industry.overview
        top_performing = industry.top_performing_companies
        top_growth = industry.top_growth_companies
        logger.info("Fetched industry data for %s", industry_key)
        if logs is not None:
            logs.append(f"Fetched industry data for {industry_key}")
        return {
            "overview": overview,
            "top_performing": top_performing,
            "top_growth": top_growth,
        }
    except Exception as e:
        logger.error("Failed to fetch industry data for %s: %s", industry_key, e)
        if logs is not None:
            logs.append(f"Failed to fetch industry data for {industry_key}: {e}")
        return {}

def fetch_market_summary(region, logs=None):
    try:
        market = yf.Market(region)
        summary = market.summary
        status = market.status
        logger.info("Fetched market summary for %s", region)
        if logs is not None:
            logs.append(f"Fetched market summary for {region}")
        return {
            "summary": summary,
            "status": status,
        }
    except Exception as e:
        logger.error("Failed to fetch market summary for %s: %s", region, e)
        if logs is not None:
            logs.append(f"Failed to fetch market summary for {region}: {e}")
        return {}

def fetch_news(query, count=10, logs=None):
    try:
        news = yf.Search(query, news_count=count).news
        logger.info("Fetched news for '%s'", query)
        if logs is not None:
            logs.append(f"Fetched news for '{query}'")
        return news
    except Exception as e:
        logger.error("Failed to fetch news for '%s': %s", query, e)
        if logs is not None:
            logs.append(f"Failed to fetch news for '{query}': {e}")
        return []
