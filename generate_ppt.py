import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

def create_seminar_presentation():
    prs = Presentation()
    # 16:9 widescreen slides
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # Professional Cyber Security Color Palette
    C_BG_DARK = RGBColor(15, 23, 42)       # Slate 900
    C_CARD_DARK = RGBColor(30, 41, 59)     # Slate 800
    C_BLUE = RGBColor(37, 99, 235)         # Blue 600
    C_CYAN = RGBColor(56, 189, 248)        # Sky 400
    C_WHITE = RGBColor(255, 255, 255)
    C_GRAY = RGBColor(148, 163, 184)       # Slate 400
    C_LIGHT_BG = RGBColor(248, 250, 252)   # Slate 50
    C_RED = RGBColor(239, 68, 68)          # Red 500
    C_GREEN = RGBColor(34, 197, 94)        # Green 500

    def add_header(slide, title_text, category_text="CYBER SECURITY TECHNICAL CLUB SEMINAR"):
        # Top banner shape
        top_bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(1.1))
        top_bar.fill.solid()
        top_bar.fill.fore_color.rgb = C_BG_DARK
        top_bar.line.color.rgb = C_BLUE
        top_bar.line.width = Pt(1.5)

        tx_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.12), Inches(11.7), Inches(0.85))
        tf = tx_box.text_frame
        tf.word_wrap = True
        
        p0 = tf.paragraphs[0]
        p0.text = category_text.upper()
        p0.font.size = Pt(10)
        p0.font.bold = True
        p0.font.color.rgb = C_CYAN

        p1 = tf.add_paragraph()
        p1.text = title_text
        p1.font.size = Pt(20)
        p1.font.bold = True
        p1.font.color.rgb = C_WHITE

        # Footer
        ft_box = slide.shapes.add_textbox(Inches(0.8), Inches(7.05), Inches(11.7), Inches(0.35))
        ft_tf = ft_box.text_frame
        ft_p = ft_tf.paragraphs[0]
        ft_p.text = "PhishGuard: Fake Email Detection Tool  |  Team: APEX CIPHER  |  1st Year B.Tech CSE"
        ft_p.font.size = Pt(9.5)
        ft_p.font.color.rgb = C_GRAY

    # =========================================================================
    # SLIDE 1: TITLE SLIDE
    # =========================================================================
    slide1 = prs.slides.add_slide(blank_layout)
    bg1 = slide1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(7.5))
    bg1.fill.solid()
    bg1.fill.fore_color.rgb = C_BG_DARK
    bg1.line.fill.background()

    # Title Card container
    card1 = slide1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.2), Inches(0.9), Inches(10.933), Inches(5.7))
    card1.fill.solid()
    card1.fill.fore_color.rgb = C_CARD_DARK
    card1.line.color.rgb = C_CYAN
    card1.line.width = Pt(2)

    tb1 = slide1.shapes.add_textbox(Inches(1.6), Inches(1.2), Inches(10.133), Inches(2.2))
    tf1 = tb1.text_frame
    tf1.word_wrap = True

    p = tf1.paragraphs[0]
    p.text = "TECHNICAL CLUB SEMINAR PRESENTATION"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = C_CYAN
    p.alignment = PP_ALIGN.CENTER

    p = tf1.add_paragraph()
    p.text = "Phishing Detection Tool:\nIdentifying and Preventing Fake Email"
    p.font.size = Pt(28)
    p.font.bold = True
    p.font.color.rgb = C_WHITE
    p.alignment = PP_ALIGN.CENTER

    p = tf1.add_paragraph()
    p.text = "A Rule-Based Threat Assessment Engine in C Programming"
    p.font.size = Pt(14)
    p.font.color.rgb = C_GRAY
    p.alignment = PP_ALIGN.CENTER

    # Metadata Grid Boxes on Slide 1
    details = [
        ("Team Name", "APEX CIPHER", C_CYAN),
        ("Department", "Computer Science & Engg (CSE)", C_WHITE),
        ("Academic Year", "1st Year B.Tech (2026)", C_WHITE),
        ("Technical Club", "Cyber Security & Coding Club", C_CYAN),
        ("Language Used", "C Programming (Standard C99)", C_GREEN),
        ("Core Focus", "Fake Email & URL Detection", C_WHITE),
    ]

    for idx, (lbl, val, col) in enumerate(details):
        r = idx // 3
        c = idx % 3
        x = Inches(1.6 + c * 3.4)
        y = Inches(3.8 + r * 1.3)
        w = Inches(3.2)
        h = Inches(1.05)

        s_box = slide1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, y, w, h)
        s_box.fill.solid()
        s_box.fill.fore_color.rgb = C_BG_DARK
        s_box.line.color.rgb = RGBColor(51, 65, 85)
        s_box.line.width = Pt(1)

        t_box = slide1.shapes.add_textbox(x, y, w, h)
        tf = t_box.text_frame
        tf.word_wrap = True
        
        p = tf.paragraphs[0]
        p.text = lbl.upper()
        p.font.size = Pt(9.5)
        p.font.bold = True
        p.font.color.rgb = C_GRAY
        
        p2 = tf.add_paragraph()
        p2.text = val
        p2.font.size = Pt(12)
        p2.font.bold = True
        p2.font.color.rgb = col

    # =========================================================================
    # SLIDE 2: ABSTRACT
    # =========================================================================
    slide2 = prs.slides.add_slide(blank_layout)
    add_header(slide2, "2. Abstract - Project Summary & Outcome")

    # Left content box
    c_left = slide2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.4), Inches(6.0), Inches(5.3))
    c_left.fill.solid()
    c_left.fill.fore_color.rgb = C_CARD_DARK
    c_left.line.color.rgb = RGBColor(51, 65, 85)

    tb2 = slide2.shapes.add_textbox(Inches(1.0), Inches(1.6), Inches(5.6), Inches(4.9))
    tf2 = tb2.text_frame
    tf2.word_wrap = True

    items2 = [
        ("The Proposed Idea", "Build a lightweight, offline desktop scanner in pure C to detect fake phishing emails without requiring heavy cloud AI models or external Python libraries."),
        ("The Problem Addressed", "Attackers deceive students and non-technical users using lookalike domains (paypa1), artificial urgency (account suspended), and raw IP links (192.168.x.x)."),
        ("The Expected Outcome", "An automated scanner that calculates an accurate Risk Score (0–100), outputs immediate verdicts (SAFE or CRITICAL), and guides users with prevention advice.")
    ]

    for title, desc in items2:
        p = tf2.add_paragraph() if tf2.paragraphs[0].text else tf2.paragraphs[0]
        p.text = f"• {title}:"
        p.font.size = Pt(13)
        p.font.bold = True
        p.font.color.rgb = C_CYAN
        
        p_desc = tf2.add_paragraph()
        p_desc.text = desc
        p_desc.font.size = Pt(11)
        p_desc.font.color.rgb = C_WHITE
        p_desc.space_after = Pt(14)

    # Right Box with Image
    c_right = slide2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(7.1), Inches(1.4), Inches(5.4), Inches(5.3))
    c_right.fill.solid()
    c_right.fill.fore_color.rgb = C_CARD_DARK
    c_right.line.color.rgb = C_BLUE
    c_right.line.width = Pt(1.5)

    img_flow = "docs/images/phishing_flow.png"
    if os.path.exists(img_flow):
        slide2.shapes.add_picture(img_flow, Inches(7.3), Inches(2.3), Inches(5.0), Inches(2.2))

    cap_box = slide2.shapes.add_textbox(Inches(7.3), Inches(4.8), Inches(5.0), Inches(1.4))
    ctf = cap_box.text_frame
    ctf.word_wrap = True
    cp = ctf.paragraphs[0]
    cp.text = "Figure 1: High-Level Workflow"
    cp.font.size = Pt(11)
    cp.font.bold = True
    cp.font.color.rgb = C_CYAN
    cp.alignment = PP_ALIGN.CENTER
    cp2 = ctf.add_paragraph()
    cp2.text = "Attacker sends fake email -> PhishGuard inspects 4 security layers in C -> Alerts user before data theft occurs."
    cp2.font.size = Pt(9.5)
    cp2.font.color.rgb = C_GRAY
    cp2.alignment = PP_ALIGN.CENTER

    # =========================================================================
    # SLIDE 3: PROBLEM STATEMENT
    # =========================================================================
    slide3 = prs.slides.add_slide(blank_layout)
    add_header(slide3, "3. Problem Statement - Why This Project Matters")

    cards3 = [
        ("WHAT PROBLEM ARE WE SOLVING?", 
         "Cyber criminals use social engineering and visual deception to fake emails. Instead of breaking passwords through software bugs, they trick users into willingly handing over bank passwords, OTPs, and credit cards.",
         C_RED, Inches(0.8)),
        ("WHO FACES THIS PROBLEM?", 
         "1. College Students: Targeted with fake scholarship grants, exam fee notices, and student loan baits.\n2. Non-Technical Users: Unable to notice lookalike spellings like 'paypa1.com'.\n3. Educational Labs: Lack enterprise cybersecurity firewalls.",
         C_CYAN, Inches(4.8)),
        ("WHY DOES IT MATTER?", 
         "• Financial Loss: Bank accounts drained within minutes.\n• Credential Theft: University portal & email hijack.\n• Need for Awareness: A transparent, beginner-friendly tool teaches students how phishing works internally.",
         C_GREEN, Inches(8.8)),
    ]

    for title, desc, col, x in cards3:
        box = slide3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, Inches(1.5), Inches(3.7), Inches(5.2))
        box.fill.solid()
        box.fill.fore_color.rgb = C_CARD_DARK
        box.line.color.rgb = col
        box.line.width = Pt(1.5)

        tb = slide3.shapes.add_textbox(x + Inches(0.15), Inches(1.7), Inches(3.4), Inches(4.8))
        tf = tb.text_frame
        tf.word_wrap = True

        p = tf.paragraphs[0]
        p.text = title
        p.font.size = Pt(12)
        p.font.bold = True
        p.font.color.rgb = col
        p.space_after = Pt(12)

        for line in desc.split("\n"):
            p2 = tf.add_paragraph()
            p2.text = line
            p2.font.size = Pt(10)
            p2.font.color.rgb = C_WHITE
            p2.space_after = Pt(6)

    # =========================================================================
    # SLIDE 4: RELATED WORK / LITERATURE SURVEY (6 PAPERS)
    # =========================================================================
    slide4 = prs.slides.add_slide(blank_layout)
    add_header(slide4, "4. Related Work / Literature Survey (5 to 6 Papers Analyzed)")

    papers = [
        ("Paper 1: Bergholz et al. (2010)", "Model-Based NLP & Markov Chains", "High processing overhead; fails on short or image-only phishing emails."),
        ("Paper 2: Basnet et al. (2012)", "Machine Learning (SVM, Naive Bayes)", "Complex black-box models; vulnerable to adversarial evasion."),
        ("Paper 3: Sheng et al. (2009)", "URL Blacklists (PhishTank, Google)", "Cannot stop zero-hour (freshly created) domains (4-12 hr delay)."),
        ("Paper 4: Almomani et al. (2013)", "Email Filtering Survey (SPF/DKIM)", "Spoofed display names routinely bypass basic SPF/DKIM filters."),
        ("Paper 5: Fette et al. (2007) [BASE]", "PILFER Structural Feature Extractor", "High false positive rate on legitimate newsletters with many links."),
        ("Paper 6: Marchal et al. (2016)", "Lexical Brand Target Matching", "Requires heavy browser extensions and external database queries."),
    ]

    for idx, (p_title, p_tech, p_limit) in enumerate(papers):
        r = idx // 2
        c = idx % 2
        x = Inches(0.8 + c * 5.9)
        y = Inches(1.4 + r * 1.8)
        w = Inches(5.6)
        h = Inches(1.65)

        p_box = slide4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, y, w, h)
        p_box.fill.solid()
        p_box.fill.fore_color.rgb = C_CARD_DARK
        p_box.line.color.rgb = C_BLUE if "BASE" in p_title else RGBColor(51, 65, 85)
        p_box.line.width = Pt(1.5)

        tb = slide4.shapes.add_textbox(x + Inches(0.15), y + Inches(0.1), w - Inches(0.3), h - Inches(0.2))
        tf = tb.text_frame
        tf.word_wrap = True

        p = tf.paragraphs[0]
        p.text = p_title
        p.font.size = Pt(10.5)
        p.font.bold = True
        p.font.color.rgb = C_CYAN if "BASE" not in p_title else C_GREEN

        p2 = tf.add_paragraph()
        p2.text = f"• Solution: {p_tech}"
        p2.font.size = Pt(9.5)
        p2.font.color.rgb = C_WHITE

        p3 = tf.add_paragraph()
        p3.text = f"• Limitation: {p_limit}"
        p3.font.size = Pt(9.5)
        p3.font.color.rgb = RGBColor(252, 165, 165)

    # =========================================================================
    # SLIDE 5: VISUAL EXAMPLE - FAKE EMAIL ANATOMY
    # =========================================================================
    slide5 = prs.slides.add_slide(blank_layout)
    add_header(slide5, "Visual Anatomy of a Phishing Email (What Our Code Inspects)")

    img_break = "docs/images/email_breakdown.png"
    if os.path.exists(img_break):
        slide5.shapes.add_picture(img_break, Inches(0.8), Inches(1.5), Inches(7.5), Inches(4.3))

    # Right side explanations
    side_box = slide5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(8.6), Inches(1.5), Inches(3.9), Inches(5.2))
    side_box.fill.solid()
    side_box.fill.fore_color.rgb = C_CARD_DARK
    side_box.line.color.rgb = C_CYAN
    side_box.line.width = Pt(1.5)

    stb = slide5.shapes.add_textbox(Inches(8.8), Inches(1.7), Inches(3.5), Inches(4.8))
    stf = stb.text_frame
    stf.word_wrap = True

    p = stf.paragraphs[0]
    p.text = "THE 4 CORE CHECKS:"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = C_CYAN
    p.space_after = Pt(10)

    rules_explain = [
        ("Check 1: Lookalike Sender", "paypa1.com replaces letter 'l' with digit '1'. Our code flags this immediately (+35 pts)."),
        ("Check 2: Panic Words", "'URGENT' or 'Account Suspended' forces hasty actions (+25 pts)."),
        ("Check 3: Raw IP Link", "Links like '192.168.1.50' instead of real domains are major red flags (+25 pts)."),
        ("Check 4: Data Demand", "Asking for Passwords, Credit Cards, or OTPs is a guaranteed scam (+30 pts).")
    ]

    for title, desc in rules_explain:
        p = stf.add_paragraph()
        p.text = f"• {title}:"
        p.font.size = Pt(10)
        p.font.bold = True
        p.font.color.rgb = C_WHITE
        p2 = stf.add_paragraph()
        p2.text = desc
        p2.font.size = Pt(9)
        p2.font.color.rgb = C_GRAY
        p2.space_after = Pt(6)

    # Meter at bottom
    img_meter = "docs/images/score_meter.png"
    if os.path.exists(img_meter):
        slide5.shapes.add_picture(img_meter, Inches(0.8), Inches(5.9), Inches(7.5), Inches(1.1))

    # =========================================================================
    # SLIDE 6: PROPOSED WORK (BASE PAPER & BEGINNER C CODE)
    # =========================================================================
    slide6 = prs.slides.add_slide(blank_layout)
    add_header(slide6, "5. Proposed Work (Base Paper & C Implementation)")

    # Left box: Base paper & logic
    lp_box = slide6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.4), Inches(5.5), Inches(5.3))
    lp_box.fill.solid()
    lp_box.fill.fore_color.rgb = C_CARD_DARK
    lp_box.line.color.rgb = C_BLUE
    lp_box.line.width = Pt(1.5)

    tb_lp = slide6.shapes.add_textbox(Inches(1.0), Inches(1.6), Inches(5.1), Inches(4.9))
    tf_lp = tb_lp.text_frame
    tf_lp.word_wrap = True

    p = tf_lp.paragraphs[0]
    p.text = "BASE PAPER IDENTIFICATION:"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = C_CYAN
    p.space_after = Pt(4)

    p2 = tf_lp.add_paragraph()
    p2.text = "Fette et al. (2007) - 'Learning to Detect Phishing Emails' (PILFER)\nIEEE / ACM Conference on World Wide Web."
    p2.font.size = Pt(10.5)
    p2.font.bold = True
    p2.font.color.rgb = C_WHITE
    p2.space_after = Pt(8)

    p3 = tf_lp.add_paragraph()
    p3.text = "HOW WE ADAPTED IT FOR 1ST YEAR STUDENTS:"
    p3.font.size = Pt(11)
    p3.font.bold = True
    p3.font.color.rgb = C_CYAN
    p3.space_after = Pt(4)

    bullet_pts = [
        "1. Converted heavy ML features into 4 direct, explainable if-else checks.",
        "2. Uses standard C library functions: stdio.h, string.h (strstr), ctype.h (tolower).",
        "3. Zero external dependencies - runs on any C compiler (GCC, Clang, VS Code).",
        "4. Transparent Threat Score (0 to 100) with clear Safe / Danger recommendations."
    ]
    for b in bullet_pts:
        pb = tf_lp.add_paragraph()
        pb.text = b
        pb.font.size = Pt(9.5)
        pb.font.color.rgb = C_GRAY
        pb.space_after = Pt(4)

    # Right box: Code Snippet
    rp_box = slide6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.6), Inches(1.4), Inches(5.9), Inches(5.3))
    rp_box.fill.solid()
    rp_box.fill.fore_color.rgb = RGBColor(10, 15, 30)
    rp_box.line.color.rgb = RGBColor(56, 189, 248)
    rp_box.line.width = Pt(1)

    code_block = (
        "// simple_phishguard.c (Student C Code)\n"
        "#include <stdio.h>\n"
        "#include <string.h>\n\n"
        "int main() {\n"
        "    char sender[100], subject[150], body[500];\n"
        "    int score = 0;\n\n"
        "    // 1. Take User Input\n"
        "    printf(\"Enter Sender: \");\n"
        "    fgets(sender, sizeof(sender), stdin);\n\n"
        "    // 2. CHECK 1: Fake Sender (paypa1, .xyz)\n"
        "    if (strstr(sender, \"paypa1\") != NULL) score += 35;\n\n"
        "    // 3. CHECK 2: Urgent Subject (urgent, blocked)\n"
        "    if (strstr(subject, \"urgent\") != NULL) score += 25;\n\n"
        "    // 4. CHECK 3: Raw IP Link (http://192.)\n"
        "    if (strstr(body, \"http://192.\") != NULL) score += 25;\n\n"
        "    // 5. CHECK 4: Credential Demand (password, card)\n"
        "    if (strstr(body, \"password\") != NULL) score += 30;\n\n"
        "    // 6. Final Result\n"
        "    if (score >= 50) printf(\"CRITICAL PHISHING!\");\n"
        "    else printf(\"SAFE EMAIL\");\n"
        "    return 0;\n"
        "}"
    )

    tb_code = slide6.shapes.add_textbox(Inches(6.75), Inches(1.5), Inches(5.6), Inches(5.1))
    tf_c = tb_code.text_frame
    tf_c.word_wrap = True
    for idx, line in enumerate(code_block.split("\n")):
        p = tf_c.paragraphs[0] if idx == 0 else tf_c.add_paragraph()
        p.text = line
        p.font.size = Pt(8.5)
        p.font.name = "Consolas"
        p.font.color.rgb = C_CYAN if line.startswith("//") else C_WHITE

    # =========================================================================
    # SLIDE 7: REFERENCES
    # =========================================================================
    slide7 = prs.slides.add_slide(blank_layout)
    add_header(slide7, "6. References (Academic Papers & Standards)")

    c_ref = slide7.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.4), Inches(11.733), Inches(5.3))
    c_ref.fill.solid()
    c_ref.fill.fore_color.rgb = C_CARD_DARK
    c_ref.line.color.rgb = C_BLUE
    c_ref.line.width = Pt(1.5)

    tb_ref = slide7.shapes.add_textbox(Inches(1.1), Inches(1.6), Inches(11.1), Inches(4.9))
    tf_ref = tb_ref.text_frame
    tf_ref.word_wrap = True

    references = [
        ("[1] BASE PAPER: I. Fette, N. Sadeh, and A. Tomasic",
         "\"Learning to Detect Phishing Emails,\" Proceedings of the 16th International World Wide Web Conference (WWW '07), Banff, Alberta, Canada, pp. 649-656, 2007."),
        ("[2] S. Marchal, J. Francois, R. State, and T. Engel",
         "\"Know Your Phish: Novel Content-Based Phishing Detection of Crafty Phishing Webpages,\" IEEE Transactions on Computers, vol. 65, no. 8, pp. 2401-2414, 2016."),
        ("[3] A. Almomani, B. B. Gupta, S. Atawneh, A. Meulenberg, and E. Almomani",
         "\"A Survey of Phishing Email Filtering Techniques,\" IEEE Communications Surveys & Tutorials, vol. 15, no. 4, pp. 2070-2090, 2013."),
        ("[4] R. Basnet, S. Mukkamala, and A. H. Sung",
         "\"Detection of Phishing Attacks: A Machine Learning Approach,\" Studies in Fuzziness and Soft Computing, Springer Berlin Heidelberg, pp. 373-383, 2012."),
        ("[5] S. Sheng, B. Wardman, G. Warner, L. Cranor, J. Hong, and C. Zhang",
         "\"An Empirical Analysis of Phishing Blacklists,\" 6th Conference on Email and Anti-Spam (CEAS '09), Mountain View, CA, 2009."),
        ("[6] E. Bergholz, J. Chang-Paauwe, F. Coatrieux, et al.",
         "\"Improved Phishing Detection using Model-Based Features and Classifiers,\" Cyberpsychology & Behavior, vol. 13, no. 2, pp. 135-142, 2010."),
        ("[7] C Programming Documentation",
         "ISO/IEC 9899:1999 (C99 Standard Specification), ANSI C Standard Library (stdio.h, string.h, ctype.h).")
    ]

    for title, cit in references:
        p = tf_ref.add_paragraph() if tf_ref.paragraphs[0].text else tf_ref.paragraphs[0]
        p.text = title
        p.font.size = Pt(10)
        p.font.bold = True
        p.font.color.rgb = C_CYAN if "BASE PAPER" in title else C_WHITE
        
        p2 = tf_ref.add_paragraph()
        p2.text = cit
        p2.font.size = Pt(9)
        p2.font.color.rgb = C_GRAY
        p2.space_after = Pt(5)

    # Save Presentation
    out_ppt = "E:\\project in c\\docs\\PhishGuard_Seminar_Presentation.pptx"
    prs.save(out_ppt)
    print(f"[+] Attractive PPT successfully created at: {out_ppt}")

if __name__ == '__main__':
    create_seminar_presentation()
