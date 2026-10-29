#include <stdio.h>
#include <string.h>
#include <ctype.h>
#include <stdbool.h>

// Convert string to lowercase for easy matching
void make_lowercase(char str[]) {
    for (int i = 0; str[i] != '\0'; i++) {
        str[i] = (char)tolower((unsigned char)str[i]);
    }
}

// Function to generate a clean HTML Security & Quarantine Report
void generate_html_report(const char *sender, const char *subject, const char *body,
                          int score, bool fake_sender, bool urgent_subj, 
                          bool dangerous_link, bool asking_data) {
    FILE *fp = fopen("quarantine_report.html", "w");
    if (!fp) {
        printf("[-] Error creating quarantine_report.html\n");
        return;
    }

    const char *badge_color = (score >= 50) ? "#ef4444" : (score >= 20) ? "#f59e0b" : "#10b981";
    const char *verdict_text = (score >= 50) ? "CRITICAL PHISHING THREAT" : 
                              (score >= 20) ? "SUSPICIOUS EMAIL" : "SAFE / CLEAN EMAIL";

    fprintf(fp, "<!DOCTYPE html>\n<html lang=\"en\">\n<head>\n");
    fprintf(fp, "<meta charset=\"UTF-8\">\n<title>PhishGuard Security Report</title>\n");
    fprintf(fp, "<style>\n");
    fprintf(fp, "body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background: #090d16; color: #f8fafc; padding: 30px; margin: 0; }\n");
    fprintf(fp, ".card { max-width: 800px; margin: 0 auto; background: #0f172a; border-radius: 12px; border: 1px solid #334155; padding: 28px; box-shadow: 0 10px 30px rgba(0,0,0,0.6); }\n");
    fprintf(fp, ".header { display: flex; justify-content: space-between; align-items: center; border-bottom: 2px solid #2563eb; padding-bottom: 16px; margin-bottom: 20px; }\n");
    fprintf(fp, ".title { font-size: 22px; font-weight: bold; color: #38bdf8; }\n");
    fprintf(fp, ".badge { background: %s; color: white; padding: 6px 14px; border-radius: 9999px; font-weight: bold; font-size: 13px; }\n", badge_color);
    fprintf(fp, ".info-box { background: #1e293b; padding: 16px; border-radius: 8px; margin-bottom: 20px; font-size: 13.5px; line-height: 1.6; }\n");
    fprintf(fp, "table { width: 100%%; border-collapse: collapse; margin-top: 14px; font-size: 13px; }\n");
    fprintf(fp, "th { background: #1e293b; color: #38bdf8; text-align: left; padding: 10px; border-bottom: 2px solid #334155; }\n");
    fprintf(fp, "td { padding: 10px; border-bottom: 1px solid #334155; }\n");
    fprintf(fp, ".danger-tag { color: #f87171; font-weight: bold; }\n");
    fprintf(fp, ".safe-tag { color: #4ade80; font-weight: bold; }\n");
    fprintf(fp, ".advice { margin-top: 24px; padding: 16px; background: #1e1b4b; border-left: 4px solid #6366f1; border-radius: 6px; font-size: 13.5px; }\n");
    fprintf(fp, "</style>\n</head>\n<body>\n");

    fprintf(fp, "<div class=\"card\">\n");
    fprintf(fp, "  <div class=\"header\">\n");
    fprintf(fp, "    <div><div class=\"title\">🛡️ PhishGuard Email Security Triage</div><small style=\"color:#94a3b8;\">Team: APEX CIPHER (1st Year CSE)</small></div>\n");
    fprintf(fp, "    <div class=\"badge\">%s (Score: %d/100)</div>\n", verdict_text, score);
    fprintf(fp, "  </div>\n");

    fprintf(fp, "  <div class=\"info-box\">\n");
    fprintf(fp, "    <div><strong>Sender:</strong> %s</div>\n", sender);
    fprintf(fp, "    <div><strong>Subject:</strong> %s</div>\n", subject);
    fprintf(fp, "    <div><strong>Message Excerpt:</strong> %s</div>\n", body);
    fprintf(fp, "  </div>\n");

    fprintf(fp, "  <h3>Detection Rules Evaluated by C Code</h3>\n");
    fprintf(fp, "  <table>\n");
    fprintf(fp, "    <tr><th>Security Check</th><th>Points Added</th><th>Status</th></tr>\n");
    
    fprintf(fp, "    <tr><td>Check 1: Lookalike / Fake Sender Domain (paypa1, .xyz)</td><td>+35 pts</td><td>%s</td></tr>\n",
            fake_sender ? "<span class=\"danger-tag\">TRIGGERED [DANGER]</span>" : "<span class=\"safe-tag\">PASSED [CLEAN]</span>");

    fprintf(fp, "    <tr><td>Check 2: Urgent / Panic Words in Subject (urgent, suspended)</td><td>+25 pts</td><td>%s</td></tr>\n",
            urgent_subj ? "<span class=\"danger-tag\">TRIGGERED [DANGER]</span>" : "<span class=\"safe-tag\">PASSED [CLEAN]</span>");

    fprintf(fp, "    <tr><td>Check 3: Dangerous Raw IP Link (http://192.168.x.x)</td><td>+25 pts</td><td>%s</td></tr>\n",
            dangerous_link ? "<span class=\"danger-tag\">TRIGGERED [DANGER]</span>" : "<span class=\"safe-tag\">PASSED [CLEAN]</span>");

    fprintf(fp, "    <tr><td>Check 4: Requesting Passwords, OTPs, or Credit Cards</td><td>+30 pts</td><td>%s</td></tr>\n",
            asking_data ? "<span class=\"danger-tag\">TRIGGERED [DANGER]</span>" : "<span class=\"safe-tag\">PASSED [CLEAN]</span>");

    fprintf(fp, "  </table>\n");

    fprintf(fp, "  <div class=\"advice\">\n");
    if (score >= 50) {
        fprintf(fp, "    <strong>Action Required:</strong> Immediate Quarantine. Do NOT click any links, open attachments, or reply to sender. Report to Cyber Security SOC.\n");
    } else if (score >= 20) {
        fprintf(fp, "    <strong>Action Required:</strong> Suspicious email. Contact sender through an official phone number or out-of-band channel before clicking.\n");
    } else {
        fprintf(fp, "    <strong>Action Required:</strong> Email looks authentic and safe. Standard security precautions apply.\n");
    }
    fprintf(fp, "  </div>\n");

    fprintf(fp, "</div>\n</body>\n</html>\n");
    fclose(fp);
    printf("[+] Successfully generated quarantine_report.html!\n");
}

