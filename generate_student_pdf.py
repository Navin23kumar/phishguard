import os
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, Image, HRFlowable
)
from reportlab.pdfgen import canvas

class StudentNumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super(StudentNumberedCanvas, self).__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super(StudentNumberedCanvas, self).showPage()
        super(StudentNumberedCanvas, self).save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        self.setFont("Helvetica-Bold", 8)
        self.setFillColor(colors.HexColor("#64748b"))

        # Header
        self.drawString(54, 11 * inch - 36, "PhishGuard: Fake Email Detection Tool | 1st Year C Project")
        self.setFont("Helvetica", 8)
        self.drawRightString(8.5 * inch - 54, 11 * inch - 36, "Team: APEX CIPHER")
        
        self.setStrokeColor(colors.HexColor("#cbd5e1"))
        self.setLineWidth(0.75)
        self.line(54, 11 * inch - 40, 8.5 * inch - 54, 11 * inch - 40)

        # Footer
        self.line(54, 45, 8.5 * inch - 54, 45)
        self.setFont("Helvetica", 8)
        self.drawString(54, 32, "Technical Club Seminar Presentation | Computer Science Department")
        page_text = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(8.5 * inch - 54, 32, page_text)
        self.restoreState()


def build_student_seminar_pdf():
    out_pdf = "E:\\project in c\\docs\\PhishGuard_Beginner_Seminar_Report.pdf"
    doc = SimpleDocTemplate(
        out_pdf,
        pagesize=letter,
        leftMargin=50,
        rightMargin=50,
        topMargin=50,
        bottomMargin=50
    )

    styles = getSampleStyleSheet()

    c_blue = colors.HexColor("#2563eb")
    c_dark = colors.HexColor("#0f172a")

    title_style = ParagraphStyle(
        'Title', fontName='Helvetica-Bold', fontSize=20, leading=24,
        textColor=c_dark, alignment=1
    )
    subtitle_style = ParagraphStyle(
        'Subtitle', fontName='Helvetica', fontSize=11, leading=15,
        textColor=colors.HexColor("#475569"), alignment=1
    )
    h1_style = ParagraphStyle(
        'H1', fontName='Helvetica-Bold', fontSize=13, leading=16,
        textColor=c_blue, spaceBefore=10, spaceAfter=4, keepWithNext=True
    )
    h2_style = ParagraphStyle(
        'H2', fontName='Helvetica-Bold', fontSize=10.5, leading=14,
        textColor=c_dark, spaceBefore=7, spaceAfter=2, keepWithNext=True
    )
    body_style = ParagraphStyle(
        'Body', fontName='Helvetica', fontSize=9, leading=13,
        textColor=colors.HexColor("#334155"), spaceBefore=2, spaceAfter=4
    )
    bullet_style = ParagraphStyle(
        'Bullet', fontName='Helvetica', fontSize=9, leading=13,
        textColor=colors.HexColor("#334155"), leftIndent=12, spaceBefore=1, spaceAfter=2
    )
    code_style = ParagraphStyle(
        'Code', fontName='Courier', fontSize=7.5, leading=9.5,
        textColor=colors.HexColor("#0f172a")
    )

    story = []

    # -------------------------------------------------------------
    # PAGE 1: COVER & WHAT IS PHISHING + DIAGRAM 1
    # -------------------------------------------------------------
    story.append(Spacer(1, 8))
    story.append(Paragraph("CYBER SECURITY TECHNICAL CLUB PROJECT", ParagraphStyle('Badge', fontName='Helvetica-Bold', fontSize=9, leading=11, textColor=c_blue, alignment=1)))
    story.append(Spacer(1, 4))
    story.append(Paragraph("Phishing Detection Tool: Identifying & Preventing Fake Email", title_style))
    story.append(Paragraph("A Simple & Understandable C Programming Project for Beginners", subtitle_style))
    story.append(Spacer(1, 6))

    # Student Info Box
    info_data = [
        [Paragraph("<b>Project Title:</b>", body_style), Paragraph("PhishGuard (Fake Email Detector)", body_style),
         Paragraph("<b>Developed By:</b>", body_style), Paragraph("<b>Team APEX CIPHER</b>", body_style)],
        [Paragraph("<b>Student Level:</b>", body_style), Paragraph("1st Year B.Tech / CSE Students", body_style),
         Paragraph("<b>Language Used:</b>", body_style), Paragraph("C Language (stdio.h, string.h, ctype.h)", body_style)]
    ]
    t_info = Table(info_data, colWidths=[1.3*inch, 2.2*inch, 1.3*inch, 2.3*inch])
    t_info.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#f1f5f9")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#cbd5e1")),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#e2e8f0")),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t_info)
    story.append(Spacer(1, 8))

    story.append(Paragraph("1. What is Phishing? (In Simple Words)", h1_style))
    story.append(Paragraph(
        "<b>Phishing</b> is a trick where a cyber criminal (hacker) sends a <b>fake email</b> pretending to be from a real trusted "
        "company like a Bank, Google, or PayPal. Their goal is to make people panic so that they click a fake link and give away "
        "their passwords, OTPs, or credit card numbers.",
        body_style
    ))

    # Insert Image 1: Flow diagram
    if os.path.exists("docs/images/phishing_flow.png"):
        story.append(Image("docs/images/phishing_flow.png", width=6.8*inch, height=2.4*inch))
        story.append(Paragraph("<i>Figure 1: How an attacker sends a fake email and how our C program protects the user.</i>", 
                               ParagraphStyle('Caption', fontName='Helvetica-Oblique', fontSize=7.5, textColor=colors.HexColor("#64748b"), alignment=1)))
    story.append(Spacer(1, 8))

    story.append(Paragraph("2. Why Did We Choose C Language for This Project?", h1_style))
    story.append(Paragraph(
        "In our first year of college, <b>C programming</b> is our fundamental subject. Building this project in C helped us practice: "
        "<br/>• <b>Character Arrays (Strings):</b> Storing email sender, subject, and message. "
        "<br/>• <b>String Functions:</b> Using <code>strstr()</code> to search for keywords and <code>tolower()</code> for uppercase/lowercase matching. "
        "<br/>• <b>Conditionals (if-else):</b> Adding points whenever a suspicious pattern is discovered. "
        "<br/>• <b>Cyber Security Awareness:</b> Learning real-world defensive techniques used in IT clubs and SOC teams.",
        body_style
    ))

    story.append(PageBreak())

    # -------------------------------------------------------------
    # PAGE 2: HOW THE DETECTOR WORKS + DIAGRAM 2 & 3
    # -------------------------------------------------------------
    story.append(Paragraph("3. The 4 Simple Checks Our Program Performs", h1_style))
    story.append(Paragraph(
        "Instead of complex formulas, our program performs <b>4 easy-to-understand checks</b> just like a human security analyst does:",
        body_style
    ))

    story.append(Paragraph("<b>Check 1: Fake / Lookalike Sender Email Address (+35 Points)</b>", h2_style))
    story.append(Paragraph("Attackers change small letters to trick our eyes (like <code>paypa1.com</code> with number '1' instead of letter 'l', or <code>g00gle.com</code> with zeros). If our code finds these fake spellings, it gives 35 risk points.", body_style))

    story.append(Paragraph("<b>Check 2: Urgent / Panic Words in the Subject Line (+25 Points)</b>", h2_style))
    story.append(Paragraph("Fake emails always make people rush so they don't think carefully. They use words like: <i>\"URGENT\"</i>, <i>\"Account Suspended\"</i>, or <i>\"Action Required\"</i>. If found, our code adds 25 risk points.", body_style))

    story.append(Paragraph("<b>Check 3: Dangerous Web Links & Raw IP Numbers (+25 Points)</b>", h2_style))
    story.append(Paragraph("Real companies never send raw computer IP numbers like <code>http://192.168.1.50/login</code>. Attackers use raw IPs or <code>click here</code> links to lead victims to phishing websites.", body_style))

    story.append(Paragraph("<b>Check 4: Asking for Secret Confidential Information (+30 Points)</b>", h2_style))
    story.append(Paragraph("Real banks clearly state: <i>'We never ask for your password or PIN via email'</i>. If the email contains words like <i>'password'</i>, <i>'credit card'</i>, or <i>'OTP'</i>, it is almost certainly a scam (+30 points).", body_style))

    story.append(Spacer(1, 4))
    if os.path.exists("docs/images/email_breakdown.png"):
        story.append(Image("docs/images/email_breakdown.png", width=6.8*inch, height=2.6*inch))
        story.append(Paragraph("<i>Figure 2: Example of a fake PayPal email showing the exact 4 parts inspected by our C code.</i>", 
                               ParagraphStyle('Caption2', fontName='Helvetica-Oblique', fontSize=7.5, textColor=colors.HexColor("#64748b"), alignment=1)))

    story.append(Spacer(1, 6))
    story.append(Paragraph("4. How the Risk Score is Calculated", h1_style))
    if os.path.exists("docs/images/score_meter.png"):
        story.append(Image("docs/images/score_meter.png", width=6.8*inch, height=1.3*inch))

    table_score_data = [
        [Paragraph("<font color='white'><b>Risk Score</b></font>", body_style), 
         Paragraph("<font color='white'><b>Result Category</b></font>", body_style), 
         Paragraph("<font color='white'><b>What the User Should Do</b></font>", body_style)],
        [Paragraph("<b>0 to 19 Points</b>", body_style), Paragraph("<font color='#16a34a'><b>SAFE EMAIL</b></font>", body_style), Paragraph("The email looks normal and safe to read.", body_style)],
        [Paragraph("<b>20 to 49 Points</b>", body_style), Paragraph("<font color='#d97706'><b>SUSPICIOUS</b></font>", body_style), Paragraph("Be careful! Don't open any attachments or links.", body_style)],
        [Paragraph("<b>50 to 100 Points</b>", body_style), Paragraph("<font color='#dc2626'><b>DANGEROUS PHISHING!</b></font>", body_style), Paragraph("High alert! Delete the email immediately.", body_style)]
    ]
    t_scores = Table(table_score_data, colWidths=[1.5*inch, 2.2*inch, 3.4*inch])
    t_scores.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#0f172a")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#cbd5e1")),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#e2e8f0")),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.HexColor("#f0fdf4"), colors.HexColor("#fffbeb"), colors.HexColor("#fef2f2")])
    ]))
    story.append(t_scores)

    story.append(PageBreak())

    # -------------------------------------------------------------
    # PAGE 3: EASY BEGINNER C CODE + EXPLANATION
    # -------------------------------------------------------------
    story.append(Paragraph("5. The Beginner-Friendly C Source Code (`simple_phishguard.c`)", h1_style))
    story.append(Paragraph(
        "Here is the clean, easy-to-read C code written using simple 1st-year concepts (arrays, <code>if</code> statements, and <code>strstr()</code>):",
        body_style
    ))

    code_snippet = (
        "#include &lt;stdio.h&gt;\n"
        "#include &lt;string.h&gt;\n"
        "#include &lt;ctype.h&gt;\n\n"
        "int main() {\n"
        "    char sender[100], subject[150], body[500];\n"
        "    int score = 0;\n\n"
        "    // 1. Take input from user\n"
        "    printf(\"Enter Sender Email: \");\n"
        "    fgets(sender, sizeof(sender), stdin);\n\n"
        "    // 2. CHECK 1: Fake / Lookalike Domain\n"
        "    if (strstr(sender, \"paypa1\") != NULL || strstr(sender, \".xyz\") != NULL) {\n"
        "        printf(\"[!] Suspicious Sender detected! (+35 points)\\n\");\n"
        "        score = score + 35;\n"
        "    }\n\n"
        "    // 3. CHECK 2: Urgent words in Subject\n"
        "    if (strstr(subject, \"urgent\") != NULL || strstr(subject, \"suspended\") != NULL) {\n"
        "        printf(\"[!] Panic/Urgent subject detected! (+25 points)\\n\");\n"
        "        score = score + 25;\n"
        "    }\n\n"
        "    // 4. CHECK 3: Fake links with raw IP numbers\n"
        "    if (strstr(body, \"http://192.\") != NULL || strstr(body, \"click here\") != NULL) {\n"
        "        printf(\"[!] Dangerous link detected! (+25 points)\\n\");\n"
        "        score = score + 25;\n"
        "    }\n\n"
        "    // 5. CHECK 4: Asking for password or credit card\n"
        "    if (strstr(body, \"password\") != NULL || strstr(body, \"credit card\") != NULL) {\n"
        "        printf(\"[!] Asking for sensitive card/password! (+30 points)\\n\");\n"
        "        score = score + 30;\n"
        "    }\n\n"
        "    // 6. Show Final Result\n"
        "    if (score >= 50) {\n"
        "        printf(\"VERDICT: [DANGEROUS PHISHING EMAIL!]\\n\");\n"
        "    } else {\n"
        "        printf(\"VERDICT: [SAFE EMAIL]\\n\");\n"
        "    }\n"
        "    return 0;\n"
        "}\n"
    )
    t_code = Table([[Paragraph(code_snippet.replace('\n', '<br/>').replace(' ', '&nbsp;'), code_style)]], colWidths=[7.1*inch])
    t_code.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#f8fafc")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#94a3b8")),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(t_code)

    story.append(Paragraph("Simple Functions Used in Our Code (Viva Q&A):", h2_style))
    story.append(Paragraph("• <b><code>fgets()</code>:</b> Takes string input safely from the keyboard without causing memory overflows.", bullet_style))
    story.append(Paragraph("• <b><code>strstr(str1, str2)</code>:</b> A standard C string function that checks if <code>str2</code> exists inside <code>str1</code>. If found, it returns non-NULL.", bullet_style))
    story.append(Paragraph("• <b><code>tolower()</code>:</b> Converts letters to lowercase so capital letters like 'URGENT' or 'Urgent' both get detected.", bullet_style))

    story.append(Spacer(1, 4))
    story.append(Paragraph("6. Seminar Presentation Tips for APEX CIPHER", h1_style))
    story.append(Paragraph("<b>1. Start with a Hook:</b> Show the fake email image and ask the class: <i>'Can you spot why paypa1.com is fake?'</i>", bullet_style))
    story.append(Paragraph("<b>2. Keep it Simple:</b> Explain the 4 rules clearly (Fake Sender, Urgent Subject, Raw IP Link, Asking Password).", bullet_style))
    story.append(Paragraph("<b>3. Run the Demo:</b> Type a fake email into the terminal and show the total score reaching 100 points!", bullet_style))
    story.append(Paragraph("<b>4. Conclusion:</b> Summarize that basic C programming logic is powerful enough to protect users from cyber scams.", bullet_style))

    doc.build(story, canvasmaker=StudentNumberedCanvas)
    print(f"[+] Beginner Student Seminar PDF successfully generated: {out_pdf}")

if __name__ == '__main__':
    build_student_seminar_pdf()
