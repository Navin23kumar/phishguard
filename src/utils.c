#include "phishguard.h"

/* Convert ASCII string to lowercase in-place */
void str_to_lower(char *str) {
    if (!str) return;
    for (; *str; ++str) {
        *str = (char)tolower((unsigned char)*str);
    }
}

/* Levenshtein Distance for Typosquatting detection */
int calculate_levenshtein(const char *s1, const char *s2) {
    if (!s1 || !s2) return 999;
    int len1 = (int)strlen(s1);
    int len2 = (int)strlen(s2);
    
    if (len1 > 128 || len2 > 128) return 999;

    int d[130][130];
    for (int i = 0; i <= len1; i++) d[i][0] = i;
    for (int j = 0; j <= len2; j++) d[0][j] = j;

    for (int i = 1; i <= len1; i++) {
        for (int j = 1; j <= len2; j++) {
            int cost = (tolower((unsigned char)s1[i - 1]) == tolower((unsigned char)s2[j - 1])) ? 0 : 1;
            int del = d[i - 1][j] + 1;
            int ins = d[i][j - 1] + 1;
            int sub = d[i - 1][j - 1] + cost;
            
            int min = del;
            if (ins < min) min = ins;
            if (sub < min) min = sub;
            d[i][j] = min;
        }
    }
    return d[len1][len2];
}

/* Check if string is an IPv4 address (e.g. 192.168.1.1) */
bool is_ip_address(const char *host) {
    if (!host) return false;
    int parts = 0;
    int cur_val = 0;
    int digits_in_part = 0;
    
    for (int i = 0; host[i] != '\0'; i++) {
        char c = host[i];
        if (isdigit((unsigned char)c)) {
            cur_val = cur_val * 10 + (c - '0');
            digits_in_part++;
            if (cur_val > 255 || digits_in_part > 3) return false;
        } else if (c == '.') {
            if (digits_in_part == 0) return false;
            parts++;
            cur_val = 0;
            digits_in_part = 0;
        } else {
            return false;
        }
    }
    return (parts == 3 && digits_in_part > 0);
}

/* Extract domain from an email (e.g. user@domain.com) or URL (http://domain.com/path) */
bool extract_domain(const char *input, char *domain_out, size_t max_len) {
    if (!input || !domain_out || max_len == 0) return false;
    domain_out[0] = '\0';
    
    const char *start = NULL;
    
    // Check if it's an email address containing '@'
    const char *at = strchr(input, '@');
    if (at) {
        start = at + 1;
        // Clean trailing spaces or '>'
        size_t idx = 0;
        while (start[idx] && start[idx] != '>' && start[idx] != ' ' && start[idx] != '\r' && start[idx] != '\n' && idx < max_len - 1) {
            domain_out[idx] = (char)tolower((unsigned char)start[idx]);
            idx++;
        }
        domain_out[idx] = '\0';
        return (idx > 0);
    }
    
    // Check if URL (http:// or https:// or plain domain)
    const char *proto = strstr(input, "://");
    if (proto) {
        start = proto + 3;
    } else {
        start = input;
    }
    
    size_t idx = 0;
    while (start[idx] && start[idx] != '/' && start[idx] != ':' && start[idx] != '?' && 
           start[idx] != '#' && start[idx] != ' ' && start[idx] != '>' && start[idx] != '"' && 
           start[idx] != '\'' && start[idx] != '\r' && start[idx] != '\n' && idx < max_len - 1) {
        domain_out[idx] = (char)tolower((unsigned char)start[idx]);
        idx++;
    }
    domain_out[idx] = '\0';
    
    return (strlen(domain_out) > 0);
}
