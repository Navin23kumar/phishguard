#include "phishguard.h"

/* Terminal ANSI Colors */
#define ANSI_RED     "\x1b[1;31m"
#define ANSI_GREEN   "\x1b[1;32m"
#define ANSI_YELLOW  "\x1b[1;33m"
#define ANSI_CYAN    "\x1b[1;36m"
#define ANSI_WHITE   "\x1b[1;37m"
#define ANSI_RESET   "\x1b[0m"

static const char *get_risk_str(RiskLevel level) {
    switch (level) {
        case RISK_SAFE: return "LEGITIMATE / SAFE";
        case RISK_SUSPICIOUS: return "SUSPICIOUS";
        case RISK_CRITICAL_PHISHING: return "CRITICAL PHISHING THREAT";
        default: return "UNKNOWN";
    }
}

static const char *get_risk_color(RiskLevel level) {
    switch (level) {
        case RISK_SAFE: return ANSI_GREEN;
        case RISK_SUSPICIOUS: return ANSI_YELLOW;
        case RISK_CRITICAL_PHISHING: return ANSI_RED;
        default: return ANSI_WHITE;
    }
}

void print_terminal_report(const EmailMessage *msg, const PhishReport *report) {
    printf("\n%s========================================================================%s\n", ANSI_CYAN, ANSI_RESET);
    printf("%s   [PhishGuard AI-Shield] Phishing Email Analysis Report%s\n", ANSI_WHITE, ANSI_RESET);
    printf("%s========================================================================%s\n", ANSI_CYAN, ANSI_RESET);
    
    printf("%-18s: %s\n", "Sender (From)", msg->from[0] ? msg->from : "N/A");
    printf("%-18s: %s\n", "Reply-To", msg->reply_to[0] ? msg->reply_to : "None (Matches From)");
    printf("%-18s: %s\n", "Subject", msg->subject[0] ? msg->subject : "N/A");
    printf("%-18s: %s\n", "Detected Domain", msg->sender_domain[0] ? msg->sender_domain : "N/A");
    printf("%-18s: SPF=%s | DKIM=%s | DMARC=%s\n", "Email Auth",
           msg->spf_result[0] ? msg->spf_result : "None",
           msg->dkim_result[0] ? msg->dkim_result : "None",
           msg->dmarc_result[0] ? msg->dmarc_result : "None");
    printf("%-18s: %d extracted\n", "Embedded URLs", msg->url_count);

    if (msg->url_count > 0) {
        printf("------------------------------------------------------------------------\n");
        printf("Extracted Links for Inspection:\n");
        for (int i = 0; i < msg->url_count; i++) {
            printf("  [%d] %s\n", i + 1, msg->urls[i]);
        }
    }

    printf("------------------------------------------------------------------------\n");
    printf("Risk Evaluation Breakdown:\n");
    if (report->trigger_count == 0) {
        printf("  %s* No suspicious indicators triggered.%s\n", ANSI_GREEN, ANSI_RESET);
    } else {
        for (int i = 0; i < report->trigger_count; i++) {
            const RuleTrigger *t = &report->triggers[i];
            printf("  %s[%-16s]%s +%-2d pts | %-40s (Evid: %s)\n",
                   ANSI_YELLOW, t->rule_id, ANSI_RESET, t->score_impact, t->description, t->evidence);
        }
    }

    printf("------------------------------------------------------------------------\n");
    printf("FINAL THREAT SCORE : %s%d / 100%s\n", get_risk_color(report->risk_level), report->total_score, ANSI_RESET);
    printf("VERDICT            : %s[%s]%s\n", get_risk_color(report->risk_level), get_risk_str(report->risk_level), ANSI_RESET);
    printf("RECOMMENDATION     : %s\n", report->recommendation);
    printf("%s========================================================================%s\n\n", ANSI_CYAN, ANSI_RESET);
}

