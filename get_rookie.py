import urllib.request
import json
import urllib.parse

def fetch_wiki_data(title):
    title_encoded = urllib.parse.quote(title)
    url = f"https://en.wikipedia.org/w/api.php?action=query&prop=extracts&exintro=1&explaintext=1&titles={title_encoded}&format=json"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})

    with urllib.request.urlopen(req) as response:
        data = json.loads(response.read().decode())
        pages = data['query']['pages']
        for page_id, page_data in pages.items():
            if page_id != "-1":
                return page_data.get('extract', 'No extract found.')
    return 'Not found'

print(fetch_wiki_data("List_of_The_Rookie_episodes"))
