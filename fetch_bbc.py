import urllib.request
import ssl
import re

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

req = urllib.request.Request(
    'https://www.bbc.com/news/articles/cwyvxejqyx4o?at_medium=RSS&at_campaign=rss',
    headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
)

try:
    with urllib.request.urlopen(req, context=ctx) as response:
        html = response.read().decode('utf-8')
        paragraphs = re.findall(r'<p[^>]*>(.*?)</p>', html)
        article_text = []
        for p in paragraphs:
            clean_p = re.sub(r'<[^>]+>', '', p).strip()
            if clean_p and len(clean_p) > 50: # filter out nav items
                article_text.append(clean_p)

        print("\n\n".join(article_text))
except Exception as e:
    print(f"Error: {e}")
