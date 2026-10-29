#include "phishguard.h"

void init_email_message(EmailMessage *msg) {
    if (!msg) return;
    memset(msg, 0, sizeof(EmailMessage));
}

/* Extract URLs from message body */
static void scan_for_urls(EmailMessage *msg) {
    const char *text = msg->body;
    const char *protocols[] = {"http://", "https://", "ftp://"};
    int num_proto = 3;

    for (int p = 0; p < num_proto; p++) {
        const char *cursor = text;
        while ((cursor = strstr(cursor, protocols[p])) != NULL && msg->url_count < MAX_URLS) {
            char url_buf[MAX_STRING_LEN];
            size_t ulen = 0;
            
            while (*cursor && !isspace((unsigned char)*cursor) && 
                   *cursor != '"' && *cursor != '\'' && *cursor != '<' && *cursor != '>' && 
                   ulen < sizeof(url_buf) - 1) {
                url_buf[ulen++] = *cursor++;
            }
            url_buf[ulen] = '\0';
            
            // Deduplicate
            bool exists = false;
            for (int i = 0; i < msg->url_count; i++) {
                if (strcmp(msg->urls[i], url_buf) == 0) {
                    exists = true;
                    break;
                }
            }
            if (!exists && ulen > 7) {
                strncpy(msg->urls[msg->url_count], url_buf, MAX_STRING_LEN - 1);
                msg->url_count++;
            }
        }
    }
}

/* Parse RFC-822 / RFC-5322 style raw email (.eml / .txt) */
bool parse_email_file(const char *filepath, EmailMessage *msg) {
    FILE *fp = fopen(filepath, "r");
    if (!fp) {
        return false;
    }

    init_email_message(msg);
    char line[MAX_LINE_LEN];
    bool in_headers = true;
    size_t body_len = 0;

    while (fgets(line, sizeof(line), fp)) {
        if (in_headers) {
            // An empty line indicates the boundary between email headers and the body
            if (line[0] == '\r' || line[0] == '\n') {
                in_headers = false;
                continue;
            }

            if (strncasecmp(line, "From:", 5) == 0) {
                char *val = line + 5;
                while (*val == ' ') val++;
                val[strcspn(val, "\r\n")] = 0;
                strncpy(msg->from, val, sizeof(msg->from) - 1);
                
                // Parse display name and domain
                char *open_bracket = strchr(val, '<');
                if (open_bracket) {
                    size_t name_len = open_bracket - val;
                    if (name_len > 0) {
                        strncpy(msg->sender_display_name, val, name_len);
                        msg->sender_display_name[name_len] = '\0';
                        // Trim trailing quotes/spaces
                        char *end = msg->sender_display_name + strlen(msg->sender_display_name) - 1;
                        while (end > msg->sender_display_name && (*end == ' ' || *end == '"' || *end == '\'')) {
                            *end = '\0';
                            end--;
                        }
                    }
                    extract_domain(open_bracket, msg->sender_domain, sizeof(msg->sender_domain));
                } else {
                    extract_domain(val, msg->sender_domain, sizeof(msg->sender_domain));
                }
            } else if (strncasecmp(line, "Reply-To:", 9) == 0) {
                char *val = line + 9;
                while (*val == ' ') val++;
                val[strcspn(val, "\r\n")] = 0;
                strncpy(msg->reply_to, val, sizeof(msg->reply_to) - 1);
                extract_domain(val, msg->reply_to_domain, sizeof(msg->reply_to_domain));
            } else if (strncasecmp(line, "Return-Path:", 12) == 0) {
                char *val = line + 12;
                while (*val == ' ') val++;
                val[strcspn(val, "\r\n")] = 0;
                strncpy(msg->return_path, val, sizeof(msg->return_path) - 1);
            } else if (strncasecmp(line, "Subject:", 8) == 0) {
                char *val = line + 8;
                while (*val == ' ') val++;
                val[strcspn(val, "\r\n")] = 0;
                strncpy(msg->subject, val, sizeof(msg->subject) - 1);
            } else if (strncasecmp(line, "Date:", 5) == 0) {
                char *val = line + 5;
                while (*val == ' ') val++;
                val[strcspn(val, "\r\n")] = 0;
                strncpy(msg->date, val, sizeof(msg->date) - 1);
            } else if (strncasecmp(line, "Authentication-Results:", 23) == 0 ||
                       strncasecmp(line, "Received-SPF:", 13) == 0) {
                char temp[MAX_LINE_LEN];
                strncpy(temp, line, sizeof(temp));
                str_to_lower(temp);
                if (strstr(temp, "spf=fail") || strstr(temp, "spf: fail") || strstr(temp, "fail (")) {
                    strncpy(msg->spf_result, "FAIL", sizeof(msg->spf_result) - 1);
                } else if (strstr(temp, "spf=pass") || strstr(temp, "pass (")) {
                    strncpy(msg->spf_result, "PASS", sizeof(msg->spf_result) - 1);
                }
                
                if (strstr(temp, "dkim=fail")) {
                    strncpy(msg->dkim_result, "FAIL", sizeof(msg->dkim_result) - 1);
                } else if (strstr(temp, "dkim=pass")) {
                    strncpy(msg->dkim_result, "PASS", sizeof(msg->dkim_result) - 1);
                }
                
                if (strstr(temp, "dmarc=fail")) {
                    strncpy(msg->dmarc_result, "FAIL", sizeof(msg->dmarc_result) - 1);
                } else if (strstr(temp, "dmarc=pass")) {
                    strncpy(msg->dmarc_result, "PASS", sizeof(msg->dmarc_result) - 1);
                }
            }
        } else {
            // Email body accumulation
            size_t l = strlen(line);
            if (body_len + l < MAX_EMAIL_BODY_LEN - 1) {
                memcpy(msg->body + body_len, line, l);
                body_len += l;
                msg->body[body_len] = '\0';
            }
        }
    }

    fclose(fp);
    scan_for_urls(msg);
    return true;
}
