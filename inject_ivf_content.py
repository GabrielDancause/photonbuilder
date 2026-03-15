import re
import json

file_path = "src/pages/sites/siliconbased/ivf-due-date-calculator.astro"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

explainer_html = """      <h2>Why Standard Pregnancy Math Fails for IVF</h2>
      <p>If you conceive naturally, your obstetrician will calculate your estimated due date (EDD) by adding 280 days (exactly 40 weeks) to the first day of your last menstrual period (LMP). This standard medical formula operates on the assumption that ovulation and conception occurred exactly on day 14 of a perfect 28-day cycle.</p>

      <p>For individuals undergoing In Vitro Fertilization (IVF), this standard assumption is entirely medically inaccurate. IVF cycles involve extensive hormonal suppression and controlled ovarian stimulation, meaning the actual date of your last menstrual period is completely irrelevant to the true gestational age of the embryo. In an IVF setting, the exact moment of fertilization (or the exact age of the embryo at transfer) is known with absolute scientific precision. Therefore, IVF due date calculations must be based on these precise clinical milestones rather than the outdated, generalized LMP method.</p>

      <h2>The Medical Methodology: How We Calculate Your True EDD</h2>
      <p>To determine an accurate IVF due date, medical professionals use the specific timeline of your embryology process. A full-term pregnancy is medically defined as lasting exactly 266 days from the moment of fertilization (not from the LMP). Our calculator reverse-engineers this timeline based on the specific type of procedure you underwent.</p>

      <h3>1. Calculating from Embryo Transfer Date</h3>
      <p>When you undergo a Frozen Embryo Transfer (FET) or a fresh transfer, the embryo has already been growing in a laboratory incubator for several days before being transferred into the uterus. To calculate the due date, we must subtract the age of the embryo from the standard 266-day gestation period.</p>

      <ul>
        <li><strong>For a Day 5 Transfer (Blastocyst):</strong> The formula is: Transfer Date + 266 days - 5 days (which simplifies to Transfer Date + 261 days). Because the embryo has already completed 5 days of its 266-day journey outside the womb, we subtract those 5 days from the total remaining gestation time.</li>
        <li><strong>For a Day 3 Transfer (Cleavage Stage):</strong> The formula is: Transfer Date + 266 days - 3 days (simplifying to Transfer Date + 263 days).</li>
        <li><strong>For a Day 6 Transfer:</strong> While medically similar to a Day 5 transfer, some clinics specifically calculate using the exact 6 days: Transfer Date + 266 days - 6 days (simplifying to Transfer Date + 260 days).</li>
      </ul>

      <h3>2. Calculating from Egg Retrieval / Insemination Date</h3>
      <p>If you prefer to calculate from the date of your egg retrieval (or the date of ICSI/insemination), the math is actually much simpler. The day of retrieval is clinically considered "Day 0" of fertilization.</p>

      <p><strong>The Formula:</strong> Retrieval Date + 266 days.</p>

      <p>In this scenario, we do not subtract the age of the embryo because the retrieval date itself marks the exact starting point of the 266-day developmental clock. This method is exceptionally accurate because it tracks the precise moment the biological clock of the pregnancy began.</p>

      <h2>Understanding Gestational Age vs. Fetal Age</h2>
      <p>One of the most confusing aspects of early IVF pregnancy is understanding how doctors track how "far along" you are. Even though fertilization happened in a lab, obstetricians universally track pregnancy using Gestational Age, which adds an artificial two weeks to the pregnancy timeline.</p>

      <p>Why do they add two weeks? To keep IVF pregnancies aligned with standard natural conception charts. If you transferred a 5-day embryo today, you are not considered "5 days pregnant." Instead, your doctor artificially sets your "last menstrual period" to exactly two weeks and five days prior to today. Therefore, on the exact day of a Day 5 embryo transfer, you are already considered <strong>2 weeks and 5 days pregnant</strong> (or 19 days gestational age). On the day of a Day 3 transfer, you are exactly 2 weeks and 3 days pregnant.</p>

      <p>Our calculator automatically performs these complex adjustments in the background to provide you with your current standard Gestational Age, ensuring the timeline you see perfectly matches the terminology your OB-GYN will use during your ultrasound appointments.</p>

      <h2>The Accuracy of Estimated Due Dates</h2>
      <p>It is crucial to remember that the word "estimated" is doing a lot of heavy lifting. Only about 4% to 5% of babies are actually born precisely on their calculated due date. While the IVF calculation method is vastly more mathematically precise than the natural LMP method, human biology is not a perfectly timed machine.</p>

      <p>A pregnancy is generally considered "full term" anywhere between 37 weeks and 42 weeks of gestation. The EDD generated by this calculator simply serves as the central anchor point (exactly 40 weeks) for your medical team to schedule vital prenatal testing, anatomy scans, and potential induction timelines. Twins or multiples, which are statistically more common in certain IVF protocols, will almost always result in an earlier delivery timeline dictated by your maternal-fetal medicine specialist.</p>

      <p>For those navigating the complex data involved in fertility tracking, you might also appreciate tools that help organize complex matrices of information, such as our <a href="/rref-calculator">RREF Calculator</a>.</p>"""

