#ifndef PHISHGUARD_H
#define PHISHGUARD_H

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>
#include <stdbool.h>

#define MAX_LINE_LEN 2048
#define MAX_EMAIL_BODY_LEN 65536
#define MAX_URLS 128
#define MAX_KEYWORDS 128
#define MAX_RULES_TRIGGERED 64
#define MAX_STRING_LEN 256

/* Threat Risk Levels */
typedef enum {
    RISK_SAFE = 0,
    RISK_SUSPICIOUS,
    RISK_CRITICAL_PHISHING
} RiskLevel;

/* Individual Security Rule Detection */
typedef struct {
    char rule_id[32];
    char description[256];
    int score_impact;
    char evidence[256];
} RuleTrigger;

/* Email Data Structure */
typedef struct {
    char from[MAX_STRING_LEN];
    char reply_to[MAX_STRING_LEN];
    char return_path[MAX_STRING_LEN];
    char subject[MAX_STRING_LEN];
    char date[MAX_STRING_LEN];
    char spf_result[64];
    char dkim_result[64];
    char dmarc_result[64];
    
    char sender_display_name[MAX_STRING_LEN];
    char sender_domain[MAX_STRING_LEN];
    char reply_to_domain[MAX_STRING_LEN];
    
    char body[MAX_EMAIL_BODY_LEN];
    
    char urls[MAX_URLS][MAX_STRING_LEN];
    int url_count;
} EmailMessage;

/* Phishing Analysis Report */
typedef struct {
    int total_score;           // 0 to 100+ (capped at 100 for percentage)
    RiskLevel risk_level;
    RuleTrigger triggers[MAX_RULES_TRIGGERED];
    int trigger_count;
    char recommendation[512];
} PhishReport;

/* Function Prototypes */
void init_email_message(EmailMessage *msg);
bool parse_email_file(const char *filepath, EmailMessage *msg);
void analyze_email(const EmailMessage *msg, PhishReport *report);
void print_terminal_report(const EmailMessage *msg, const PhishReport *report);
void export_json_report(const char *out_filepath, const EmailMessage *msg, const PhishReport *report);
void export_html_quarantine(const char *out_filepath, const EmailMessage *msg, const PhishReport *report);

/* Utility / Detection helpers */
int calculate_levenshtein(const char *s1, const char *s2);
bool extract_domain(const char *email_or_url, char *domain_out, size_t max_len);
bool is_ip_address(const char *host);
void str_to_lower(char *str);

#endif /* PHISHGUARD_H */
