from agent.protocol.local.search import search_with_serpapi
from dotenv import load_dotenv
import os
from agent.protocol.local.generator import generate_tweet
load_dotenv() 

tweet = generate_tweet("Mahler's Symphony No.5 Adagietto")
print(f"\n📝 Tweet:\n{tweet}")

load_dotenv()  # This loads variables from .env into os.environ
'''
results = search_with_serpapi("Mahler 5th Symphony meaning")
for r in results:
    print(f"\n📝 {r['title']}\n🔗 {r['link']}\n👉 {r['snippet']}")'''