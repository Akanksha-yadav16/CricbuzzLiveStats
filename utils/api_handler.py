 # utils/api_handler.py
import requests
import os

# You will need your RapidAPI key (get from https://rapidapi.com/cricketapilive/api/cricbuzz-cricket/)
RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY", "your_api_key_here")

BASE_URL = "https://cricbuzz-cricket.p.rapidapi.com"

HEADERS = {
    "x-rapidapi-host": "cricbuzz-cricket.p.rapidapi.com",
    "x-rapidapi-key": RAPIDAPI_KEY
}


def get_live_matches():
    """Fetch all live matches"""
    url = f"{BASE_URL}/matches/v1/live"
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print("❌ Error fetching live matches:", e)
        return None


def get_match_score(match_id: str):
    """Fetch scorecard for a given match"""
    url = f"{BASE_URL}/mcenter/v1/{match_id}/scard"
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"❌ Error fetching match {match_id} score:", e)
        return None


API_HOST = "cricbuzz-cricket.p.rapidapi.com"
API_KEY = os.getenv("RAPIDAPI_KEY")  # Make sure you set this in your environment!

HEADERS = {
    "x-rapidapi-host": API_HOST,
    "x-rapidapi-key": API_KEY,
}

def get_player_stats(player_id: str):
    """Fetch player career stats from Cricbuzz API"""
    urls = [
        f"https://cricbuzz-cricket.p.rapidapi.com/stats/v1/player/{player_id}",
        f"https://cricbuzz-cricket.p.rapidapi.com/stats/v1/player/{player_id}/profile",
    ]
    for url in urls:
        try:
            response = requests.get(url, headers=HEADERS, timeout=10)
            print("URL:", url)
            print("STATUS:", response.status_code)
            print("RAW TEXT:", response.text[:200])

            if response.status_code == 200:
                return response.json()
        except Exception as e:
            print(f"❌ Error fetching stats from {url}: {e}")
    return None

