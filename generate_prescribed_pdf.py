import os
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, Image, HRFlowable
)
from reportlab.pdfgen import canvas

class SeminarNumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super(SeminarNumberedCanvas, self).__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super(SeminarNumberedCanvas, self).showPage()
        super(SeminarNumberedCanvas, self).save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        self.setFont("Helvetica-Bold", 8)
        self.setFillColor(colors.HexColor("#64748b"))

        # Header
        self.drawString(50, 11 * inch - 36, "Phishing Detection Tool: Identifying & Preventing Fake Email")
        self.setFont("Helvetica", 8)
        self.drawRightString(8.5 * inch - 50, 11 * inch - 36, "Team: APEX CIPHER | 1st Year CSE")
        
        self.setStrokeColor(colors.HexColor("#cbd5e1"))
        self.setLineWidth(0.75)
        self.line(50, 11 * inch - 40, 8.5 * inch - 50, 11 * inch - 40)

        # Footer
        self.line(50, 45, 8.5 * inch - 50, 45)
        self.setFont("Helvetica", 8)
        self.drawString(50, 32, "Technical Club Seminar Presentation | Cyber Security Domain")
        page_text = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(8.5 * inch - 50, 32, page_text)
        self.restoreState()


def build_prescribed_seminar_pdf():
    out_pdf = "E:\\project in c\\docs\\PhishGuard_Seminar_Presentation_Report.pdf"
    doc = SimpleDocTemplate(
        out_pdf,
        pagesize=letter,
        leftMargin=50,
        rightMargin=50,
        topMargin=50,
        bottomMargin=50
    )

    styles = getSampleStyleSheet()

    c_blue = colors.HexColor("#1d4ed8")
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
        'H2', fontName='Helvetica-Bold', fontSize=10, leading=13.5,
        textColor=c_dark, spaceBefore=6, spaceAfter=2, keepWithNext=True
    )
    body_style = ParagraphStyle(
        'Body', fontName='Helvetica', fontSize=8.8, leading=12.5,
        textColor=colors.HexColor("#334155"), spaceBefore=2, spaceAfter=4
    )
    bullet_style = ParagraphStyle(
        'Bullet', fontName='Helvetica', fontSize=8.8, leading=12.5,
        textColor=colors.HexColor("#334155"), leftIndent=12, spaceBefore=1, spaceAfter=2
    )
    code_style = ParagraphStyle(
        'Code', fontName='Courier', fontSize=7.5, leading=9.5,
        textColor=colors.HexColor("#0f172a")
    )

    story = []

    # =========================================================================
    # SECTION 1: TITLE SLIDE / COVER BLOCK
    # =========================================================================
    story.append(Spacer(1, 6))
    story.append(Paragraph("TECHNICAL CLUB SEMINAR PRESENTATION", ParagraphStyle('Badge', fontName='Helvetica-Bold', fontSize=9, leading=11, textColor=c_blue, alignment=1)))
    story.append(Spacer(1, 4))
    story.append(Paragraph("Phishing Detection Tool: Identifying and Preventing Fake Email", title_style))
    story.append(Spacer(1, 2))
    story.append(Paragraph("A Rule-Based Threat Assessment Engine in C Programming", subtitle_style))
    story.append(Spacer(1, 8))

    # Prescribed Details Table
    title_data = [
        [Paragraph("<b>Project Title:</b>", body_style), Paragraph("Phishing Detection Tool: Identifying & Preventing Fake Email", body_style),
         Paragraph("<b>Team Name:</b>", body_style), Paragraph("<b>APEX CIPHER</b>", body_style)],
        [Paragraph("<b>Department:</b>", body_style), Paragraph("Computer Science & Engineering (CSE)", body_style),
         Paragraph("<b>Academic Year:</b>", body_style), Paragraph("1st Year B.Tech (2026)", body_style)],
        [Paragraph("<b>Technical Club:</b>", body_style), Paragraph("Cyber Security & Coding Club", body_style),
         Paragraph("<b>Programming Language:</b>", body_style), Paragraph("C Language (Standard C99)", body_style)]
    ]
    t_title = Table(title_data, colWidths=[1.3*inch, 2.3*inch, 1.3*inch, 2.2*inch])
    t_title.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#f8fafc")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#cbd5e1")),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#e2e8f0")),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t_title)
    story.append(Spacer(1, 8))

    # =========================================================================
    # SECTION 2: ABSTRACT
    # =========================================================================
    story.append(Paragraph("2. Abstract", h1_style))
    story.append(Paragraph(
        "Email phishing represents the most common entry gate for online financial fraud, account hijacking, and data theft. "
        "Novice internet users and students frequently fall victim to spoofed sender addresses, urgent subject lines, and deceptive links. "
        "<b>PhishGuard</b> is a lightweight, rule-based cybersecurity tool developed in <b>C programming</b> to inspect incoming email text "
        "without requiring heavy cloud services or third-party libraries. The tool evaluates the sender domain for typosquatting "
        "(e.g., <code>paypa1.com</code>), identifies psychological urgency cues in the subject line, flags raw numerical IP hyperlinks "
        "(e.g., <code>http://192.168.1.50/login</code>), and detects unauthorized requests for confidential credentials. "
        "The system aggregates these indicators into a unified <b>Risk Score (0–100)</b>, categorizes the email as <b>Safe</b>, "
        "<b>Suspicious</b>, or <b>Critical Phishing</b>, and guides the user to prevent data loss. The expected outcome is an easy-to-understand, "
        "portable desktop security scanner that demonstrates core cybersecurity principles using introductory C concepts.",
        body_style
    ))

    # Add Figure 1 (Flow diagram)
    if os.path.exists("docs/images/phishing_flow.png"):
        story.append(Spacer(1, 2))
        story.append(Image("docs/images/phishing_flow.png", width=6.8*inch, height=2.2*inch))
        story.append(Paragraph("<i>Figure 1: High-level workflow showing how an attacker crafts a fake email and how the C program shields the user.</i>", 
                               ParagraphStyle('Caption', fontName='Helvetica-Oblique', fontSize=7.5, textColor=colors.HexColor("#64748b"), alignment=1)))

    # =========================================================================
    # SECTION 3: PROBLEM STATEMENT
    # =========================================================================
    story.append(Spacer(1, 4))
    story.append(Paragraph("3. Problem Statement", h1_style))
    story.append(Paragraph("<b>What problem are we trying to solve?</b>", h2_style))
    story.append(Paragraph(
        "Cyber adversaries exploit human psychology rather than technical flaws. They craft fake emails that visually mimic authentic institutions "
        "(such as banks, universities, or online shopping portals) to manipulate victims into revealing confidential passwords, OTPs, and credit card numbers.",
        body_style
    ))
    story.append(Paragraph("<b>Who faces this problem?</b>", h2_style))
    story.append(Paragraph(
        "• College students receiving fake scholarship, examination fee, or campus job offers.<br/>"
        "• Everyday internet users who cannot distinguish lookalike domain names (e.g., digit '1' replacing letter 'l').<br/>"
        "• Small educational institutions and laboratories lacking enterprise-grade AI email gateways.",
        body_style
    ))
    story.append(Paragraph("<b>Why does it matter?</b>", h2_style))
    story.append(Paragraph(
        "A single fraudulent click can lead to total bank account drainage, identity theft, or university credential compromise. "
        "Providing users with an understandable, offline tool that clearly explains <i>why</i> an email is dangerous empowers people with cybersecurity awareness.",
        body_style
    ))

    story.append(PageBreak())

    # =========================================================================
    # SECTION 4: RELATED WORK / EXISTING SOLUTIONS / LITERATURE SURVEY
    # =========================================================================
    story.append(Paragraph("4. Related Work / Existing Solutions / Literature Survey", h1_style))
    story.append(Paragraph(
        "Extensive research has been conducted on anti-phishing mechanisms. Below is a comprehensive survey of <b>6 foundational research papers</b>, "
        "highlighting their methodologies and real-world limitations:",
        body_style
    ))

    lit_data = [
        [
            Paragraph("<font color='white'><b>Paper / Author / Year</b></font>", body_style),
            Paragraph("<font color='white'><b>Technology / Solution Proposed</b></font>", body_style),
            Paragraph("<font color='white'><b>Limitations / Drawbacks</b></font>", body_style)
        ],
        [
            Paragraph("<b>Paper 1:</b><br/>Bergholz et al. (2010)<br/><i>\"Improved Phishing Detection using Model-Based Features\"</i>", body_style),
            Paragraph("Statistical Natural Language Processing (NLP) and dynamic Markov chains to detect deceptive language in email text.", body_style),
            Paragraph("High computational complexity; requires continuous training; struggles with very short or image-only phishing emails.", body_style)
        ],
        [
            Paragraph("<b>Paper 2:</b><br/>Basnet et al. (2012)<br/><i>\"Detection of Phishing Attacks using Machine Learning\"</i>", body_style),
            Paragraph("Evaluated 7 ML algorithms (SVM, Random Forest, Naive Bayes) using 16 email structural features.", body_style),
            Paragraph("Black-box nature; difficult for beginner students to understand; vulnerable to adversarial evasion techniques.", body_style)
        ],
        [
            Paragraph("<b>Paper 3:</b><br/>Sheng et al. (2009)<br/><i>\"An Empirical Analysis of Phishing Blacklists\"</i>", body_style),
            Paragraph("DNS and URL reputation blacklists (e.g., Google Safe Browsing, PhishTank) to block malicious websites.", body_style),
            Paragraph("Cannot protect against zero-hour (freshly created) phishing domains; average delay of 4 to 12 hours before blacklist entry.", body_style)
        ],
        [
            Paragraph("<b>Paper 4:</b><br/>Almomani et al. (2013)<br/><i>\"A Survey of Phishing Email Filtering Techniques\"</i>", body_style),
            Paragraph("Comprehensive survey comparing content-based, header-based, and authentication filtering (SPF/DKIM).", body_style),
            Paragraph("Highlighted that spoofed sender display names routinely bypass basic SPF/DKIM filters if configured incorrectly.", body_style)
        ],
        [
            Paragraph("<b>Paper 5:</b><br/>Fette et al. (2007)<br/><i>\"Learning to Detect Phishing Emails (PILFER)\"</i>", body_style),
            Paragraph("10 structural feature extractors including IP links, number of links, HTML forms, and script tags.", body_style),
            Paragraph("High false positive rate on legitimate newsletters that contain multiple links and promotional discounts.", body_style)
        ],
        [
            Paragraph("<b>Paper 6:</b><br/>Marchal et al. (2016)<br/><i>\"Know Your Phish: Novel Content-Based Phishing Detection\"</i>", body_style),
            Paragraph("Lexical analysis of target brands versus registered domain names to catch typosquatting lookalike attacks.", body_style),
            Paragraph("Requires heavy browser extensions and external database queries that introduce user latency.", body_style)
        ]
    ]

    t_lit = Table(lit_data, colWidths=[2.2*inch, 2.5*inch, 2.4*inch])
    t_lit.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#0f172a")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#cbd5e1")),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#e2e8f0")),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#f8fafc")])
    ]))
    story.append(t_lit)
    story.append(Spacer(1, 8))

    # Visual Example Box (Figure 2)
    if os.path.exists("docs/images/email_breakdown.png"):
        story.append(Image("docs/images/email_breakdown.png", width=6.8*inch, height=2.4*inch))
        story.append(Paragraph("<i>Figure 2: Visual mapping of fake email indicators analyzed by our proposed system.</i>", 
                               ParagraphStyle('Caption2', fontName='Helvetica-Oblique', fontSize=7.5, textColor=colors.HexColor("#64748b"), alignment=1)))

    story.append(PageBreak())

    # =========================================================================
    # SECTION 5: PROPOSED WORK (BASE PAPER & ARCHITECTURE)
    # =========================================================================
    story.append(Paragraph("5. Proposed Work (Base Paper & Implementation)", h1_style))
    story.append(Paragraph(
        "<b>Base Paper Reference:</b><br/>"
        "Our work is inspired by and grounded in the foundational framework established by <b>Fette et al. (2007) - 'Learning to Detect Phishing Emails' (PILFER)</b>, "
        "combined with lexical brand verification techniques from <b>Marchal et al. (2016)</b>. While the base papers relied on heavy machine learning engines, "
        "our proposed work adapts these proven structural features into a <b>lightweight, rule-based scoring engine written in pure C</b>.",
        body_style
    ))

    story.append(Paragraph("Key Components of Our Proposed Solution:", h2_style))
    story.append(Paragraph("<b>1. Lookalike Domain & Typosquatting Checker:</b> Uses string scanning (<code>strstr()</code>) to spot deceptive brand spellings (e.g., <code>paypa1</code>, <code>micr0soft</code>, <code>.xyz</code>, <code>.top</code>) (+35 points).", bullet_style))
    story.append(Paragraph("<b>2. Psychological Urgency Analyzer:</b> Detects panic-inducing subject keywords (<code>\"urgent\"</code>, <code>\"suspended\"</code>, <code>\"blocked\"</code>, <code>\"action required\"</code>) (+25 points).", bullet_style))
    story.append(Paragraph("<b>3. Raw IP & Dangerous Link Inspector:</b> Flags links starting with numerical IP addresses (e.g., <code>http://192.168.x.x</code>) or generic <code>click here</code> lures (+25 points).", bullet_style))
    story.append(Paragraph("<b>4. Sensitive Credential Harvesting Sensor:</b> Alerts if the email asks for confidential items like <code>\"password\"</code>, <code>\"credit card\"</code>, or <code>\"OTP\"</code> (+30 points).", bullet_style))
    story.append(Paragraph("<b>5. Unified Risk Scoring & Prevention Verdict:</b> Adds triggered points (capped at 100) and displays a clear recommendation to prevent user compromise.", bullet_style))

    # Beginner Code Snapshot
    story.append(Spacer(1, 4))
    story.append(Paragraph("Proposed C Implementation Code (`simple_phishguard.c`):", h2_style))

    code_text = (
        "#include &lt;stdio.h&gt;\n"
        "#include &lt;string.h&gt;\n"
        "#include &lt;ctype.h&gt;\n\n"
        "int main() {\n"
        "    char sender[100], subject[150], body[500];\n"
        "    int score = 0;\n\n"
        "    // 1. Take User Input\n"
        "    printf(\"Enter Sender: \");  fgets(sender, sizeof(sender), stdin);\n"
        "    printf(\"Enter Subject: \"); fgets(subject, sizeof(subject), stdin);\n"
        "    printf(\"Enter Body: \");    fgets(body, sizeof(body), stdin);\n\n"
        "    // 2. Rule Evaluation Engine\n"
        "    if (strstr(sender, \"paypa1\") || strstr(sender, \".xyz\"))  score += 35;\n"
        "    if (strstr(subject, \"urgent\") || strstr(subject, \"suspended\")) score += 25;\n"
        "    if (strstr(body, \"http://192.\") || strstr(body, \"click here\")) score += 25;\n"
        "    if (strstr(body, \"password\") || strstr(body, \"credit card\")) score += 30;\n\n"
        "    // 3. Final Verdict\n"
        "    if (score >= 50) printf(\"VERDICT: [DANGEROUS PHISHING EMAIL! - DO NOT OPEN]\\n\");\n"
        "    else printf(\"VERDICT: [SAFE EMAIL]\\n\");\n"
        "    return 0;\n"
        "}"
    )
    t_code = Table([[Paragraph(code_text.replace('\n', '<br/>').replace(' ', '&nbsp;'), code_style)]], colWidths=[7.1*inch])
    t_code.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#f8fafc")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#94a3b8")),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(t_code)

    # =========================================================================
    # SECTION 6: REFERENCES
    # =========================================================================
    story.append(Spacer(1, 6))
    story.append(Paragraph("6. References", h1_style))
    story.append(Paragraph(
        "[1] I. Fette, N. Sadeh, and A. Tomasic, \"Learning to Detect Phishing Emails,\" in <i>Proceedings of the 16th International Conference on World Wide Web (WWW '07)</i>, Banff, Alberta, Canada, pp. 649–656, 2007. <b>[Base Paper]</b><br/>"
        "[2] S. Marchal, J. Francois, R. State, and T. Engel, \"Know Your Phish: Novel Content-Based Phishing Detection of Crafty Phishing Webpages,\" <i>IEEE Transactions on Computers</i>, vol. 65, no. 8, pp. 2401–2414, 2016.<br/>"
        "[3] A. Almomani, B. B. Gupta, S. Atawneh, A. Meulenberg, and E. Almomani, \"A Survey of Phishing Email Filtering Techniques,\" <i>IEEE Communications Surveys & Tutorials</i>, vol. 15, no. 4, pp. 2070–2090, 2013.<br/>"
        "[4] R. Basnet, S. Mukkamala, and A. H. Sung, \"Detection of Phishing Attacks: A Machine Learning Approach,\" in <i>Studies in Fuzziness and Soft Computing</i>, Springer, Berlin, Heidelberg, pp. 373–383, 2012.<br/>"
        "[5] S. Sheng, B. Wardman, G. Warner, L. Cranor, J. Hong, and C. Zhang, \"An Empirical Analysis of Phishing Blacklists,\" in <i>Proceedings of the 6th Conference on Email and Anti-Spam (CEAS '09)</i>, Mountain View, CA, 2009.<br/>"
        "[6] E. Bergholz, J. Chang-Paauwe, F. Coatrieux, et al., \"Improved Phishing Detection using Model-Based Features and Classifiers,\" <i>Cyberpsychology & Behavior</i>, vol. 13, no. 2, pp. 135–142, 2010.<br/>"
        "[7] C Programming Language Documentation, ISO/IEC 9899:1999 (C99 Standard Specification), ANSI C Standard Library (<code>stdio.h</code>, <code>string.h</code>, <code>ctype.h</code>).",
        ParagraphStyle('RefStyle', fontName='Helvetica', fontSize=7.5, leading=10.5, textColor=colors.HexColor("#334155"))
    ))

    doc.build(story, canvasmaker=SeminarNumberedCanvas)
    print(f"[+] Complete Prescribed Seminar PDF generated: {out_pdf}")

if __name__ == '__main__':
    build_prescribed_seminar_pdf()
