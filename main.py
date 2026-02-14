import re
from collections import Counter
from scrape import scrape_articles
from translate import translate_titles

articles = scrape_articles()
translated_titles = translate_titles([a["title"] for a in articles])

# Output
print("\n📰 Original Title and Content:\n")
for i, a in enumerate(articles, 1):
    print(f"{i}.\nTitle: {a['title']}\nContent: {a['content']}\n{'-'*100}")

print("\n🌐 Translated Titles:")
for t in translated_titles:
    print("-", t)

words = re.findall(r'\b\w+\b', ' '.join(translated_titles).lower())
word_counts = Counter(words)
repeated = {word: count for word, count in word_counts.items() if count > 2}

print("\n🔁 Repeated Words (count > 2):")
for word, count in repeated.items():
    print(f"{word}: {count}")
