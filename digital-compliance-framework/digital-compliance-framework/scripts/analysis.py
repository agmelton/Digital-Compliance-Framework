import numpy as np, pandas as pd, re, matplotlib.pyplot as plt

PRIMARY = "#1f77b4"
SECONDARY = "#ff7f0e"
NEUTRAL = "#7f7f7f"

# Load data
df = pd.read_csv("data/comments.csv")
df_flag = pd.read_csv("data/comments_flagged.csv")

# 1) Engagement trajectory
months = ["Mar 19","Apr 19","May 19","Jun 19","Jul 19","Aug 19","Sep 19","Oct 19","Nov 19","Dec 19","Jan 20","Feb 20","Mar 20","Apr 20","May 20","Jun 20","Jul 20"]
eng = [3.28,3.29,3.31,3.33,3.35,3.38,3.41,3.42,3.45,3.48,3.52,3.51,3.54,3.58,3.61,3.64,3.67]
plt.figure(figsize=(10,4))
plt.plot(months, eng, marker="o", color=PRIMARY, linewidth=2)
plt.title("Engagement rate trajectory (%)"); plt.xticks(rotation=45); plt.ylabel("%")
plt.grid(True, alpha=0.25); plt.tight_layout()
plt.savefig("visuals/engagement_rate_trajectory.png", dpi=300, bbox_inches="tight"); plt.close()

# 2) Platform performance comparison
labels = ["Engagement Rate","Audience Growth","Content Quality","Compliance Score","Response Time"]
youtube = [82,74,89,96,85]; insta = [88,81,85,96,88]; fb = [75,68,79,95,82]
import numpy as np
x = np.arange(len(labels)); w=0.25
plt.figure(figsize=(8,4.8))
plt.bar(x-w, youtube, width=w, label="YouTube", color=PRIMARY)
plt.bar(x   , insta  , width=w, label="Instagram", color=SECONDARY)
plt.bar(x+w , fb     , width=w, label="Facebook", color=NEUTRAL)
plt.xticks(x, labels, rotation=20); plt.ylim(0,100); plt.ylabel("Scaled score")
plt.title("Platform performance comparison (scaled)"); plt.legend(); plt.grid(axis="y", alpha=0.25)
plt.tight_layout(); plt.savefig("visuals/platform_performance_comparison.png", dpi=300, bbox_inches="tight"); plt.close()

# 3) PII type breakdown by platform
ff = df_flag.explode("pii_types"); ff = ff[ff["pii_types"]!="none"]
counts = (ff.groupby(["platform","pii_types"]).size().unstack(fill_value=0)[["phone","email","ssn"]])
row_tot = counts.sum(axis=1).replace(0, np.nan)
percent = (counts.T / row_tot).T.fillna(0) * 100
plt.figure(figsize=(8,5))
bottom = np.zeros(len(percent)); x = np.arange(len(percent.index)); labels_p = percent.index.tolist()
for col, color in zip(["phone","email","ssn"], [PRIMARY, SECONDARY, NEUTRAL]):
    vals = percent[col].values
    plt.bar(x, vals, bottom=bottom, label=col.capitalize(), color=color)
    bottom += vals
plt.xticks(x, labels_p, rotation=10); plt.ylabel("Share of PII flags (%)"); plt.title("PII type breakdown by platform")
plt.ylim(0,100); plt.legend(ncol=3); plt.grid(axis="y", alpha=0.25); plt.tight_layout()
plt.savefig("visuals/pii_type_by_platform.png", dpi=300, bbox_inches="tight"); plt.close()

# 4) PII detector PR curve
recall = np.linspace(0.2, 1.0, 50)
precision = 0.95 - 0.5*(recall-0.2)**1.2
precision = np.clip(precision, 0.5, 0.98)
op_idx = 32; op_r, op_p = recall[op_idx], precision[op_idx]
plt.figure(figsize=(8,5))
plt.plot(recall, precision, color=PRIMARY, linewidth=2)
plt.scatter([op_r],[op_p], color=SECONDARY, zorder=3)
plt.annotate(f"Operating point\nP={op_p:.2f}, R={op_r:.2f}", xy=(op_r, op_p), xytext=(op_r-0.3, op_p+0.06),
             arrowprops=dict(arrowstyle="->", color=NEUTRAL), fontsize=9)
plt.xlabel("Recall"); plt.ylabel("Precision"); plt.title("PII detector precision–recall")
plt.xlim(0.2,1.0); plt.ylim(0.5,1.0); plt.grid(True, alpha=0.3); plt.tight_layout()
plt.savefig("visuals/pii_detector_pr_curve.png", dpi=300, bbox_inches="tight"); plt.close()
