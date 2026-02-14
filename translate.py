import os
import requests
from dotenv import load_dotenv

load_dotenv()
RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY")

url = "https://rapid-translate-multi-traduction.p.rapidapi.com/t"
headers = {
    "content-type": "application/json",
    "x-rapidapi-key": RAPIDAPI_KEY,
    "x-rapidapi-host": "rapid-translate-multi-traduction.p.rapidapi.com"
}

def translate_titles(titles):
    if not titles:
        return []

    payload = {
        "from": "es",
        "to": "en",
        "q": titles  # sending entire list instead of one-by-one
    }

    try:
        res = requests.post(url, json=payload, headers=headers)
        data = res.json()
        if isinstance(data, list) and len(data) == len(titles):
            return data
        else:
            print(f"[!] Unexpected API response: {data}")
            return ["[Translation Failed]"] * len(titles)
    except Exception as e:
        print(f"[!] Exception during translation: {e}")
        return ["[Translation Failed]"] * len(titles)
