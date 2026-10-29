#include <stdio.h>
#include <string.h>
#include <ctype.h>

// Convert string to lowercase so we can match easily
void make_lowercase(char str[]) {
    for (int i = 0; str[i] != '\0'; i++) {
        str[i] = tolower(str[i]);
    }
}

int main() {
    char sender[100];
    char subject[150];
    char body[500];
    int score = 0;

    printf("====================================================\n");
    printf("   PhishGuard: Simple Fake Email Detector (C Lang)  \n");
    printf("   Created by Student Team: APEX CIPHER             \n");
    printf("====================================================\n\n");

    // 1. Get email details from user
    printf("Enter Sender Email (e.g., support@paypa1.com): ");
    fgets(sender, sizeof(sender), stdin);
    sender[strcspn(sender, "\n")] = 0; // remove newline

    printf("Enter Email Subject: ");
    fgets(subject, sizeof(subject), stdin);
    subject[strcspn(subject, "\n")] = 0;

    printf("Enter Email Body text: ");
    fgets(body, sizeof(body), stdin);
    body[strcspn(body, "\n")] = 0;

    // Convert everything to lowercase for easy checking
    make_lowercase(sender);
    make_lowercase(subject);
    make_lowercase(body);

    printf("\n--- Scanning Email Security Indicators ---\n");

    // CHECK 1: Fake / Lookalike Domain (Typosquatting)
    if (strstr(sender, "paypa1") != NULL || strstr(sender, "micr0soft") != NULL || 
        strstr(sender, "g00gle") != NULL || strstr(sender, ".xyz") != NULL || 
        strstr(sender, ".top") != NULL) {
        printf("[!] WARNING: Suspicious/Fake sender address found! (+35 points)\n");
        score = score + 35;
    }

    // CHECK 2: Urgent words in Subject
    if (strstr(subject, "urgent") != NULL || strstr(subject, "suspended") != NULL || 
        strstr(subject, "blocked") != NULL || strstr(subject, "action required") != NULL) {
        printf("[!] WARNING: Panic/Urgent subject detected! (+25 points)\n");
        score = score + 25;
    }

    // CHECK 3: Fake links or raw IP addresses in body
    if (strstr(body, "http://192.") != NULL || strstr(body, "http://10.") != NULL || 
        strstr(body, "click here") != NULL || strstr(body, "login-verify") != NULL) {
        printf("[!] WARNING: Dangerous or unsecure web link detected! (+25 points)\n");
        score = score + 25;
    }

    // CHECK 4: Asking for secret personal details (Password, OTP, Card number)
    if (strstr(body, "password") != NULL || strstr(body, "credit card") != NULL || 
        strstr(body, "otp") != NULL || strstr(body, "bank account") != NULL) {
        printf("[!] WARNING: Asking for sensitive personal/banking data! (+30 points)\n");
        score = score + 30;
    }

    // Cap score at 100
    if (score > 100) {
        score = 100;
    }

    // FINAL RESULT
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

    return 0;
}
