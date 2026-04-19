# Informational Health Robustness: モデルの頑健性と復元パラドックスの証明

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

本リポジトリは、アンケートや大規模データ収集における「社会的望ましさバイアス（忖度）」が情報システムに与える破壊的影響について、その構造的普遍性（頑健性）と、事後補正の不可能性（復元パラドックス）を検証するPythonシミュレーションです。

「マイノリティの比率が違えば結果も変わるのではないか」「事後的にバイアスを計算して逆算すれば真実を復元できるのではないか」というデータサイエンスの標準的な反論を、数理的に完全に反証します。

## 📌 背景と問題意識 (Background)

データ分析の現場では、データが歪んでいても「後からパラメータを推定して補正すればよい」という素朴な楽観論が存在します。しかし、本シミュレーションは以下の3つの事実を定量的に証明し、データ生成プロセスそのものが歪んだ系における「事後処理の無力さ」を提示します。

1. **マイノリティ比率への感度 (Validation D)**: 
   警告を発するマイノリティが全体の1%という極小であっても、20%という比較的大きな集団であっても、バイアスが臨界点を超えた瞬間にシグナルが「崖」のように消滅する構造は変わりません。
2. **忖度標的への感度 (Validation E)**: 
   同調圧力が「中立の3」「無難な4」「極端な5」のどこへ向かおうとも、真実の警告（評価1）が破壊されるメカニズムは不変です。
3. **復元パラドックス (Validation F)**: 
   歪んだデータから真の分布を復元しようと試みる際、分析者が推定するバイアス係数（v2）が真値からわずかにズレるだけで、復元データと真実との間にある情報ギャップ（KLダイバージェンス）は指数関数的に増大します。これは事後補正が不可能であることを意味します。

## 🧮 数理モデル (Mathematical Model)

個人の最終的な効用（U_total）を、内発的な「本音（U_true）」と外発的な「忖度（U_target）」の線形結合として定義し、Softmax関数を通じて選択確率を算出します。

U_total = (1 - v2) * U_true + v2 * U_target

* v2: 社会的望ましさ（忖度）の重み。0で完全な本音、1で完全な同調。
* Beta: 回答者の確信度。Softmax関数の鋭敏さを制御。

## 📊 出力される分析結果 (Outputs)

スクリプトを実行すると `final_rigorous_validation` ディレクトリが作成され、以下の高解像度グラフ（PNG）と生データ（CSV）が生成されます。

* **Fig D: Robustness of Signal Cliff across Minority Ratios**
  * マイノリティ比率（1%, 5%, 10%, 20%）ごとのシグナル消滅曲線の比較。
* **Fig E: Invariance of Signal Loss across Different Targets**
  * 忖度のターゲット（3, 4, 5）ごとのシグナル消滅曲線の比較。
* **Fig F: Information Gap caused by Estimation Error of v2**
  * 推定エラーが引き起こす情報ギャップ（KLダイバージェンス）の増幅を示す「復元パラドックス」の可視化。
* **data_F_recovery.csv**
  * 復元パラドックスの検証に用いた各種パラメータと誤差の生データ。

## 🚀 実行方法 (Usage)

本コードは **Google Colaboratory** または ローカルのPython環境で実行可能です。

1. `robustness_sim.py`（または Jupyter Notebook形式）を実行します。
2. 計算完了後、グラフとCSVを格納した `rigorous_robustness_archive.zip` が生成されます。

### ローカル環境での実行に関する注意
ローカルのPython環境（VSCode, JupyterLab等）で実行する場合は、Colab固有のモジュールを無効化してください。
スクリプト内の `from google.colab import files` および、末尾のコメントアウトされている `files.download(...)` は使用せず、そのままスクリプトを実行すると作業ディレクトリにZIPファイルが生成されます。

```bash
# 依存ライブラリのインストール
pip install -r requirements.txt

# スクリプトの実行
python robustness_sim.py
