# PhishGuard: Phishing Email Detection & Threat Triage Engine
**Author / Security Team:** APEX CIPHER  
**Domain:** Cyber Security | Email Security & SOC Operations  
**Language:** Pure C (C99 Standard, Portable on Windows / Linux / macOS)  
**Target Audience:** College Technical Club, Hackathon, Cyber Defense Workshop  

---

## 📌 Executive Summary
Phishing remains the #1 initial access vector in 80%+ of cyber attacks and ransomware incidents. **PhishGuard** is an automated email threat triage engine written in pure C that inspects raw email files (`.eml`, `.txt`) or interactive inputs against multi-layered cyber security detection rules:
1. **Email Authentication Validation:** Verifies SPF, DKIM, and DMARC alignment status.
2. **Header & Display Name Spoofing Detection:** Identifies discrepancies between display names, `From` address, and `Reply-To` traps.
3. **Domain Typosquatting Analysis:** Uses the **Levenshtein Distance Algorithm** to flag lookalike domains targeting major brands (e.g., `paypa1-security.xyz`).
4. **URL & Link Threat Inspection:** Flags raw IP hosts (e.g. `http://192.168.1.100`), suspicious top-level domains (`.xyz`, `.top`, `.click`), URL shorteners, and deceptive brand subdomains.
5. **Natural Language / Social Engineering Indicators:** Parses urgent calls to action, fake deadlines, and credential harvesting triggers.
6. **Automated Prevention & Triage Output:** Generates terminal threat breakdowns, machine-readable JSON for SIEM ingestion, and an HTML Quarantine Warning Page.

---

## 📁 Project Architecture
```
project in c/
├── include/
│   └── phishguard.h        # Structs, risk definitions, and prototypes
├── src/
│   ├── main.c              # CLI argument parser and execution pipeline
│   ├── email_parser.c      # RFC-822 / 5322 header and body extractor
│   ├── phish_engine.c      # Multi-layer cybersecurity detection logic
│   ├── reporter.c          # Terminal UI, JSON SIEM export, HTML Quarantine
│   └── utils.c             # Levenshtein distance, domain extraction, IP validation
├── samples/
│   ├── phishing_paypal.eml      # Realistic PayPal credential harvesting sample
│   ├── phishing_office365.eml   # Corporate spear-phishing simulation
│   └── legitimate_github.eml    # Valid, authentic notification sample
├── Makefile                # GCC build script
└── README.md               # Complete documentation & technical presentation guide
```

---

## ⚙️ Compilation & Build

### Using GCC (MinGW / Windows / Linux)
```bash
gcc -Wall -Wextra -std=c99 -Iinclude -Dstrncasecmp=_strnicmp -Dstrcasecmp=_stricmp src/*.c -o phishguard.exe
```
*(On Linux/macOS, simply omit `-Dstrncasecmp=_strnicmp -Dstrcasecmp=_stricmp`)*

Or using Make:
```bash
make
```

---

## 🚀 Usage Guide

### 1. Analyze an Email File (.eml)
```bash
./phishguard samples/phishing_paypal.eml
```

### 2. Generate SIEM JSON & HTML Quarantine Warning
```bash
./phishguard samples/phishing_paypal.eml --json report.json --html quarantine.html
```

### 3. Interactive Triage Mode (Live demo in Technical Club)
```bash
./phishguard --interactive
```

---

## 🛡️ Detection Capabilities & Scoring Model

| Category | Detection Rule | Threat Score |
| :--- | :--- | :---: |
| **Authentication** | SPF Alignment Failure | +25 pts |
| **Authentication** | DKIM Signature Failure | +20 pts |
| **Authentication** | DMARC Policy Rejection | +30 pts |
| **Header Analysis** | From vs Reply-To Mismatch | +25 pts |
| **Header Analysis** | Display Name Brand Impersonation | +35 pts |
| **Domain Analysis** | Typosquatting (Levenshtein Dist $\le 2$) | +35 pts |
| **URL Inspection** | Numerical Raw IP Host in Link | +30 pts |
| **URL Inspection** | Suspicious / Abused TLD (`.xyz`, `.top`, etc.) | +20 pts |
| **URL Inspection** | URL Shortener Masking (`bit.ly`, `tinyurl`) | +15 pts |
| **Social Engineering**| Urgency, account lock threats, credential demand | +10 to +30 pts |

### Threat Verdict:
- **0 – 19 pts:** `SAFE / LEGITIMATE`
- **20 – 49 pts:** `SUSPICIOUS` (Requires manual verification)
- **50 – 100 pts:** `CRITICAL PHISHING THREAT` (Immediate Quarantine)

---

## 🎤 Presentation Pitch for Technical Club
1. **Problem Statement:** How cyber adversaries deceive users using modern spoofing and social engineering techniques.
2. **Technical Depth:** Demonstrating low-level string manipulation, RFC header parsing, and the dynamic programming Levenshtein algorithm in C.
3. **Defensive Pipeline:** Demonstrating how SOC (Security Operations Center) analysts triage suspicious emails and automate defense via SIEM JSON reports and browser quarantine pages.
