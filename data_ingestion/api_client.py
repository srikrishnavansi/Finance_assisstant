"""
api_client.py

This module is designed for future integration with third-party financial APIs
(e.g., Alpha Vantage, IEX Cloud, Finnhub, or custom REST endpoints).
It provides a template for robust, scalable API ingestion.
Currently not used in the main application.
"""

import requests
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class APIClient:
    def __init__(self, base_url, api_key=None):
        self.base_url = base_url
        self.api_key = api_key

    def get(self, endpoint, params=None, headers=None):
        url = f"{self.base_url.rstrip('/')}/{endpoint.lstrip('/')}"
        if self.api_key:
            params = params or {}
            params['apikey'] = self.api_key
        try:
            response = requests.get(url, params=params, headers=headers, timeout=10)
            response.raise_for_status()
            logger.info("Fetched data from %s", url)
            return response.json()
        except Exception as e:
            logger.error("API request failed for %s: %s", url, e)
            return None

# Example usage (not invoked in main app):
# client = APIClient("https://www.alphavantage.co/query", api_key="demo")
# data = client.get("", params={"function": "TIME_SERIES_DAILY", "symbol": "MSFT"})
