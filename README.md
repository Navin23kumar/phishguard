# PhishGuard: Phishing Email Detection & Threat Triage Engine
**Author / Security Team:** APEX CIPHER (1st Year CSE)  
**Domain:** Cyber Security | Fake Email Detection & Threat Triage  
**Technologies Used:** Pure C Language (C99 Standard) & HTML/CSS/JavaScript  
**Zero Python:** This project is built 100% using native C and modern HTML.

---

## 📌 Project Overview
PhishGuard is a beginner-friendly cybersecurity tool developed by 1st-year computer science students (**APEX CIPHER**). It identifies fraudulent phishing emails using 4 rule-based security checks:
1. **Lookalike / Fake Sender Domains (Typosquatting):** Detects visually altered domains (e.g. `paypa1.com` instead of `paypal.com`, `.xyz` domains).
2. **Artificial Psychological Urgency:** Flags panic keywords in subject lines (`urgent`, `suspended`, `action required`).
3. **Deceptive & Raw IP Hyperlinks:** Detects links using raw numerical IP addresses (e.g. `http://192.168.1.50/login`) instead of authentic domain names.
4. **Confidential Credential Harvesting:** Flags unauthorized demands for sensitive data (`password`, `credit card`, `OTP`).

---

## 📁 Repository Structure (100% C & HTML)
```
├── simple_phishguard.c      # Clean, beginner-friendly C detector (takes input & outputs HTML)
├── src/                     # Advanced multi-file C triage engine
│   ├── main.c               # CLI router & argument dispatcher
│   ├── phish_engine.c       # Heuristic scoring engine in C
│   ├── email_parser.c       # RFC-822 header & link stream parser
│   ├── reporter.c           # Terminal & HTML report generator
│   └── utils.c              # Levenshtein distance & domain extraction
├── include/
│   └── phishguard.h         # C header structures & function prototypes
├── samples/                 # Email threat test files (.eml format)
│   ├── phishing_paypal.eml
│   ├── phishing_office365.eml
│   └── legitimate_github.eml
├── index.html               # Web Browser Simulator (Runs detection live in any browser)
├── slides.html              # 7-Slide Technical Club Presentation for Chrome/Edge
├── docs/
│   └── presentation_slides.html
├── Makefile                 # GCC build script
├── run.bat                  # Windows batch runner
└── README.md
```

---

## ⚙️ How to Compile & Run (Pure C)

### 1. Compile with GCC
```bash
gcc simple_phishguard.c -o simple_phishguard.exe
```

### 2. Run the C Program
```bash
./simple_phishguard.exe
```
Enter sample email information when prompted. The C program will:
1. Display the threat analysis on your terminal.
2. Output a formatted **`quarantine_report.html`** file that you can view in any browser.

---

## 🌐 Running in the Browser (HTML Simulator)
Simply double-click **`index.html`** (or open `http://localhost:8080/index.html`).
- Click **⚠️ PayPal Phishing** or **⚠️ Office 365 Phishing** to see the C logic run interactively in the web browser.
- Open **`slides.html`** in your browser and press **F11** for a full-screen presentation slideshow for your seminar.
