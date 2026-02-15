#  BrowserStack Assessment

This project demonstrates web scraping, text translation via Rapid Translate Multi Traduction API, word frequency analysis, and cross-browser testing using Selenium , Python and BrowserStack.

---

##  Problem Statement

1. Visit [El País – Opinion Section](https://elpais.com/opinion/)
2. Scrape:
   - First 5 articles
   - Print **title** and **content** in Spanish
   - Download the **cover image** if available
3. Translate Titles:
   - Use **Rapid Translate Multi Traduction API**
   - Translate all 5 article titles from **Spanish to English**
4. Analyze Translated Headers:
   - Identify words repeated **more than twice**
5. Cross-Browser Testing:
   - Run locally first
   - Then execute on **BrowserStack** using **5 parallel threads** with combinations of desktop and mobile browsers

---

## 🗂️ Project Structure

```
Browserstack_CE_assignment/
├── .env                   # Stores credentials (not pushed to GitHub)
├── .gitignore             # Ignores .env, __pycache__, etc.
├── README.md             
├── requirements.txt       # Dependencies
├── main.py                # Runs local scraping + translation
├── scrape.py              # Scraper function (with image saving)
├── translate.py           # Single-call translation logic
├── browserstack_test.py   # Parallel test run across 5 devices via BrowserStack
└── images/                
```

---

##  Setup Instructions

### 1️⃣ Clone & Navigate

```bash
git clone https://github.com/shubhamkr7519/Browserstack_CE_assignment.git
cd Browserstack_CE_assignment
```

### 2️⃣ Setup Virtual Environment

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate
```

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Create `.env` File

In the root folder, add:

```
RAPIDAPI_KEY=your_rapidapi_key
BROWSERSTACK_USERNAME=your_browserstack_username
BROWSERSTACK_ACCESS_KEY=your_browserstack_access_key
```

---

## 🚀 How to Run

### ▶️ Run Locally

```bash
python main.py
```

- Scrapes the first 5 articles
- Saves cover images (if available)
- Translates titles
- Prints repeated words from translated headers

### 🌐 Run on BrowserStack

```bash
python browserstack_test.py
```

---

## 🔐 API & Testing Info

### RapidAPI
- [Rapid Translate Multi Traduction API](https://rapidapi.com/)

### BrowserStack
- WebDriver URL used:
  ```
  https://<USERNAME>:<ACCESS_KEY>@hub-cloud.browserstack.com/wd/hub
  ```
- Capabilities defined for real devices and desktop browsers

---

## 🧾 requirements.txt

```
selenium
requests
python-dotenv
```


<<<<<<< HEAD
## 👨‍💻 Author

**Ankur Upadhyay**

```
Email: ankurupadhyay325@gmail.com 
LinkedIn: https://www.linkedin.com/in/ankur-upadhyay-30a497235/?originalSubdomain=in
```