faq_data = [
    {
        "@type": "Question",
        "name": "Why shouldn't I use the first day of my last period for an IVF due date?",
        "acceptedAnswer": {
            "@type": "Answer",
            "text": "The standard last menstrual period (LMP) calculation assumes ovulation happened exactly 14 days later. In an IVF cycle, your cycle is medically altered, making the LMP completely irrelevant to when fertilization actually occurred. Using the exact transfer or retrieval date provides a clinically precise gestational timeline."
        }
    },
    {
        "@type": "Question",
        "name": "How many days pregnant am I on the day of a 5-day embryo transfer?",
        "acceptedAnswer": {
            "@type": "Answer",
            "text": "To align with standard obstetric charting, your doctor adds an artificial two weeks to your timeline. Therefore, on the day you transfer a 5-day embryo (blastocyst), you are officially considered 2 weeks and 5 days (19 days) pregnant."
        }
    },
    {
        "@type": "Question",
        "name": "Is my egg retrieval date the same as my conception date?",
        "acceptedAnswer": {
            "@type": "Answer",
            "text": "Clinically, yes. The day of your egg retrieval (which is the same day the eggs are fertilized via standard insemination or ICSI) is considered 'Day 0' of embryonic development. It serves as the exact point of conception for medical dating purposes."
        }
    },
    {
        "@type": "Question",
        "name": "Does the due date change if I am pregnant with twins?",
        "acceptedAnswer": {
            "@type": "Answer",
            "text": "The calculated 40-week Estimated Due Date (EDD) does not mathematically change, as it is a fixed milestone. However, twins rarely reach 40 weeks. Most medical professionals consider a twin pregnancy full-term around 37 or 38 weeks, and delivery is usually scheduled accordingly."
        }
    },
    {
        "@type": "Question",
        "name": "What is the difference between a Day 3 and Day 5 embryo transfer calculation?",
        "acceptedAnswer": {
            "@type": "Answer",
            "text": "A Day 5 embryo (blastocyst) has been developing outside the womb for two days longer than a Day 3 embryo (cleavage stage). Therefore, when calculating the due date from the day of transfer, you subtract 261 days for a Day 5 transfer, and 263 days for a Day 3 transfer."
        }
    }
]

faq_html = ""
for faq in faq_data:
    faq_html += f"""      <details>
        <summary>{faq['name']}</summary>
        <p>{faq['acceptedAnswer']['text']}</p>
      </details>\n"""

# Inject Explainer
content = re.sub(r'<!-- Explainer content goes here -->', explainer_html, content)

# Inject FAQ HTML
content = re.sub(r'<!-- FAQs go here -->', faq_html, content)

# Inject JSON-LD Schema
schema_json = json.dumps(faq_data, indent=6)
schema_json = "[\n" + ",\n".join(["      " + json.dumps(item) for item in faq_data]) + "\n    ]"

content = re.sub(r'"mainEntity": \[\]', f'"mainEntity": {schema_json}', content)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)

print("Explainer, FAQ, and Schema injected successfully.")
