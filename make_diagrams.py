import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches

os.makedirs("docs/images", exist_ok=True)

# -------------------------------------------------------------
# Image 1: Phishing Architecture & Flow (What is Phishing?)
# -------------------------------------------------------------
fig, ax = plt.subplots(figsize=(8, 3.5), dpi=200)
ax.set_xlim(0, 10)
ax.set_ylim(0, 4)
ax.axis('off')

# Box 1: Attacker
ax.add_patch(patches.FancyBboxPatch((0.5, 1.2), 2.2, 1.8, boxstyle="round,pad=0.1", fc="#fee2e2", ec="#ef4444", lw=2))
ax.text(1.6, 2.4, "Attacker / Hacker", ha='center', va='center', fontsize=11, fontweight='bold', color="#b91c1c")
ax.text(1.6, 1.7, "• Creates fake email\n• Spoofs bank name\n• Adds urgency", ha='center', va='center', fontsize=8, color="#7f1d1d")

# Arrow 1
ax.annotate('', xy=(3.8, 2.1), xytext=(2.8, 2.1),
            arrowprops=dict(facecolor='#ef4444', edgecolor='#b91c1c', width=2, headwidth=7))
ax.text(3.3, 2.4, "Fake Email", ha='center', fontsize=8, fontweight='bold', color="#b91c1c")

# Box 2: PhishGuard (Our C Program)
ax.add_patch(patches.FancyBboxPatch((3.9, 0.8), 2.5, 2.4, boxstyle="round,pad=0.1", fc="#eff6ff", ec="#3b82f6", lw=2))
ax.text(5.15, 2.7, "PhishGuard (C Program)", ha='center', va='center', fontsize=11, fontweight='bold', color="#1d4ed8")
ax.text(5.15, 1.7, "1. Checks Fake Sender\n2. Checks Urgent Words\n3. Checks Fake IP Links\n4. Checks Data Demand", ha='center', va='center', fontsize=8, color="#1e3a8a")

# Arrow 2
ax.annotate('', xy=(7.4, 2.1), xytext=(6.5, 2.1),
            arrowprops=dict(facecolor='#10b981', edgecolor='#047857', width=2, headwidth=7))
ax.text(6.95, 2.4, "Analysis", ha='center', fontsize=8, fontweight='bold', color="#047857")

# Box 3: User Protected
ax.add_patch(patches.FancyBboxPatch((7.5, 1.2), 2.2, 1.8, boxstyle="round,pad=0.1", fc="#ecfdf5", ec="#10b981", lw=2))
ax.text(8.6, 2.4, "User / Student", ha='center', va='center', fontsize=11, fontweight='bold', color="#047857")
ax.text(8.6, 1.7, "Safe from Scam!\nResult: ALERT or SAFE\nPoints: 0 to 100", ha='center', va='center', fontsize=8, color="#065f46")

plt.tight_layout()
plt.savefig("docs/images/phishing_flow.png", bbox_inches='tight')
plt.close()

# -------------------------------------------------------------
# Image 2: Anatomy of a Phishing Email (Visual Example)
# -------------------------------------------------------------
fig, ax = plt.subplots(figsize=(8, 4.2), dpi=200)
ax.set_xlim(0, 10)
ax.set_ylim(0, 5)
ax.axis('off')

# Email outer box
ax.add_patch(patches.FancyBboxPatch((0.5, 0.3), 9, 4.4, boxstyle="round,pad=0.1", fc="#f8fafc", ec="#94a3b8", lw=2))
ax.text(5, 4.4, "ANATOMY OF A FAKE EMAIL (WHAT OUR CODE CHECKS)", ha='center', fontsize=12, fontweight='bold', color="#0f172a")

# From line
ax.text(0.9, 3.8, "From:  PayPal Security <support@paypa1.com>", fontsize=9.5, fontfamily='monospace', color="#0f172a")
ax.add_patch(patches.FancyBboxPatch((6.3, 3.65), 3.0, 0.45, boxstyle="round,pad=0.05", fc="#fee2e2", ec="#dc2626", lw=1))
ax.text(7.8, 3.88, "[CHECK 1: Fake Domain 'paypa1']", ha='center', fontsize=8, fontweight='bold', color="#b91c1c")

# Subject line
ax.text(0.9, 3.1, "Subject: URGENT: Your account suspended immediately!", fontsize=9.5, fontfamily='monospace', color="#0f172a")
ax.add_patch(patches.FancyBboxPatch((6.3, 2.95), 3.0, 0.45, boxstyle="round,pad=0.05", fc="#fef3c7", ec="#d97706", lw=1))
ax.text(7.8, 3.18, "[CHECK 2: Panic Word 'URGENT']", ha='center', fontsize=8, fontweight='bold', color="#92400e")

# Body line 1
ax.text(0.9, 2.3, "Dear User, someone tried to hack your account.", fontsize=9, fontfamily='monospace', color="#334155")
ax.text(0.9, 1.8, "Click here to login: http://192.168.1.50/verify", fontsize=9, fontfamily='monospace', color="#1d4ed8")
ax.add_patch(patches.FancyBboxPatch((6.3, 1.65), 3.0, 0.45, boxstyle="round,pad=0.05", fc="#fee2e2", ec="#dc2626", lw=1))
ax.text(7.8, 1.88, "[CHECK 3: Raw IP Link, Not PayPal]", ha='center', fontsize=8, fontweight='bold', color="#b91c1c")

# Body line 2
ax.text(0.9, 1.1, "Please verify your credit card & password now.", fontsize=9, fontfamily='monospace', color="#334155")
ax.add_patch(patches.FancyBboxPatch((6.3, 0.95), 3.0, 0.45, boxstyle="round,pad=0.05", fc="#fee2e2", ec="#dc2626", lw=1))
ax.text(7.8, 1.18, "[CHECK 4: Asks for Credit Card]", ha='center', fontsize=8, fontweight='bold', color="#b91c1c")

plt.tight_layout()
plt.savefig("docs/images/email_breakdown.png", bbox_inches='tight')
plt.close()

# -------------------------------------------------------------
# Image 3: Score Meter Diagram
# -------------------------------------------------------------
fig, ax = plt.subplots(figsize=(8, 2.2), dpi=200)
ax.set_xlim(0, 100)
ax.set_ylim(0, 2)
ax.axis('off')

# Safe bar (0 - 20)
ax.add_patch(patches.Rectangle((0, 0.6), 20, 0.8, fc="#22c55e", ec="#15803d", lw=1.5))
ax.text(10, 1.0, "0 - 19: SAFE", ha='center', va='center', fontsize=10, fontweight='bold', color="white")

# Suspicious bar (20 - 50)
ax.add_patch(patches.Rectangle((20, 0.6), 30, 0.8, fc="#f59e0b", ec="#b45309", lw=1.5))
ax.text(35, 1.0, "20 - 49: SUSPICIOUS", ha='center', va='center', fontsize=10, fontweight='bold', color="white")

# Danger bar (50 - 100)
ax.add_patch(patches.Rectangle((50, 0.6), 50, 0.8, fc="#ef4444", ec="#b91c1c", lw=1.5))
ax.text(75, 1.0, "50 - 100: CRITICAL PHISHING!", ha='center', va='center', fontsize=10, fontweight='bold', color="white")

ax.text(50, 1.7, "PHISHGUARD RISK SCORING METER", ha='center', fontsize=11, fontweight='bold', color="#0f172a")

plt.tight_layout()
plt.savefig("docs/images/score_meter.png", bbox_inches='tight')
plt.close()

print("[+] Generated 3 illustrative diagrams in docs/images/")
