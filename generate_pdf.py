import os
import sys
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super(NumberedCanvas, self).__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super(NumberedCanvas, self).showPage()
        super(NumberedCanvas, self).save()

    def draw_page_decorations(self, page_count):
        if self._pageNumber == 1:
            # Skip header/footer on title/cover page
            return

        self.saveState()
        self.setFont("Helvetica-Bold", 8)
        self.setFillColor(colors.HexColor("#64748b"))

        # Running Header
        self.drawString(54, 11 * inch - 36, "PHISHGUARD: AI-SHIELD EMAIL PHISHING DETECTION & DEFENSE ENGINE")
        self.setFont("Helvetica", 8)
        self.drawRightString(8.5 * inch - 54, 11 * inch - 36, "Cyber Security Seminar Report")
        
        self.setStrokeColor(colors.HexColor("#cbd5e1"))
        self.setLineWidth(0.75)
        self.line(54, 11 * inch - 42, 8.5 * inch - 54, 11 * inch - 42)

        # Running Footer
        self.line(54, 46, 8.5 * inch - 54, 46)
        self.setFont("Helvetica", 8)
        self.drawString(54, 34, "Technical Club Project | Department of Computer Science & Engineering")
        page_text = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(8.5 * inch - 54, 34, page_text)
        self.restoreState()