void export_json_report(const char *out_filepath, const EmailMessage *msg, const PhishReport *report) {
    FILE *fp = fopen(out_filepath, "w");
    if (!fp) return;

    fprintf(fp, "{\n");
    fprintf(fp, "  \"sender\": \"%s\",\n", msg->from);
    fprintf(fp, "  \"reply_to\": \"%s\",\n", msg->reply_to);
    fprintf(fp, "  \"subject\": \"%s\",\n", msg->subject);
    fprintf(fp, "  \"sender_domain\": \"%s\",\n", msg->sender_domain);
    fprintf(fp, "  \"auth\": {\n");
    fprintf(fp, "    \"spf\": \"%s\",\n", msg->spf_result);
    fprintf(fp, "    \"dkim\": \"%s\",\n", msg->dkim_result);
    fprintf(fp, "    \"dmarc\": \"%s\"\n", msg->dmarc_result);
    fprintf(fp, "  },\n");
    fprintf(fp, "  \"phishing_score\": %d,\n", report->total_score);
    fprintf(fp, "  \"risk_level\": \"%s\",\n", get_risk_str(report->risk_level));
    fprintf(fp, "  \"recommendation\": \"%s\",\n", report->recommendation);
    fprintf(fp, "  \"triggers\": [\n");
    for (int i = 0; i < report->trigger_count; i++) {
        fprintf(fp, "    {\n");
        fprintf(fp, "      \"rule_id\": \"%s\",\n", report->triggers[i].rule_id);
        fprintf(fp, "      \"score\": %d,\n", report->triggers[i].score_impact);
        fprintf(fp, "      \"desc\": \"%s\",\n", report->triggers[i].description);
        fprintf(fp, "      \"evidence\": \"%s\"\n", report->triggers[i].evidence);
        fprintf(fp, "    }%s\n", (i == report->trigger_count - 1) ? "" : ",");
    }
    fprintf(fp, "  ],\n");
    fprintf(fp, "  \"extracted_urls\": [\n");
    for (int i = 0; i < msg->url_count; i++) {
        fprintf(fp, "    \"%s\"%s\n", msg->urls[i], (i == msg->url_count - 1) ? "" : ",");
    }
    fprintf(fp, "  ]\n");
    fprintf(fp, "}\n");

    fclose(fp);
}

