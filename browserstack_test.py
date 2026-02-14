from concurrent.futures import ThreadPoolExecutor
from selenium.webdriver.remote.webdriver import WebDriver as RemoteWebDriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from scrape import scrape_articles
from translate import translate_titles
from collections import Counter
from dotenv import load_dotenv
import os
import re

load_dotenv()
USERNAME = os.getenv("BROWSERSTACK_USERNAME")
ACCESS_KEY = os.getenv("BROWSERSTACK_ACCESS_KEY")

def run_on_browserstack(cap):
    if not USERNAME or not ACCESS_KEY:
        print("[!] Missing credentials in .env")
        return

    # Construct remote URL
    remote_url = f"https://{USERNAME}:{ACCESS_KEY}@hub-cloud.browserstack.com/wd/hub"

    try:
        # Use ChromeOptions just to load capabilities
        options = ChromeOptions()
        for key, value in cap.items():
            options.set_capability(key, value)

        driver = RemoteWebDriver(command_executor=remote_url, options=options)
        articles = scrape_articles(driver)
        driver.quit()
    except Exception as e:
        print(f"[!] Error launching test for {cap.get('browserName')} — {e}")
        return

    # Output metadata
    print(f"\n🌍 Test on: {cap.get('browserName')} — {cap.get('device', cap.get('platformName', 'Desktop'))}")

    # Translate titles
    translated = translate_titles([a['title'] for a in articles])

    # Output scraped and translated info
    print("\n📰 Spanish Articles:")
    for i, a in enumerate(articles, 1):
        print(f"{i}. {a['title']}\n   {a['content']}\n")

    print("🌐 Translated Titles:")
    for t in translated:
        print("-", t)

    # Analyze repeated words
    words = re.findall(r'\b\w+\b', ' '.join(translated).lower())
    repeated = {word: count for word, count in Counter(words).items() if count > 2}

    print("🔁 Repeated Words (count > 2):")
    for word, count in repeated.items():
        print(f"{word}: {count}")

# Define test capabilities for parallel threads
capabilities = [
    {"browserName": "Chrome", "browserVersion": "latest", "platformName": "Windows 10"},
    {"browserName": "Firefox", "browserVersion": "latest", "platformName": "Windows 10"},
    {"browserName": "Safari", "browserVersion": "latest", "platformName": "MAC"},
    {"browserName": "Chrome", "device": "Samsung Galaxy S22", "realMobile": True, "platformName": "Android"},
    {"browserName": "Safari", "device": "iPhone 13", "realMobile": True, "platformName": "iOS"},
]

# Run tests in parallel
with ThreadPoolExecutor(max_workers=5) as executor:
    executor.map(run_on_browserstack, capabilities)
