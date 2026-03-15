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
    naegele = fetch_wiki_summary("Naegele's rule")
    gestational = fetch_wiki_summary("Gestational age")

    html = f"""
    <h2>The Science Behind the Conception Calculator</h2>

    <p>Understanding when conception occurs is crucial for estimating a baby's due date and tracking fetal development. The journey from conception to birth is a complex biological process, and healthcare professionals rely on established mathematical models to estimate these key milestones. Our Conception Date Calculator uses standard obstetrical rules to reverse-engineer your conception date based on your Last Menstrual Period (LMP) or expected due date.</p>

    <h3>How Conception Dates are Calculated</h3>
    <p>The most common method for calculating estimated due dates (EDD) and conception dates is <strong>Naegele's rule</strong>. {naegele}</p>

    <p>Naegele's rule assumes a standard 28-day menstrual cycle with ovulation occurring on day 14. Therefore, the formula is:</p>
    <ul>
        <li><strong>Estimated Due Date (EDD)</strong> = First Day of LMP + 280 days (40 weeks)</li>
        <li><strong>Conception Date</strong> = EDD - 266 days (38 weeks)</li>
    </ul>

    <h3>Adjusting for Cycle Length</h3>
    <p>Not everyone has a 28-day cycle. If a cycle is longer or shorter, ovulation (and therefore conception) likely occurs on a different day. Our calculator adjusts Naegele's rule by adding or subtracting the difference between the user's cycle length and the standard 28 days. For example, in a 32-day cycle, ovulation typically occurs around day 18, so the estimated due date and conception date are pushed back by 4 days.</p>

    <h3>Gestational Age vs. Fetal Age</h3>
    <p>A common point of confusion is the difference between gestational age and fetal age. {gestational}</p>

    <p>Because it is difficult to pinpoint the exact moment of conception, healthcare providers start counting pregnancy weeks from the first day of the last menstrual period (gestational age). This means that during the first two weeks of a calculated pregnancy, a person is not actually pregnant yet. The actual age of the fetus (fetal age) is typically two weeks less than the gestational age.</p>

    <h3>Limitations of the Calculator</h3>
    <p>While mathematical models like Naegele's rule are useful baselines, they are only estimates. Several factors can affect the true conception and due dates:</p>
    <ul>
        <li><strong>Irregular Cycles:</strong> If cycle lengths vary significantly month-to-month, relying on LMP can be inaccurate.</li>
        <li><strong>Varying Luteal Phases:</strong> Ovulation does not always happen exactly 14 days before the next period.</li>
        <li><strong>Implantation Timing:</strong> The fertilized egg can take between 6 to 12 days to implant in the uterus.</li>
    </ul>
    <p>For the most accurate assessment of gestational age and conception dates, healthcare providers rely on early ultrasound measurements, particularly the crown-rump length (CRL) taken during the first trimester.</p>

    <p><em>Curious about how IP addresses are mapped to physical locations? Check out our <a href="/geo-tracker">Geo Tracker</a> tool.</em></p>
    """

    faqs = [
        {"q": "How accurate is a conception calculator?", "a": "Conception calculators provide a solid estimate based on standard medical formulas like Naegele's rule. However, because menstrual cycles vary and ovulation isn't always perfectly predictable, the calculated date is typically an estimate within a few days. Ultrasounds in the first trimester offer the most accurate dating."},
        {"q": "Why is my pregnancy calculated from my last period instead of conception?", "a": "Medical professionals use the first day of your Last Menstrual Period (LMP) because it is a known, easily identifiable date. Pinpointing the exact day of ovulation or fertilization is much more difficult. Therefore, pregnancies are universally measured in 'gestational age' starting from the LMP."},
        {"q": "Can I conceive on a day other than my ovulation day?", "a": "Conception itself (the fertilization of the egg) must happen within 12-24 hours after ovulation. However, sperm can live in the female reproductive tract for up to 5 days. This means you can have intercourse several days before ovulation and still conceive."},
        {"q": "How does cycle length affect conception dates?", "a": "If your cycle is longer than 28 days, you likely ovulate later than day 14. For instance, in a 35-day cycle, ovulation might occur around day 21. A good calculator adjusts the estimated due date and conception date to account for these longer or shorter cycles."},
        {"q": "Is the due date the same as the delivery date?", "a": "No. The Estimated Due Date (EDD) is simply the 40-week mark from the LMP. Only about 4-5% of babies are actually born on their exact due date. A pregnancy is considered full-term anywhere between 37 and 42 weeks."}
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