void export_html_quarantine(const char *out_filepath, const EmailMessage *msg, const PhishReport *report) {
    FILE *fp = fopen(out_filepath, "w");
    if (!fp) return;

    const char *badge_color = (report->risk_level == RISK_CRITICAL_PHISHING) ? "#dc2626" :
                              (report->risk_level == RISK_SUSPICIOUS) ? "#d97706" : "#16a34a";

    fprintf(fp, "<!DOCTYPE html>\n<html lang=\"en\">\n<head>\n");
    fprintf(fp, "<meta charset=\"UTF-8\">\n<title>PhishGuard Quarantine & Triage Report</title>\n");
    fprintf(fp, "<style>\n");
    fprintf(fp, "body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background: #0f172a; color: #f8fafc; margin: 0; padding: 24px; }\n");
    fprintf(fp, ".card { background: #1e293b; border-radius: 12px; max-width: 900px; margin: 0 auto; box-shadow: 0 10px 25px rgba(0,0,0,0.5); border: 1px solid #334155; overflow: hidden; }\n");
    fprintf(fp, ".header { background: #090d16; padding: 20px 28px; border-bottom: 2px solid #38bdf8; display: flex; justify-content: space-between; align-items: center; }\n");
    fprintf(fp, ".title { font-size: 20px; font-weight: bold; color: #38bdf8; letter-spacing: 0.5px; }\n");
    fprintf(fp, ".badge { background: %s; color: white; padding: 6px 14px; border-radius: 9999px; font-weight: bold; font-size: 14px; }\n", badge_color);
    fprintf(fp, ".content { padding: 28px; }\n");
    fprintf(fp, ".meta-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 16px; margin-bottom: 24px; background: #151e2e; padding: 18px; border-radius: 8px; font-size: 14px; }\n");
    fprintf(fp, ".meta-item strong { color: #94a3b8; }\n");
    fprintf(fp, ".score-box { background: #1e1b4b; border-left: 5px solid #6366f1; padding: 16px; border-radius: 6px; margin-bottom: 24px; }\n");
    fprintf(fp, "table { width: 100%%; border-collapse: collapse; margin-top: 12px; font-size: 14px; }\n");
    fprintf(fp, "th { background: #334155; color: #f1f5f9; text-align: left; padding: 10px; }\n");
    fprintf(fp, "td { padding: 10px; border-bottom: 1px solid #334155; }\n");
    fprintf(fp, ".recommendation { background: #27272a; border-left: 4px solid %s; padding: 14px; border-radius: 6px; font-weight: 500; margin-top: 20px; }\n", badge_color);
    fprintf(fp, "</style>\n</head>\n<body>\n");
    
    fprintf(fp, "<div class=\"card\">\n");
    fprintf(fp, "  <div class=\"header\"><div class=\"title\">🛡️ PhishGuard Security Analyzer</div><div class=\"badge\">%s (Score: %d/100)</div></div>\n",
            get_risk_str(report->risk_level), report->total_score);
    
    fprintf(fp, "  <div class=\"content\">\n");
    fprintf(fp, "    <div class=\"meta-grid\">\n");
    fprintf(fp, "      <div class=\"meta-item\"><strong>From:</strong> %s</div>\n", msg->from);
    fprintf(fp, "      <div class=\"meta-item\"><strong>Reply-To:</strong> %s</div>\n", msg->reply_to[0] ? msg->reply_to : "(Identical to From)");
    fprintf(fp, "      <div class=\"meta-item\"><strong>Subject:</strong> %s</div>\n", msg->subject);
    fprintf(fp, "      <div class=\"meta-item\"><strong>Sender Domain:</strong> %s</div>\n", msg->sender_domain);
    fprintf(fp, "      <div class=\"meta-item\"><strong>SPF Status:</strong> %s</div>\n", msg->spf_result[0] ? msg->spf_result : "None");
    fprintf(fp, "      <div class=\"meta-item\"><strong>DKIM / DMARC:</strong> %s / %s</div>\n",
            msg->dkim_result[0] ? msg->dkim_result : "None", msg->dmarc_result[0] ? msg->dmarc_result : "None");
    fprintf(fp, "    </div>\n");

    fprintf(fp, "    <h3>Triggered Threat Indicators (%d)</h3>\n", report->trigger_count);
    fprintf(fp, "    <table>\n<tr><th>Rule ID</th><th>Points</th><th>Threat Description</th><th>Evidence Snippet</th></tr>\n");
    for (int i = 0; i < report->trigger_count; i++) {
        fprintf(fp, "<tr><td><code>%s</code></td><td>+%d</td><td>%s</td><td><code>%s</code></td></tr>\n",
                report->triggers[i].rule_id, report->triggers[i].score_impact,
                report->triggers[i].description, report->triggers[i].evidence);
    }
    fprintf(fp, "    </table>\n");

    if (msg->url_count > 0) {
        fprintf(fp, "    <h3 style=\"margin-top:24px;\">Sanitized URLs Inspected (%d)</h3>\n<ul>\n", msg->url_count);
        for (int i = 0; i < msg->url_count; i++) {
            fprintf(fp, "<li><code>%s</code></li>\n", msg->urls[i]);
        }
        fprintf(fp, "</ul>\n");
    }

    fprintf(fp, "    <div class=\"recommendation\"><strong>Security Action Required:</strong> %s</div>\n", report->recommendation);
    fprintf(fp, "  </div>\n</div>\n");
    fprintf(fp, "</body>\n</html>\n");

    fclose(fp);
}
