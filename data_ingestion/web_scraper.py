import requests
from bs4 import BeautifulSoup

def get_latest_news(ticker):
    url = f"https://finance.yahoo.com/quote/{ticker}?p={ticker}"
    resp = requests.get(url)
    soup = BeautifulSoup(resp.text, "html.parser")
    news = []
    for item in soup.select('li.js-stream-content'):
        headline = item.select_one('h3').text if item.select_one('h3') else None
        link = item.select_one('a')['href'] if item.select_one('a') else None
        if headline and link:
            news.append({"headline": headline, "link": f"https://finance.yahoo.com{link}"})
        if len(news) >= 5:
            break
    return news
