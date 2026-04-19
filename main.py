import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import shutil
import os

# 出力ディレクトリ作成
output_dir = "final_rigorous_validation"
if os.path.exists(output_dir): shutil.rmtree(output_dir)
os.makedirs(output_dir)

# --- 1. 数理モデル定義 ---
def u_base(i, peak): return 1.0 - 0.25 * np.abs(i - peak)
def softmax(u, beta):
    ex = np.exp(beta * u)
    return ex / np.sum(ex)

def calculate_dist_generic(v2, beta, minority_ratio=0.10, target=4):
    options = np.array([1, 2, 3, 4, 5])
    u_true1, u_true2, u_sont = u_base(options, 1), u_base(options, 3), u_base(options, target)
    p1 = softmax((1 - v2) * u_true1 + v2 * u_sont, beta)
    p2 = softmax((1 - v2) * u_true2 + v2 * u_sont, beta)
    return minority_ratio * p1 + (1 - minority_ratio) * p2

# --- Validation D: Minority Ratio Sensitivity ---
v2_range = np.linspace(0, 1, 100)
ratios = [0.01, 0.05, 0.10, 0.20]
plt.figure(figsize=(8, 5))
for r in ratios:
    probs = [calculate_dist_generic(v, 5.0, minority_ratio=r)[0] for v in v2_range]
    plt.plot(v2_range, probs, label=f'Minority {int(r*100)}%', linewidth=2)
plt.axvline(x=0.5, color='red', linestyle='--', alpha=0.5)
plt.title("Fig D: Robustness of Signal Cliff across Minority Ratios", fontsize=12)
plt.xlabel("Sontaku Weight (v2)"); plt.ylabel("Prob(Rating 1)"); plt.legend(); plt.grid(True, alpha=0.3)
plt.savefig(f"{output_dir}/fig_D_minority_sensitivity.png", dpi=300); plt.close()

# --- Validation E: Target Sensitivity ---
targets = [3, 4, 5]
plt.figure(figsize=(8, 5))
for t in targets:
    probs = [calculate_dist_generic(v, 5.0, target=t)[0] for v in v2_range]
    plt.plot(v2_range, probs, label=f'Sontaku Target = {t}', linewidth=2)
plt.axvline(x=0.5, color='red', linestyle='--', alpha=0.5)
plt.title("Fig E: Invariance of Signal Loss across Different Targets", fontsize=12)
plt.xlabel("Sontaku Weight (v2)"); plt.ylabel("Prob(Rating 1)"); plt.legend(); plt.grid(True, alpha=0.3)
plt.savefig(f"{output_dir}/fig_E_target_sensitivity.png", dpi=300); plt.close()

# --- Validation F: The Recovery Paradox ---
v2_true = 0.5; beta = 5.0
p_true = calculate_dist_generic(0, beta)
v2_ests = np.linspace(0, 1, 100)
errors = [np.sum(p_true * np.log((p_true + 1e-10) / (calculate_dist_generic(ve, beta) + 1e-10))) for ve in v2_ests]
plt.figure(figsize=(8, 5))
plt.plot(v2_ests, errors, color='black', linewidth=2)
plt.axvline(x=v2_true, color='green', linestyle=':', label='True v2')
plt.title("Fig F: Information Gap caused by Estimation Error of v2", fontsize=12)
plt.xlabel("Estimated v2"); plt.ylabel("KL Divergence from Truth"); plt.legend(); plt.grid(True, alpha=0.3)
plt.savefig(f"{output_dir}/fig_F_recovery_paradox.png", dpi=300); plt.close()

# --- CSV保存 & ZIP化 ---
pd.DataFrame({'v2': v2_range, 'Error': errors}).to_csv(f"{output_dir}/data_F_recovery.csv", index=False)
shutil.make_archive("rigorous_robustness_archive", 'zip', output_dir)
print("✅ Done. 'rigorous_robustness_archive.zip' is created.")

# Colabで実行中の場合は以下でダウンロード可能
# from google.colab import files
# files.download("rigorous_robustness_archive.zip")
