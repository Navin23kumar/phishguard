#include "phishguard.h"

static void print_banner(void) {
    printf("\n");
    printf("========================================================================\n");
    printf("   ____  _     _     _      ____                     _ \n");
    printf("  |  _ \\| |__ (_)___| |__  / ___|_   _  __ _ _ __ __| |\n");
    printf("  | |_) | '_ \\| / __| '_ \\| |  _| | | |/ _` | '__/ _` |\n");
    printf("  |  __/| | | | \\__ \\ | | | |_| | |_| | (_| | | | (_| |\n");
    printf("  |_|   |_| |_|_|___/_| |_|\\____|\\__,_|\\__,_|_|  \\__,_|\n");
    printf("   Email Security & Phishing Triage Engine (CyberSec Club)\n");
    printf("========================================================================\n");
}

static void print_usage(const char *prog) {
    printf("Usage:\n");
    printf("  %s <email_file.eml | email_file.txt> [options]\n\n", prog);
    printf("Options:\n");
    printf("  --json <file>   Export triage report as machine-readable JSON\n");
    printf("  --html <file>   Export interactive quarantine HTML report\n");
    printf("  --interactive   Run in interactive email inspection mode\n");
    printf("  --help          Display this help message\n\n");
    printf("Example:\n");
    printf("  %s samples/phishing_paypal.eml --html report.html --json report.json\n\n", prog);
}

static void run_interactive_mode(void) {
    EmailMessage msg;
    init_email_message(&msg);

    printf("\n[ Interactive Email Threat Assessment ]\n");
    printf("Enter Sender (e.g. \"PayPal Support <service@paypa1-security.com>\"): ");
    if (!fgets(msg.from, sizeof(msg.from), stdin)) return;
    msg.from[strcspn(msg.from, "\r\n")] = 0;

    printf("Enter Reply-To (press Enter to skip): ");
    if (fgets(msg.reply_to, sizeof(msg.reply_to), stdin)) {
        msg.reply_to[strcspn(msg.reply_to, "\r\n")] = 0;
    }

    printf("Enter Email Subject: ");
    if (fgets(msg.subject, sizeof(msg.subject), stdin)) {
        msg.subject[strcspn(msg.subject, "\r\n")] = 0;
    }

    printf("SPF Result [PASS / FAIL / NONE]: ");
    if (fgets(msg.spf_result, sizeof(msg.spf_result), stdin)) {
        msg.spf_result[strcspn(msg.spf_result, "\r\n")] = 0;
    }

    printf("DKIM Result [PASS / FAIL / NONE]: ");
    if (fgets(msg.dkim_result, sizeof(msg.dkim_result), stdin)) {
        msg.dkim_result[strcspn(msg.dkim_result, "\r\n")] = 0;
    }

    printf("Enter Email Body text (end with an empty line or line with 'END'):\n");
    char line[MAX_LINE_LEN];
    size_t blen = 0;
    while (fgets(line, sizeof(line), stdin)) {
        if (strcmp(line, "END\n") == 0 || strcmp(line, "\n") == 0 || strcmp(line, "END\r\n") == 0) {
            break;
        }
        size_t l = strlen(line);
        if (blen + l < MAX_EMAIL_BODY_LEN - 1) {
            memcpy(msg.body + blen, line, l);
            blen += l;
            msg.body[blen] = '\0';
        }
    }

    // Extract domains
    char *ob = strchr(msg.from, '<');
    if (ob) {
        size_t name_len = ob - msg.from;
        strncpy(msg.sender_display_name, msg.from, name_len);
        msg.sender_display_name[name_len] = '\0';
        extract_domain(ob, msg.sender_domain, sizeof(msg.sender_domain));
    } else {
        extract_domain(msg.from, msg.sender_domain, sizeof(msg.sender_domain));
    }

    if (strlen(msg.reply_to) > 0) {
        extract_domain(msg.reply_to, msg.reply_to_domain, sizeof(msg.reply_to_domain));
    }

    // Find links in body
    const char *protocols[] = {"http://", "https://"};
    for (int p = 0; p < 2; p++) {
        const char *cursor = msg.body;
        while ((cursor = strstr(cursor, protocols[p])) != NULL && msg.url_count < MAX_URLS) {
            char ubuf[MAX_STRING_LEN];
            size_t ulen = 0;
            while (*cursor && !isspace((unsigned char)*cursor) && ulen < sizeof(ubuf) - 1) {
                ubuf[ulen++] = *cursor++;
            }
            ubuf[ulen] = '\0';
            strncpy(msg.urls[msg.url_count++], ubuf, MAX_STRING_LEN - 1);
        }
    }

    PhishReport report;
    analyze_email(&msg, &report);
    print_terminal_report(&msg, &report);
}

int main(int argc, char *argv[]) {
    print_banner();

    if (argc < 2) {
        print_usage(argv[0]);
        return 1;
    }

    if (strcmp(argv[1], "--interactive") == 0 || strcmp(argv[1], "-i") == 0) {
        run_interactive_mode();
        return 0;
    }

    if (strcmp(argv[1], "--help") == 0 || strcmp(argv[1], "-h") == 0) {
        print_usage(argv[0]);
        return 0;
    }

    const char *input_file = argv[1];
    const char *json_out = NULL;
    const char *html_out = NULL;

    for (int i = 2; i < argc; i++) {
        if (strcmp(argv[i], "--json") == 0 && i + 1 < argc) {
            json_out = argv[++i];
        } else if (strcmp(argv[i], "--html") == 0 && i + 1 < argc) {
            html_out = argv[++i];
        }
    }

    EmailMessage msg;
    if (!parse_email_file(input_file, &msg)) {
        fprintf(stderr, "[-] Error: Failed to open or parse email file '%s'\n", input_file);
        return 1;
    }

    PhishReport report;
    analyze_email(&msg, &report);
    print_terminal_report(&msg, &report);

    if (json_out) {
        export_json_report(json_out, &msg, &report);
        printf("[+] Exported JSON report to: %s\n", json_out);
    }

    if (html_out) {
        export_html_quarantine(html_out, &msg, &report);
        printf("[+] Exported Interactive HTML Quarantine page to: %s\n", html_out);
    }

    return (report.risk_level == RISK_CRITICAL_PHISHING) ? 2 : 0;
}
