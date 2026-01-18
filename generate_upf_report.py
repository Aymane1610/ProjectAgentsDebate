
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import os

def create_pdf(output_path):
    c = canvas.Canvas(output_path, pagesize=letter)
    width, height = letter

    # Title
    c.setFont("Helvetica-Bold", 18)
    c.drawCentredString(width/2, height - 50, "UPF DEEP INTELLIGENCE REPORT 2024")
    
    c.setFont("Helvetica", 10)
    c.drawCentredString(width/2, height - 70, "Confidential Document - Internal Use Only")
    
    # Body
    text_content = [
        ("1. STRATEGIC VISION & HYBRID LEARNING", [
            "The University (UPF) is moving towards a 60/40 Hybrid Model. 60% of courses in Computer Science",
            "are now digital. However, Architecture and Civil Engineering require 100% physical presence.",
            "Contradiction Notice: While the website claims 'Flexibility', the Internal Rule 402 states that",
            "missing 2 physical labs leads to immediate failure."
        ]),
        ("2. ENGINEERING PROGRAMS & HIDDEN COSTS", [
            "- COMPUTER ENGINEERING: Yearly tuition is 55,000 MAD. ",
            "  *Hidden Cost A: Laboratory Access Fee of 5,000 MAD for AI Research.",
            "  *Hidden Cost B: Cloud Computing Subscription (AWS/Azure) is NOT included (approx. 2,000 MAD/year).",
            "- CIVIL ENGINEERING: Yearly tuition is 52,000 MAD.",
            "  *Constraint: Mandatory 3rd-year internship is strictly NON-PAID. Students must cover travel costs.",
            "  *Benefit: 100% job placement in Fes region, but only 40% in Casablanca."
        ]),
        ("3. ADMISSION - THE GATEKEEPER SYSTEM", [
            "Option A: Direct Admission for Baccalaureate 'Tres Bien' (16+/20).",
            "Option B: The 'Technical Battle' - A 4-hour entrance exam on July 15th for others.",
            "English Proficiency: A mandatory B2 test is required. If failed, students must take a",
            "Mandatory Summer Bridge Program costing 4,500 MAD."
        ]),
        ("4. CAMPUS INFRASTRUCTURE REALITY", [
            "The new 'Eco-Campus' is marketed as fully operational. ",
            "Fact-Check: Blocks C and D (Laboratories) are still under construction until September 2025.",
            "Students will share temporary facilities in the Old Wing during the 2024-2025 season."
        ]),
        ("5. STATISTICAL PERFORMANCE", [
            "Computer Science Insertion Rate: 92% within 6 months.",
            "Civil Engineering Insertion Rate: 68% within 6 months (Market slowdown detected).",
            "Architecture Satisfaction Rate: 88% but lowest starting salaries (Avg 7,500 MAD)."
        ])
    ]

    y_pos = height - 110
    for title, lines in text_content:
        c.setFont("Helvetica-Bold", 12)
        c.drawString(50, y_pos, title)
        y_pos -= 20
        c.setFont("Helvetica", 10)
        for line in lines:
            c.drawString(70, y_pos, line)
            y_pos -= 15
        y_pos -= 10

    c.save()
    print(f"PDF Successfully created at {output_path}")

if __name__ == "__main__":
    kb_dir = os.path.join(os.getcwd(), "knowledge_base")
    if not os.path.exists(kb_dir):
        os.makedirs(kb_dir)
    
    pdf_path = os.path.join(kb_dir, "UPF_Deep_Intelligence_Report_2024.pdf")
    create_pdf(pdf_path)
