def calculate_exposure(market_data, sector=None, region=None):
    # If market_data is present, use it for dynamic reporting.
    if market_data:
        # Try to extract exposure information from data if available (customize as needed)
        return {
            "region": region,
            "sector": sector,
            "exposure_percent": None,  # Only fill if you have real data
            "change_percent": None
        }
    return {
        "region": region,
        "sector": sector,
        "exposure_percent": None,
        "change_percent": None
    }

def analyze_earnings(earnings_data):
    if not earnings_data:
        return "No earnings data available."
    surprise = float(earnings_data[0].get("surprise", 0)) if isinstance(earnings_data, list) and earnings_data else 0
    res = "beat" if surprise > 0 else "missed"
    return f"{earnings_data[0]['fiscalDateEnding']}: {res} estimates by {abs(surprise)}%" if earnings_data else "No earnings data available."
