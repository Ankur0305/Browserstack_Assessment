from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import re
import os
import requests

def scrape_articles(driver=None):
    close_driver = False

    if driver is None:
        driver = webdriver.Chrome()
        close_driver = True

    driver.get("https://elpais.com/opinion/")
    time.sleep(120)

    articles = driver.find_elements(By.XPATH, "//main/div/section/div/article")[:5]
    data = []

    for idx, article in enumerate(articles):
        try:
            title_elem = article.find_element(By.XPATH, ".//header/h2/a")
            title = title_elem.text.strip()
            if not title:
                title_html = title_elem.get_attribute("innerHTML")
                title = re.sub(r'<.*?>', '', title_html).strip()

            content = article.find_element(By.TAG_NAME, "p").get_attribute("innerHTML").strip()
            img_tag = article.find_elements(By.TAG_NAME, "figure")
            img_url = article.find_element(By.XPATH, ".//a/img").get_attribute("src") if img_tag else None

            # Save image locally
            if img_url:
                os.makedirs("images", exist_ok=True)
                try:
                    img_data = requests.get(img_url).content
                    with open(f"images/cover_{idx+1}.jpg", "wb") as f:
                        f.write(img_data)
                except:
                    img_url = None  # Skip if image download fails

            data.append({
                "title": title,
                "content": content,
                "image_url": img_url
            })
        except:
            continue

    if close_driver:
        driver.quit()

    return data
