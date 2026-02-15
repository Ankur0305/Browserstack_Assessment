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

    remote_url = f"https://{USERNAME}:{ACCESS_KEY}@hub-cloud.browserstack.com/wd/hub"

    driver = None
    articles = []

    try:
        options = ChromeOptions()

        # Mandatory
        options.set_capability("browserName", cap["browserName"])

        # Optional (desktop)
        if "browserVersion" in cap:
            options.set_capability("browserVersion", cap["browserVersion"])

        # BrowserStack options
        options.set_capability("bstack:options", cap["bstack:options"])

        driver = RemoteWebDriver(
            command_executor=remote_url,
            options=options
        )

        articles = scrape_articles(driver)

        # -------- Mark test as PASSED on BrowserStack --------
        driver.execute_script(
            'browserstack_executor: {"action":"setSessionStatus","arguments":{"status":"passed","reason":"Scraping completed successfully"}}'
        )

    except Exception as e:

        # -------- Mark test as FAILED on BrowserStack --------
        if driver:
            try:
                driver.execute_script(
                    'browserstack_executor: {"action":"setSessionStatus","arguments":{"status":"failed","reason":"Exception during test execution"}}'
                )
            except Exception:
                pass

        print(f"[!] Error launching test for {cap.get('browserName')} — {e}")
        return

    finally:
        if driver:
            try:
                driver.quit()
            except Exception:
                pass

    print(f"\n🌍 Test on: {cap.get('browserName')}")

    translated = translate_titles([a["title"] for a in articles])

    print("\n📰 Spanish Articles:")
    for i, a in enumerate(articles, 1):
        print(f"{i}. {a['title']}\n   {a['content']}\n")

    print("🌐 Translated Titles:")
    for t in translated:
        print("-", t)

    words = re.findall(r"\b\w+\b", " ".join(translated).lower())
    repeated = {w: c for w, c in Counter(words).items() if c > 2}

    print("🔁 Repeated Words (count > 2):")
    for word, count in repeated.items():
        print(f"{word}: {count}")


# ----------------------------
# BrowserStack capabilities
# ----------------------------

capabilities = [

    # Chrome – Desktop
    {
        "browserName": "Chrome",
        "browserVersion": "latest",
        "bstack:options": {
            "os": "Windows",
            "osVersion": "10",
            "buildName": "Parallel Scraping Test",
            "sessionName": "Chrome Desktop"
        }
    },

    # Firefox – Desktop
    {
        "browserName": "Firefox",
        "browserVersion": "latest",
        "bstack:options": {
            "os": "Windows",
            "osVersion": "10",
            "buildName": "Parallel Scraping Test",
            "sessionName": "Firefox Desktop"
        }
    },

    # Safari – macOS
    {
        "browserName": "Safari",
        "browserVersion": "latest",
        "bstack:options": {
            "os": "OS X",
            "osVersion": "Ventura",
            "buildName": "Parallel Scraping Test",
            "sessionName": "Safari Desktop"
        }
    },

    # Android – real device
    {
        "browserName": "Chrome",
        "bstack:options": {
            "deviceName": "Samsung Galaxy S22",
            "realMobile": True,
            "osVersion": "12",
            "buildName": "Parallel Scraping Test",
            "sessionName": "Android S22"
        }
    },

    # iOS – real device
    {
        "browserName": "Safari",
        "bstack:options": {
            "deviceName": "iPhone 13",
            "realMobile": True,
            "osVersion": "15",
            "buildName": "Parallel Scraping Test",
            "sessionName": "iPhone 13"
        }
    }
]


if __name__ == "__main__":
    with ThreadPoolExecutor(max_workers=5) as executor:
        executor.map(run_on_browserstack, capabilities)