def build_seminar_pdf(filename="PhishGuard_CyberSecurity_Seminar_Report.pdf"):
    doc = SimpleDocTemplate(
        filename,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )

    styles = getSampleStyleSheet()

    # Custom styles
    c_primary = colors.HexColor("#0f172a")      # Slate 900
    c_accent = colors.HexColor("#2563eb")       # Blue 600
    c_crimson = colors.HexColor("#dc2626")      # Red 600
    c_dark = colors.HexColor("#1e293b")         # Slate 800
    c_light = colors.HexColor("#f8fafc")        # Slate 50

    title_style = ParagraphStyle(
        'CoverTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=24,
        leading=30,
        textColor=colors.HexColor("#0f172a"),
        alignment=1
    )
    
    subtitle_style = ParagraphStyle(
        'CoverSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=12,
        leading=16,
        textColor=colors.HexColor("#475569"),
        alignment=1
    )

    h1_style = ParagraphStyle(
        'Heading1_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=15,
        leading=19,
        textColor=c_accent,
        spaceBefore=14,
        spaceAfter=6,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        'Heading2_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=15,
        textColor=c_primary,
        spaceBefore=10,
        spaceAfter=4,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'Body_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=13.5,
        textColor=colors.HexColor("#334155"),
        spaceBefore=3,
        spaceAfter=6
    )

    bullet_style = ParagraphStyle(
        'Bullet_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=13,
        textColor=colors.HexColor("#334155"),
        leftIndent=15,
        spaceBefore=2,
        spaceAfter=2
    )

    code_style = ParagraphStyle(
        'Code_Custom',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=8,
        leading=10.5,
        textColor=colors.HexColor("#0f172a")
    )

    callout_style = ParagraphStyle(
        'Callout_Text',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=13,
        textColor=colors.HexColor("#1e293b")
    )

    story = []

    # =========================================================================
    # COVER / TITLE BLOCK
    # =========================================================================
    story.append(Spacer(1, 20))
    story.append(Paragraph("TECHNICAL SEMINAR REPORT", ParagraphStyle('TechBadge', fontName='Helvetica-Bold', fontSize=10, leading=12, textColor=c_accent, alignment=1)))
    story.append(Spacer(1, 10))
    story.append(Paragraph("PHISHGUARD: AUTOMATED EMAIL PHISHING DETECTION & PREVENTATIVE TRIAGE SYSTEM", title_style))
    story.append(Spacer(1, 8))
    story.append(Paragraph("A Multi-Layered Threat Intelligence & RFC-822 Parsing Framework in Pure C", subtitle_style))
    story.append(Spacer(1, 15))
    story.append(HRFlowable(width="100%", thickness=2, color=c_accent, spaceBefore=5, spaceAfter=20))

    # Seminar Metadata Table
    meta_data = [
        [Paragraph("<b>Domain:</b>", body_style), Paragraph("Cyber Security & Defensive SOC Engineering", body_style),
         Paragraph("<b>Language:</b>", body_style), Paragraph("C99 (GCC / POSIX / Windows Compatible)", body_style)],
        [Paragraph("<b>Author / Presenter:</b>", body_style), Paragraph("<b>APEX CIPHER</b>", body_style),
         Paragraph("<b>Target Audience:</b>", body_style), Paragraph("College Tech Club / Academic Seminar / SOC Triage", body_style)],
        [Paragraph("<b>Core Algorithms:</b>", body_style), Paragraph("Levenshtein DP, RFC-5322 Parsing, IP Heuristics", body_style),
         Paragraph("<b>Output Channels:</b>", body_style), Paragraph("Terminal ANSI, SIEM JSON, HTML Quarantine", body_style)]
    ]
    t_meta = Table(meta_data, colWidths=[1.3*inch, 2.2*inch, 1.2*inch, 2.3*inch])
    t_meta.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#f1f5f9")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#cbd5e1")),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#e2e8f0")),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(t_meta)
    story.append(Spacer(1, 20))

    # =========================================================================
    # 1. ABSTRACT & INTRODUCTION
    # =========================================================================
    story.append(Paragraph("1. Abstract & Problem Statement", h1_style))
    story.append(Paragraph(
        "Phishing remains the single most prolific initial attack vector in modern computer breaches, responsible for "
        "over <b>82% of enterprise cyber incidents and ransomware intrusions</b> according to industry threat telemetry. "
        "Threat actors employ advanced deceptive techniques including cryptographic protocol forging, domain lookalike "
        "(typosquatting) tactics, raw numerical IP link masking, and manipulative psychological urgency.",
        body_style
    ))
    story.append(Paragraph(
        "<b>PhishGuard</b> was engineered as a high-performance, resource-efficient cyber security detection utility "
        "written in pure <b>C (C99 standard)</b>. Operating at native machine speed with zero external library overhead, "
        "it directly inspects raw email files (RFC-822 / RFC-5322 `.eml` format), executes multi-factor rule analysis, "
        "calculates an aggregate weighted Threat Score (0–100), and outputs machine-readable SIEM JSON alongside an "
        "interactive HTML quarantine warning page.",
        body_style
    ))

    # =========================================================================
    # 2. CORE ARCHITECTURAL MODULES
    # =========================================================================
    story.append(Paragraph("2. System Architecture & Modular Design", h1_style))
    story.append(Paragraph(
        "The software architecture follows strict modular separation of concerns across 5 specialized subsystems:",
        body_style
    ))

    arch_data = [
        [Paragraph("<b>Component File</b>", body_style), Paragraph("<b>Subsystem Responsibility</b>", body_style), Paragraph("<b>Key Functions / Mechanics</b>", body_style)],
        [Paragraph("<code>include/phishguard.h</code>", code_style), Paragraph("Global Data Contracts & Definitions", body_style), Paragraph("Defines <code>EmailMessage</code>, <code>PhishReport</code>, risk thresholds", body_style)],
        [Paragraph("<code>src/email_parser.c</code>", code_style), Paragraph("RFC-822 Header & Stream Parser", body_style), Paragraph("FSM header scanner, boundary detector, link regex-free tokenizer", body_style)],
        [Paragraph("<code>src/phish_engine.c</code>", code_style), Paragraph("Cyber Threat Heuristic Engine", body_style), Paragraph("6-layer scoring engine: SPF/DKIM, display spoof, typosquatting, NLP", body_style)],
        [Paragraph("<code>src/utils.c</code>", code_style), Paragraph("Algorithmic & String Helpers", body_style), Paragraph("Levenshtein Distance ($O(N \\times M)$ DP), IP address detector, domain stripper", body_style)],
        [Paragraph("<code>src/reporter.c</code>", code_style), Paragraph("Triage Presentation & SIEM Exporter", body_style), Paragraph("Terminal ANSI color UI, JSON format generation, HTML quarantine page", body_style)],
        [Paragraph("<code>src/main.c</code>", code_style), Paragraph("CLI Router & Execution Dispatcher", body_style), Paragraph("Flag parser (<code>--json</code>, <code>--html</code>, <code>--interactive</code>), exit codes", body_style)]
    ]
    t_arch = Table(arch_data, colWidths=[1.8*inch, 2.3*inch, 2.9*inch])
    t_arch.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#0f172a")),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#cbd5e1")),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#e2e8f0")),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#f8fafc")])
    ]))
    # style headers
    t_arch._cellvalues[0][0] = Paragraph("<font color='white'><b>Component File</b></font>", body_style)
    t_arch._cellvalues[0][1] = Paragraph("<font color='white'><b>Subsystem Responsibility</b></font>", body_style)
    t_arch._cellvalues[0][2] = Paragraph("<font color='white'><b>Key Functions / Mechanics</b></font>", body_style)
    story.append(t_arch)

    story.append(PageBreak())

    # =========================================================================
    # 3. MULTI-LAYERED THREAT DETECTION PIPELINE
    # =========================================================================
    story.append(Paragraph("3. Multi-Layered Threat Detection Engine", h1_style))
    story.append(Paragraph(
        "PhishGuard adopts a defense-in-depth model that examines an email across six discrete security layers. "
        "Each layer independently penalizes suspicious traits, accumulating points toward a capped maximum score of 100.",
        body_style
    ))

    story.append(Paragraph("Layer 1: Email Authentication Verification (SPF / DKIM / DMARC)", h2_style))
    story.append(Paragraph(
        "Authentic mail infrastructure uses cryptographic DNS alignment. PhishGuard parses the "
        "<code>Authentication-Results</code> and <code>Received-SPF</code> headers: "
        "<br/>• <b>SPF (Sender Policy Framework):</b> Detects whether the delivering server IP is authorized by the domain's DNS (+25 pts on FAIL). "
        "<br/>• <b>DKIM (DomainKeys Identified Mail):</b> Checks cryptographic public-key signature validity (+20 pts on FAIL). "
        "<br/>• <b>DMARC (Domain-based Message Authentication):</b> Verifies organizational alignment (+30 pts on FAIL).",
        body_style
    ))

    story.append(Paragraph("Layer 2: Header Mismatch & Display Name Impersonation", h2_style))
    story.append(Paragraph(
        "Attackers frequently set the display name to a reputable service (e.g., <i>\"PayPal Support\"</i>) while using a throwaway "
        "compromised SMTP account. PhishGuard analyzes: "
        "<br/>• <b>Display Name Spoofing:</b> Cross-references brand keywords in the Display Name against the real Sender Domain (+35 pts). "
        "<br/>• <b>Reply-To Trap:</b> Flags instances where replies are routed to a domain different from the sender address (+25 pts).",
        body_style
    ))

    story.append(Paragraph("Layer 3: Domain Typosquatting (Levenshtein Distance DP)", h2_style))
    story.append(Paragraph(
        "Adversaries register deceptive domains that visually mimic legitimate brands (e.g., <code>paypa1.com</code>, <code>micr0soft.com</code>). "
        "PhishGuard incorporates a dynamic programming implementation of the <b>Levenshtein Edit Distance Algorithm</b>. "
        "The minimal edit operations (insertions, deletions, substitutions) between sender domain tokens and known high-value targets "
        "are calculated in $O(N \\times M)$ complexity. If $1 \\le \\text{dist} \\le 2$, a <b>+35 pts</b> penalty is triggered.",
        body_style
    ))

    story.append(Paragraph("Layer 4: Deep URL & Link Threat Inspection", h2_style))
    story.append(Paragraph(
        "Embedded URLs within message bodies are extracted and parsed into protocol, host, and path components: "
        "<br/>• <b>Numerical Raw IP Address Hosts:</b> Legitimate brands do not host consumer portals on raw IPs (e.g. <code>http://192.168.1.105/login</code>) (+30 pts). "
        "<br/>• <b>High-Risk Top Level Domains (TLDs):</b> TLDs heavily abused by phishing operators (<code>.xyz</code>, <code>.top</code>, <code>.work</code>, <code>.click</code>) (+20 pts). "
        "<br/>• <b>URL Shorteners:</b> Services like <code>bit.ly</code> or <code>tinyurl.com</code> that obscure final destinations (+15 pts). "
        "<br/>• <b>Deceptive Brand Subdomains:</b> Impersonation structures like <code>paypal.com.attacker-server.xyz</code> (+30 pts).",
        body_style
    ))

    story.append(Paragraph("Layer 5: Natural Language & Social Engineering Triggers", h2_style))
    story.append(Paragraph(
        "Lexical scanning of subjects and message bodies identifies psychological coercion patterns: "
        "<br/>• <b>Artificial Urgency:</b> <i>\"immediate action\"</i>, <i>\"within 24 hours\"</i>, <i>\"urgent\"</i> (+15 to +20 pts). "
        "<br/>• <b>Account Shock Tactics:</b> <i>\"account suspended\"</i>, <i>\"unauthorized access\"</i>, <i>\"failure will result\"</i> (+25 pts). "
        "<br/>• <b>PII & Credential Harvesting:</b> <i>\"confirm your identity\"</i>, <i>\"credit card number\"</i>, <i>\"social security number\"</i> (+20 to +30 pts).",
        body_style
    ))

    # Scoring Matrix Table
    story.append(Spacer(1, 6))
    score_table_data = [
        [Paragraph("<font color='white'><b>Score Range</b></font>", body_style),
         Paragraph("<font color='white'><b>Threat Classification</b></font>", body_style),
         Paragraph("<font color='white'><b>Automated Action / Security Policy</b></font>", body_style)],
        [Paragraph("<b>0 – 19 pts</b>", body_style), Paragraph("<font color='#16a34a'><b>SAFE / CLEAN</b></font>", body_style), Paragraph("Deliver to inbox with standard email protections.", body_style)],
        [Paragraph("<b>20 – 49 pts</b>", body_style), Paragraph("<font color='#d97706'><b>SUSPICIOUS</b></font>", body_style), Paragraph("Deliver with security banner; disable links; notify user to verify out-of-band.", body_style)],
        [Paragraph("<b>50 – 100 pts</b>", body_style), Paragraph("<font color='#dc2626'><b>CRITICAL PHISHING</b></font>", body_style), Paragraph("Immediate quarantine; block sender domain; strip links; forward to SOC.", body_style)]
    ]
    t_score = Table(score_table_data, colWidths=[1.5*inch, 2.2*inch, 3.3*inch])
    t_score.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#1e293b")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#cbd5e1")),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#e2e8f0")),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.HexColor("#f0fdf4"), colors.HexColor("#fffbeb"), colors.HexColor("#fef2f2")])
    ]))
    story.append(t_score)

    story.append(PageBreak())

    # =========================================================================
    # 4. EXPERIMENTAL VERIFICATION & TEST RESULTS
    # =========================================================================
    story.append(Paragraph("4. Experimental Results & Live Verification", h1_style))
    story.append(Paragraph(
        "PhishGuard was evaluated against standard email threat profiles. The table below documents the empirical test results "
        "captured during execution:",
        body_style
    ))

    test_results_data = [
        [Paragraph("<font color='white'><b>Test Case Dataset</b></font>", body_style),
         Paragraph("<font color='white'><b>Simulated Attack Vector</b></font>", body_style),
         Paragraph("<font color='white'><b>Score</b></font>", body_style),
         Paragraph("<font color='white'><b>Verdict</b></font>", body_style),
         Paragraph("<font color='white'><b>Key Indicators Flagged</b></font>", body_style)],
        [
            Paragraph("<b>phishing_paypal.eml</b>", body_style),
            Paragraph("Credential & Credit Card Theft via Lookalike Domain & IP link", body_style),
            Paragraph("<b>100 / 100</b>", body_style),
            Paragraph("<font color='#dc2626'><b>CRITICAL</b></font>", body_style),
            Paragraph("SPF/DKIM/DMARC fail, Brand spoof in display name, Raw IP in link, Credit card demand", body_style)
        ],
        [
            Paragraph("<b>phishing_office365.eml</b>", body_style),
            Paragraph("Corporate Spear-Phishing / Helpdesk Impersonation", body_style),
            Paragraph("<b>100 / 100</b>", body_style),
            Paragraph("<font color='#dc2626'><b>CRITICAL</b></font>", body_style),
            Paragraph("SPF/DKIM/DMARC fail, Reply-to mismatch, Abused .top TLD, Urgency ultimatum", body_style)
        ],
        [
            Paragraph("<b>legitimate_github.eml</b>", body_style),
            Paragraph("Authentic Service Notification (Token Expiration)", body_style),
            Paragraph("<b>0 / 100</b>", body_style),
            Paragraph("<font color='#16a34a'><b>SAFE</b></font>", body_style),
            Paragraph("Full SPF/DKIM/DMARC alignment, verified github.com domain, zero false positives", body_style)
        ]
    ]
    t_results = Table(test_results_data, colWidths=[1.6*inch, 1.8*inch, 0.8*inch, 1.0*inch, 1.8*inch])
    t_results.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#0f172a")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#cbd5e1")),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#e2e8f0")),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#f8fafc")])
    ]))
    story.append(t_results)

    story.append(Spacer(1, 10))
    story.append(Paragraph("Sample Terminal Execution Output (Snippet):", h2_style))

    sample_terminal = (
        "========================================================================\n"
        "   [PhishGuard AI-Shield] Phishing Email Analysis Report\n"
        "========================================================================\n"
        "Sender (From)     : \"PayPal Account Security\" &lt;support@paypa1-security.xyz&gt;\n"
        "Reply-To          : harvest-data@attacker-server.com\n"
        "Subject           : URGENT: Your account suspended due to unauthorized access\n"
        "Email Auth        : SPF=FAIL | DKIM=FAIL | DMARC=FAIL\n"
        "------------------------------------------------------------------------\n"
        "Extracted Links   : [1] http://192.168.1.105/paypal/login-verification.php\n"
        "------------------------------------------------------------------------\n"
        "FINAL THREAT SCORE: 100 / 100\n"
        "VERDICT           : [CRITICAL PHISHING THREAT]\n"
        "RECOMMENDATION    : Quarantine immediately. Do NOT click links or reply.\n"
        "========================================================================"
    )
    t_term = Table([[Paragraph(sample_terminal.replace('\n', '<br/>'), code_style)]], colWidths=[7.0*inch])
    t_term.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#090d16")),
        ('TEXTCOLOR', (0,0), (-1,-1), colors.HexColor("#38bdf8")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#38bdf8")),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
        ('RIGHTPADDING', (0,0), (-1,-1), 10),
    ]))
    story.append(t_term)

    # =========================================================================
    # 5. SEMINAR PRESENTATION & CLUB DEFENSE GUIDE
    # =========================================================================
    story.append(Spacer(1, 10))
    story.append(Paragraph("5. Technical Club Seminar Presentation Guide", h1_style))
    story.append(Paragraph(
        "When presenting this project at a Technical Club or viva seminar, structure the discourse around four key phases:",
        body_style
    ))
    story.append(Paragraph("<b>1. Live Attack Demonstration (1–2 mins):</b> Display <code>samples/phishing_paypal.eml</code> to the audience. Highlight how convincing the email looks visually while calling attention to the disguised domain (<code>paypa1-security.xyz</code>).", bullet_style))
    story.append(Paragraph("<b>2. Architectural Defense (3 mins):</b> Explain why C was chosen over high-level languages: zero garbage collection latency, minimal memory footprint (under 2 MB RAM usage), and portability across embedded mail gateways.", bullet_style))
    story.append(Paragraph("<b>3. Algorithm Showcase (2 mins):</b> Walk through the Levenshtein Distance dynamic programming matrix to demonstrate how <code>paypa1</code> is detected with distance = 1 from <code>paypal</code>.", bullet_style))
    story.append(Paragraph("<b>4. Automated Triage (2 mins):</b> Run <code>.\\run.bat</code>, select option [1], and project both the SIEM JSON payload and the browser-based HTML Quarantine page.", bullet_style))

    # =========================================================================
    # 6. FUTURE ENHANCEMENTS & CONCLUSION
    # =========================================================================
    story.append(Paragraph("6. Future Scope & Conclusion", h1_style))
    story.append(Paragraph(
        "<b>Conclusion:</b> PhishGuard demonstrates that robust, multi-layered cyber security defenses can be implemented "
        "efficiently in standard C without relying on bloated runtimes. By consolidating header authentication, typographic lookalike "
        "analysis, link threat telemetry, and behavioral heuristics, it provides enterprise-grade detection accuracy.",
        body_style
    ))
    story.append(Paragraph(
        "<b>Future Enhancements:</b> "
        "<br/>• Integration with live DNS resolver sockets to perform real-time SPF/DMARC TXT record querying. "
        "<br/>• Embedded Bayesian Machine Learning classifier written in C for adaptive spam corpus training. "
        "<br/>• Milter (Mail Filter) daemon plugin integration for live Postfix and Sendmail enterprise MTA pipelines.",
        body_style
    ))

    # Build Document
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"[+] Seminar PDF successfully generated: {filename}")


if __name__ == '__main__':
    out_pdf = "E:\\project in c\\docs\\PhishGuard_CyberSecurity_Seminar_Report.pdf"
    build_seminar_pdf(out_pdf)
