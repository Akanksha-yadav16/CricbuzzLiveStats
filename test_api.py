# test_api.py
from utils.api_handler import get_live_matches

matches = get_live_matches()
if matches:
    print("✅ Live matches fetched successfully!")
    print(matches.keys())   # top-level keys from the API response
else:
    print("❌ Failed to fetch live matches")
