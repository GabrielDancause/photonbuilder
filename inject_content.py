import re
import json

file_path = "src/pages/sites/siliconbased/rref-calculator.astro"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

explainer_html = """      <h2>What is Reduced Row Echelon Form (RREF)?</h2>
      <p>The Reduced Row Echelon Form (RREF) is a canonical form of a matrix used primarily in linear algebra to solve systems of linear equations. When a matrix is transformed into its RREF, the solutions to the corresponding system become immediately apparent. This transformation is achieved through a systematic process known as Gaussian elimination, or more specifically, Gauss-Jordan elimination.</p>

      <p>A matrix is in Reduced Row Echelon Form if it satisfies the following four specific conditions:</p>
      <ul>
        <li><strong>Zero Rows at the Bottom:</strong> Any rows consisting entirely of zeros are grouped at the very bottom of the matrix.</li>
        <li><strong>Leading Ones:</strong> The first non-zero entry in every non-zero row is a 1. This entry is called the "leading 1" or "pivot."</li>
        <li><strong>Staircase Pattern:</strong> The leading 1 of any given row must be strictly to the right of the leading 1 of the row immediately above it.</li>
        <li><strong>Column Clearance:</strong> Every leading 1 is the absolute only non-zero entry in its entire column. All other entries in that column (both above and below the leading 1) must be exactly zero.</li>
      </ul>

      <p>Understanding these conditions is critical. While many matrices can be transformed into a standard Row Echelon Form (REF) in various ways, every single matrix has exactly one unique Reduced Row Echelon Form. This uniqueness makes RREF an invaluable tool in theoretical and applied mathematics.</p>

      <h2>The Gaussian Elimination Methodology</h2>
      <p>To convert a standard matrix into its Reduced Row Echelon Form, we perform a sequence of Elementary Row Operations. There are exactly three permissible operations you can perform without altering the fundamental solution set of the system the matrix represents:</p>

      <ol>
        <li><strong>Row Swapping:</strong> You can interchange any two rows. This is often necessary when the current pivot position is a zero.</li>
        <li><strong>Scalar Multiplication:</strong> You can multiply an entire row by any non-zero constant. This is primarily used to turn a non-zero entry into a leading 1.</li>
        <li><strong>Row Addition:</strong> You can add a multiple of one row to another row. This is the crucial operation used to clear out the non-zero entries above and below your leading 1s.</li>
      </ol>

      <p>Our RREF calculator algorithmically applies these operations following a strict left-to-right, top-to-bottom methodology.</p>

      <h3>Step-by-Step RREF Algorithm</h3>
      <p>The algorithm begins at the top-left corner of the matrix and proceeds column by column. Let's break down the exact sequence of logical steps our calculator executes:</p>

      <p><strong>1. Identify the Pivot Column:</strong> Starting from the leftmost column, find the first column that contains at least one non-zero entry. This becomes your current working column.</p>

      <p><strong>2. Select the Pivot Element:</strong> Look at the entries in your pivot column, starting from the current top row downwards. Find a non-zero entry to act as your pivot. If the entry in the current top row is zero, you must perform a row swap with a row below it that has a non-zero entry in that column. Our algorithm prioritizes numerical stability here, though in exact fractional arithmetic, any non-zero pivot works perfectly.</p>

      <p><strong>3. Create the Leading 1:</strong> Once you have a non-zero pivot securely in position, multiply the entire row by the reciprocal of the pivot's value. If your pivot is 5, you multiply the entire row by 1/5. This forces the pivot position to become exactly 1.</p>

      <p><strong>4. Clear the Column:</strong> Now that you have a leading 1, you must use it to eliminate every other non-zero entry in that specific column. For every other row (both above and below), you subtract a multiple of the pivot row from that target row. If the target row has a 3 in the pivot column, you subtract 3 times the pivot row from it. This ensures the leading 1 stands entirely alone in its column.</p>

      <p><strong>5. Advance and Repeat:</strong> Once the column is cleared, you move down to the next row and over to the next column to the right. You repeat steps 1 through 4 until you either run out of rows or run out of columns.</p>

      <h2>Practical Applications of RREF</h2>
      <p>Why do developers, engineers, and mathematicians care so deeply about the Reduced Row Echelon Form? It is the skeleton key for unlocking numerous linear algebra problems.</p>

      <p><strong>Solving Linear Systems:</strong> This is the most direct application. If you have a system of variables (x, y, z), you can write it as an augmented matrix. Calculating the RREF immediately gives you the solution. If the final row reads <code>[0 0 1 | 5]</code>, you instantly know that z = 5. If a row reads <code>[0 0 0 | 1]</code>, you know the system is entirely inconsistent and has no solution.</p>

      <p><strong>Finding Matrix Inverses:</strong> To find the inverse of an n × n matrix A, you can create a block matrix <code>[A | I]</code>, where I is the identity matrix. By transforming this entire augmented matrix into RREF, the left side becomes the identity matrix, and the right side magically transforms into the inverse matrix A⁻¹. It is a brilliantly efficient mechanical process.</p>

      <p><strong>Determining Rank and Nullity:</strong> The rank of a matrix is simply the number of non-zero rows present in its Reduced Row Echelon Form. This tells you the number of linearly independent rows or columns in the original matrix, which is crucial for understanding the dimensionality of data spaces in machine learning and 3D graphics.</p>

      <h2>Computational Complexities and Fractional Precision</h2>
      <p>Building a robust RREF calculator is not merely about writing a simple loop. The primary challenge lies in floating-point arithmetic. If you use standard JavaScript decimals to perform Gaussian elimination, rounding errors rapidly accumulate. A value that mathematically should be exactly 0 might become <code>0.000000000000001</code>. When the algorithm later attempts to use this tiny number as a pivot, it scales the row by a massive, completely incorrect factor, destroying the entire calculation.</p>

      <p>To solve this, our RREF calculator employs a custom <strong>Fraction Class</strong>. Instead of converting inputs like "1/3" into <code>0.333333</code>, the calculator maintains the exact numerator and denominator throughout the entire calculation. When dividing rows or subtracting multiples, it calculates the exact Greatest Common Divisor (GCD) to keep the fractions simplified. This ensures that the final Reduced Row Echelon Form is mathematically flawless, completely bypassing the catastrophic floating-point errors that plague naive matrix calculators.</p>

      <p>While calculating matrices, if you're working on broader life planning, you might also find our new <a href="/ivf-due-date-calculator">IVF Due Date Calculator</a> helpful for specific timeline projections.</p>"""