int main() {
    char sender[150];
    char subject[200];
    char body[1000];

    char lower_sender[150];
    char lower_subject[200];
    char lower_body[1000];

    int score = 0;
    bool fake_sender = false;
    bool urgent_subj = false;
    bool dangerous_link = false;
    bool asking_data = false;

    printf("====================================================\n");
    printf("   PhishGuard: Simple Fake Email Detector (C Lang)  \n");
    printf("   Created by Student Team: APEX CIPHER             \n");
    printf("====================================================\n\n");

    // 1. Get email details from user
    printf("Enter Sender Email (e.g. support@paypa1.com): ");
    if (!fgets(sender, sizeof(sender), stdin)) return 1;
    sender[strcspn(sender, "\r\n")] = 0;

    printf("Enter Email Subject: ");
    if (!fgets(subject, sizeof(subject), stdin)) return 1;
    subject[strcspn(subject, "\r\n")] = 0;

    printf("Enter Email Body: ");
    if (!fgets(body, sizeof(body), stdin)) return 1;
    body[strcspn(body, "\r\n")] = 0;

    // Copy to lowercase buffers
    strcpy(lower_sender, sender);
    strcpy(lower_subject, subject);
    strcpy(lower_body, body);

    make_lowercase(lower_sender);
    make_lowercase(lower_subject);
    make_lowercase(lower_body);

    printf("\n--- Scanning Email Security Indicators in C ---\n");

    // CHECK 1: Fake / Lookalike Domain
    if (strstr(lower_sender, "paypa1") != NULL || strstr(lower_sender, "micr0soft") != NULL || 
        strstr(lower_sender, "g00gle") != NULL || strstr(lower_sender, ".xyz") != NULL || 
        strstr(lower_sender, ".top") != NULL) {
        printf("[!] WARNING: Suspicious/Fake sender address found! (+35 points)\n");
        score += 35;
        fake_sender = true;
    }

    // CHECK 2: Urgent words in Subject
    if (strstr(lower_subject, "urgent") != NULL || strstr(lower_subject, "suspended") != NULL || 
        strstr(lower_subject, "blocked") != NULL || strstr(lower_subject, "action required") != NULL) {
        printf("[!] WARNING: Panic/Urgent subject detected! (+25 points)\n");
        score += 25;
        urgent_subj = true;
    }

    // CHECK 3: Fake links or raw IP addresses
    if (strstr(lower_body, "http://192.") != NULL || strstr(lower_body, "http://10.") != NULL || 
        strstr(lower_body, "click here") != NULL || strstr(lower_body, "login-verify") != NULL) {
        printf("[!] WARNING: Dangerous or unsecure web link detected! (+25 points)\n");
        score += 25;
        dangerous_link = true;
    }

    // CHECK 4: Asking for secret personal details
    if (strstr(lower_body, "password") != NULL || strstr(lower_body, "credit card") != NULL || 
        strstr(lower_body, "otp") != NULL || strstr(lower_body, "bank account") != NULL) {
        printf("[!] WARNING: Asking for sensitive personal/banking data! (+30 points)\n");
        score += 30;
        asking_data = true;
    }

    if (score > 100) score = 100;

    // Terminal summary
    printf("\n====================================================\n");
    printf("Total Threat Score: %d / 100\n", score);
    if (score >= 50) {
        printf("FINAL VERDICT: [DANGEROUS PHISHING EMAIL!]\n");
        printf("ADVICE       : Do NOT click links or reply! Delete or report it.\n");
    } else if (score >= 20) {
        printf("FINAL VERDICT: [SUSPICIOUS EMAIL]\n");
        printf("ADVICE       : Be careful! Verify sender before opening.\n");
    } else {
        printf("FINAL VERDICT: [SAFE EMAIL]\n");
        printf("ADVICE       : No major phishing signs found. Looks clean.\n");
    }
    printf("====================================================\n");

    // Generate HTML report directly from C code
    generate_html_report(sender, subject, body, score, fake_sender, urgent_subj, dangerous_link, asking_data);

    return 0;
}
