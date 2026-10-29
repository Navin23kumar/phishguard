#include "phishguard.h"

/* High-profile brands frequently targeted by phishing */
static const char *TARGET_BRANDS[] = {
    "paypal", "google", "microsoft", "apple", "amazon", "netflix",
    "chase", "bankofamerica", "wellsfargo", "facebook", "instagram",
    "dropbox", "linkedin", "steam", "coinbase", "binance", "adobe"
};
static const int TARGET_BRANDS_COUNT = sizeof(TARGET_BRANDS) / sizeof(TARGET_BRANDS[0]);

/* Suspicious keywords in Subject line */
static const struct {
    const char *keyword;
    int weight;
    const char *desc;
} SUBJECT_RULES[] = {
    {"urgent", 15, "Urgent pressure tactic in subject"},
    {"immediate action", 20, "High-pressure immediate action call"},
    {"account suspended", 25, "Threat of account suspension"},
    {"unauthorized access", 25, "Security scare tactic"},
    {"verify your account", 20, "Account verification request"},
    {"password reset", 15, "Unsolicited password reset prompt"},
    {"wire transfer", 20, "Financial wire urgency"},
    {"invoice overdue", 15, "Financial demand tactic"},
    {"lottery winner", 30, "Classic lottery prize bait"}
};
static const int SUBJECT_RULES_COUNT = sizeof(SUBJECT_RULES) / sizeof(SUBJECT_RULES[0]);

/* Suspicious keywords in Body */
static const struct {
    const char *keyword;
    int weight;
    const char *desc;
} BODY_RULES[] = {
    {"kindly update", 10, "Social engineering formality"},
    {"click the link below", 15, "Call to click embedded link"},
    {"within 24 hours", 20, "Artificial deadline / urgency timer"},
    {"failure to do so will result", 25, "Threatening ultimatum"},
    {"dear customer", 10, "Generic impersonal salutation"},
    {"dear valued member", 10, "Impersonal corporate bait"},
    {"confirm your identity", 20, "Credential harvesting indicator"},
    {"security alert", 15, "Alarmist security notification"},
    {"social security number", 30, "PII harvesting request (SSN)"},
    {"credit card number", 30, "Payment card harvesting request"}
};
static const int BODY_RULES_COUNT = sizeof(BODY_RULES) / sizeof(BODY_RULES[0]);

/* Suspicious URL extensions and URL shorteners */
static const char *SUSPICIOUS_TLDS[] = {
    ".xyz", ".top", ".tk", ".ml", ".ga", ".cf", ".gq", ".work", ".click", ".buzz"
};
static const int SUSPICIOUS_TLDS_COUNT = sizeof(SUSPICIOUS_TLDS) / sizeof(SUSPICIOUS_TLDS[0]);

static const char *URL_SHORTENERS[] = {
    "bit.ly", "tinyurl.com", "t.co", "is.gd", "rb.gy", "cutt.ly"
};
static const int SHORTENERS_COUNT = sizeof(URL_SHORTENERS) / sizeof(URL_SHORTENERS[0]);

static void add_trigger(PhishReport *report, const char *rule_id, const char *desc, int score, const char *evidence) {
    if (report->trigger_count >= MAX_RULES_TRIGGERED) return;
    RuleTrigger *t = &report->triggers[report->trigger_count++];
    strncpy(t->rule_id, rule_id, sizeof(t->rule_id) - 1);
    strncpy(t->description, desc, sizeof(t->description) - 1);
    t->score_impact = score;
    strncpy(t->evidence, evidence, sizeof(t->evidence) - 1);
    report->total_score += score;
}