faq_data = [
    {
        "@type": "Question",
        "name": "What does RREF stand for?",
        "acceptedAnswer": {
            "@type": "Answer",
            "text": "RREF stands for Reduced Row Echelon Form. It is a specific state of a matrix where every leading entry is a 1, it is the only non-zero entry in its column, and the leading 1s form a staircase pattern moving down and to the right."
        }
    },
    {
        "@type": "Question",
        "name": "How is RREF different from REF?",
        "acceptedAnswer": {
            "@type": "Answer",
            "text": "REF (Row Echelon Form) only requires that the leading entries form a staircase pattern and that rows of zeros are at the bottom. RREF adds two stricter rules: every leading entry must be exactly 1, and every leading 1 must be the ONLY non-zero entry in its entire column."
        }
    },
    {
        "@type": "Question",
        "name": "Is the Reduced Row Echelon Form of a matrix unique?",
        "acceptedAnswer": {
            "@type": "Answer",
            "text": "Yes. While a given matrix can be transformed into many different valid Row Echelon Forms depending on the sequence of operations used, every matrix has exactly one, completely unique Reduced Row Echelon Form."
        }
    },
    {
        "@type": "Question",
        "name": "Can a matrix have no solution in RREF?",
        "acceptedAnswer": {
            "@type": "Answer",
            "text": "If you are using an augmented matrix to solve a system of linear equations, you can determine it has no solution if the RREF contains a row where all coefficient columns are zero, but the final augmented column is non-zero (e.g., [0 0 0 | 1]). This translates to the impossible equation 0 = 1."
        }
    },
    {
        "@type": "Question",
        "name": "Why does this calculator use fractions instead of decimals?",
        "acceptedAnswer": {
            "@type": "Answer",
            "text": "Gaussian elimination involves heavy division and subtraction. Using standard computer decimals introduces floating-point rounding errors that can completely break the algorithm (treating a tiny error as a valid pivot). Using exact fractions guarantees a mathematically perfect result."
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
# Fix the indentation slightly for the array items
schema_json = "[\n" + ",\n".join(["      " + json.dumps(item) for item in faq_data]) + "\n    ]"

content = re.sub(r'"mainEntity": \[\]', f'"mainEntity": {schema_json}', content)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)

print("Explainer, FAQ, and Schema injected successfully.")
