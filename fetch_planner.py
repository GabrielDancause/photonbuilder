import urllib.request
import urllib.parse
import json

def fetch_wiki(title):
    url = f"https://en.wikipedia.org/w/api.php?action=query&prop=extracts&explaintext=1&titles={urllib.parse.quote(title)}&format=json"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req) as response:
        data = json.loads(response.read())
        pages = data['query']['pages']
        for page_id, page_info in pages.items():
            if 'extract' in page_info:
                print(page_info['extract'][:2000])
                print("\n================\n")

fetch_wiki("Personal organizer")