void analyze_email(const EmailMessage *msg, PhishReport *report) {
    memset(report, 0, sizeof(PhishReport));

    /* -------------------------------------------------------------
     * LAYER 1: Email Header & Authentication Analysis (SPF/DKIM/DMARC)
     * ------------------------------------------------------------- */
    if (strcasecmp(msg->spf_result, "FAIL") == 0) {
        add_trigger(report, "AUTH-SPF-FAIL", "Sender SPF verification failed (Forged sender IP)", 25, msg->sender_domain);
    }
    if (strcasecmp(msg->dkim_result, "FAIL") == 0) {
        add_trigger(report, "AUTH-DKIM-FAIL", "Cryptographic DKIM signature failed or invalid", 20, "DKIM=fail");
    }
    if (strcasecmp(msg->dmarc_result, "FAIL") == 0) {
        add_trigger(report, "AUTH-DMARC-FAIL", "DMARC policy alignment check failed", 30, "DMARC=fail");
    }

    // Check Sender Domain vs Reply-To Domain mismatch (Header Spoofing)
    if (strlen(msg->sender_domain) > 0 && strlen(msg->reply_to_domain) > 0) {
        if (strcasecmp(msg->sender_domain, msg->reply_to_domain) != 0) {
            char evid[256];
            snprintf(evid, sizeof(evid), "From: %s != Reply-To: %s", msg->sender_domain, msg->reply_to_domain);
            add_trigger(report, "HEADER-REPLYTO-MISMATCH", "Mismatch between 'From' domain and 'Reply-To' domain", 25, evid);
        }
    }

    // Check Display Name Spoofing (e.g. Display Name says "PayPal Support" but email is attacker@yahoo.com)
    char lower_disp[MAX_STRING_LEN];
    strncpy(lower_disp, msg->sender_display_name, sizeof(lower_disp));
    str_to_lower(lower_disp);

    for (int i = 0; i < TARGET_BRANDS_COUNT; i++) {
        if (strstr(lower_disp, TARGET_BRANDS[i]) != NULL) {
            if (strstr(msg->sender_domain, TARGET_BRANDS[i]) == NULL) {
                char evid[256];
                snprintf(evid, sizeof(evid), "Claims '%s' in Name but sent from '%s'", TARGET_BRANDS[i], msg->sender_domain);
                add_trigger(report, "SPOOF-BRAND-NAME", "Display name brand spoofing detected", 35, evid);
                break;
            }
        }
    }

    /* -------------------------------------------------------------
     * LAYER 2: Domain Typosquatting / Lookalike Check
     * ------------------------------------------------------------- */
    if (strlen(msg->sender_domain) > 0) {
        // Strip common TLD for comparison (e.g., paypal-security.com -> paypal-security)
        char s_root[MAX_STRING_LEN];
        strncpy(s_root, msg->sender_domain, sizeof(s_root));
        char *dot = strchr(s_root, '.');
        if (dot) *dot = '\0';

        for (int i = 0; i < TARGET_BRANDS_COUNT; i++) {
            // Check direct Levenshtein distance on base brand
            int dist = calculate_levenshtein(s_root, TARGET_BRANDS[i]);
            // If edit distance is 1 or 2, and length is similar, high chance of typosquatting (e.g. paypa1, micr0soft)
            if (dist > 0 && dist <= 2 && abs((int)strlen(s_root) - (int)strlen(TARGET_BRANDS[i])) <= 2) {
                char evid[256];
                snprintf(evid, sizeof(evid), "'%s' mimics legitimate '%s' (Edit Dist: %d)", msg->sender_domain, TARGET_BRANDS[i], dist);
                add_trigger(report, "DOMAIN-TYPOSQUAT", "Typosquatting / Lookalike domain detected", 35, evid);
                break;
            }
        }
    }

    /* -------------------------------------------------------------
     * LAYER 3: Subject Line Urgency & Scare Tactics
     * ------------------------------------------------------------- */
    char lower_subject[MAX_STRING_LEN];
    strncpy(lower_subject, msg->subject, sizeof(lower_subject));
    str_to_lower(lower_subject);

    for (int i = 0; i < SUBJECT_RULES_COUNT; i++) {
        if (strstr(lower_subject, SUBJECT_RULES[i].keyword) != NULL) {
            add_trigger(report, "SUBJ-URGENCY", SUBJECT_RULES[i].desc, SUBJECT_RULES[i].weight, SUBJECT_RULES[i].keyword);
        }
    }

    /* -------------------------------------------------------------
     * LAYER 4: Email Body Social Engineering Keywords
     * ------------------------------------------------------------- */
    char lower_body[MAX_EMAIL_BODY_LEN];
    strncpy(lower_body, msg->body, sizeof(lower_body) - 1);
    str_to_lower(lower_body);

    for (int i = 0; i < BODY_RULES_COUNT; i++) {
        if (strstr(lower_body, BODY_RULES[i].keyword) != NULL) {
            add_trigger(report, "BODY-KEYWORD", BODY_RULES[i].desc, BODY_RULES[i].weight, BODY_RULES[i].keyword);
        }
    }

    /* -------------------------------------------------------------
     * LAYER 5: Deep URL & Link Threat Inspection
     * ------------------------------------------------------------- */
    for (int u = 0; u < msg->url_count; u++) {
        const char *url = msg->urls[u];
        char u_domain[MAX_STRING_LEN];
        extract_domain(url, u_domain, sizeof(u_domain));

        // 1. IP Address Host detection (e.g. http://192.168.1.50/login)
        if (is_ip_address(u_domain)) {
            char evid[256];
            snprintf(evid, sizeof(evid), "Raw IP used in URL: %s", url);
            add_trigger(report, "URL-RAW-IP", "Raw numerical IP address instead of domain name", 30, evid);
        }

        // 2. Suspicious TLD detection
        for (int t = 0; t < SUSPICIOUS_TLDS_COUNT; t++) {
            size_t dlen = strlen(u_domain);
            size_t tlen = strlen(SUSPICIOUS_TLDS[t]);
            if (dlen >= tlen && strcasecmp(u_domain + dlen - tlen, SUSPICIOUS_TLDS[t]) == 0) {
                char evid[256];
                snprintf(evid, sizeof(evid), "TLD: %s in %s", SUSPICIOUS_TLDS[t], u_domain);
                add_trigger(report, "URL-RISKY-TLD", "Suspicious / Abused top-level domain", 20, evid);
                break;
            }
        }

        // 3. URL Shortener detection (obfuscating true destination)
        for (int s = 0; s < SHORTENERS_COUNT; s++) {
            if (strcasecmp(u_domain, URL_SHORTENERS[s]) == 0) {
                char evid[256];
                snprintf(evid, sizeof(evid), "Shortener: %s", url);
                add_trigger(report, "URL-SHORTENER", "URL shortener hiding true destination", 15, evid);
                break;
            }
        }

        // 4. Brand Target in Subdomain/Path but wrong main domain (e.g. paypal.com.attacker.xyz)
        for (int b = 0; b < TARGET_BRANDS_COUNT; b++) {
            if (strstr(u_domain, TARGET_BRANDS[b]) != NULL) {
                // Check if it's the official brand domain or a subdomain trap
                char legitimate[64];
                snprintf(legitimate, sizeof(legitimate), "%s.com", TARGET_BRANDS[b]);
                if (strcasecmp(u_domain, legitimate) != 0 && 
                    !strstr(u_domain, legitimate)) {
                    char evid[256];
                    snprintf(evid, sizeof(evid), "Host '%s' impersonates brand '%s'", u_domain, TARGET_BRANDS[b]);
                    add_trigger(report, "URL-BRAND-TRAP", "Deceptive domain impersonating legitimate brand", 30, evid);
                    break;
                }
            }
        }
    }

    /* -------------------------------------------------------------
     * LAYER 6: Final Risk Score Computation and Recommendation
     * ------------------------------------------------------------- */
    if (report->total_score > 100) {
        report->total_score = 100;
    }

    if (report->total_score >= 50) {
        report->risk_level = RISK_CRITICAL_PHISHING;
        snprintf(report->recommendation, sizeof(report->recommendation),
                 "[CRITICAL] High probability of phishing attack! Quarantine email immediately. "
                 "Do NOT click any links, open attachments, or reply to sender. Report to SOC / IT Security.");
    } else if (report->total_score >= 20) {
        report->risk_level = RISK_SUSPICIOUS;
        snprintf(report->recommendation, sizeof(report->recommendation),
                 "[WARNING] Suspicious elements identified. Verify the sender identity via an out-of-band channel "
                 "(e.g., official phone number) before taking any requested action.");
    } else {
        report->risk_level = RISK_SAFE;
        snprintf(report->recommendation, sizeof(report->recommendation),
                 "[CLEAN] No significant phishing indicators detected. Standard email security precautions apply.");
    }
}
