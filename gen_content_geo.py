import json
import urllib.request
import urllib.parse

def fetch_wiki_summary(title):
    try:
        url = f"https://en.wikipedia.org/w/api.php?action=query&prop=extracts&exintro=1&explaintext=1&titles={urllib.parse.quote(title)}&format=json"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode())
            pages = data['query']['pages']
            return list(pages.values())[0].get('extract', '')
    except Exception as e:
        return ""

def generate_content():
    ipgeo = fetch_wiki_summary("Internet geolocation")
    bgp = fetch_wiki_summary("Border Gateway Protocol")

    html = f"""
    <h2>How IP Geolocation Works</h2>

    <p>Every device connected to the internet is assigned an IP (Internet Protocol) address. While these addresses are primarily used for routing data packets between networks, they also inherently carry geographical information. Our Geo Tracker queries extensive databases that map IP addresses to physical locations, allowing you to instantly determine where a user, server, or website is hosted.</p>

    <h3>The Mechanism Behind the Mapping</h3>
    <p>{ipgeo}</p>

    <p>Unlike GPS, which triangulates a precise location using satellites, IP geolocation relies on databases maintained by Regional Internet Registries (RIRs) and third-party data providers. These organizations keep records of which IP address blocks are allocated to specific Internet Service Providers (ISPs) or organizations in different geographic regions.</p>

    <h3>BGP Routing and ASNs</h3>
    <p>A crucial component of understanding IP addresses is the Border Gateway Protocol (BGP) and Autonomous System Numbers (ASNs). {bgp}</p>

    <p>When you look up an IP address, our tracker often returns an ASN. This number identifies the specific network operator or ISP (like Comcast, AT&T, or AWS) that controls that IP block. Knowing the ASN helps network administrators diagnose routing issues and identify the source of network traffic.</p>

    <h3>Accuracy and Limitations</h3>
    <p>It's important to understand that IP geolocation is not perfect. The accuracy depends heavily on the quality and freshness of the underlying databases. Generally, you can expect the following levels of accuracy:</p>
    <ul>
        <li><strong>Country Level:</strong> 95% to 99% accuracy. It is very reliable for determining the nation from which traffic originates.</li>
        <li><strong>Region/State Level:</strong> 70% to 80% accuracy.</li>
        <li><strong>City Level:</strong> 50% to 75% accuracy. It can often pinpoint the correct metropolitan area but may be assigned to the central hub of an ISP rather than the exact suburb.</li>
    </ul>

    <p>Furthermore, several technologies can obscure a user's true location:</p>
    <ul>
        <li><strong>VPNs (Virtual Private Networks):</strong> Users connecting through a VPN will appear to be located wherever the VPN server is situated, masking their actual IP.</li>
        <li><strong>Proxies:</strong> Similar to VPNs, proxies route traffic through an intermediary server.</li>
        <li><strong>Mobile Networks:</strong> Cellular data networks often route traffic through centralized gateways, making a user in a rural town appear to be in a major city hundreds of miles away.</li>
    </ul>

    <p><em>Need a different kind of calculation? Try our <a href="/conception-calculator">Conception Calculator</a>.</em></p>
    """

    faqs = [
        {"q": "Can an IP address pinpoint my exact house address?", "a": "No. IP geolocation databases typically map IP blocks to the location of the Internet Service Provider's (ISP) local routing equipment, not individual homes. At best, an IP lookup might identify your city or zip code, but it cannot provide a specific street address."},
        {"q": "Why does the tracker show a different city than where I actually am?", "a": "This happens frequently, especially on mobile networks or corporate networks. ISPs often route traffic through regional hubs. If you live in a suburb, your IP might register as the major metropolitan area where your ISP's regional gateway is located."},
        {"q": "What is an ASN?", "a": "ASN stands for Autonomous System Number. It is a globally unique identifier assigned to a network operator (like a large ISP, university, or tech company) that controls a block of IP addresses and routing policies."},
        {"q": "How does a VPN affect my IP location?", "a": "When you use a VPN, your internet traffic is encrypted and routed through a remote server. Websites and IP trackers will see the IP address and geographical location of the VPN server, completely hiding your true physical location."},
        {"q": "Are IPv4 and IPv6 geolocated differently?", "a": "The underlying concept is the same: mapping IP blocks to locations. However, because IPv6 is relatively newer and has a vastly larger address space, some older geolocation databases may struggle to map IPv6 addresses as accurately as IPv4 addresses, though this is rapidly improving."}
    ]

    faq_html = ""
    faq_schema = []

    for faq in faqs:
        faq_html += f"""
        <details class="faq-item">
            <summary>{faq['q']}</summary>
            <p>{faq['a']}</p>
        </details>
        """
        faq_schema.append({
            "@type": "Question",
            "name": faq['q'],
            "acceptedAnswer": {
                "@type": "Answer",
                "text": faq['a']
            }
        })

    print("=== HTML EXPL ===\n" + html + "\n=== HTML FAQ ===\n" + faq_html + "\n=== SCHEMA ===\n" + json.dumps(faq_schema, indent=2))

if __name__ == "__main__":
    generate_content()
