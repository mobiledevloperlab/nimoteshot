<p align="center">
  <img src="web/assets/nimoteshot-logo.svg" alt="NimoteShot" width="320">
</p>

# NimoteShot — AI アプリストア用スクリーンショットジェネレーター

**実際の画面から、編集できる文言とローカル PNG 書き出しへ。**

アプリの実画面を **App Store と Google Play** 向けの素材に仕上げます。視覚モデルで文言を下書きし、ライブエディターでテキストとレイアウトを調整して、iPhone・iPad・Android 用の画像を書き出せます。アプリ公開を準備する個人開発者や製品チーム向けです。

**Python 3.11+ · Linux / macOS / Windows · 出力言語 17 種類 · AGPLv3+**

[English](README.md) · [简体中文](README.zh-CN.md) · 日本語 · [한국어](README.ko.md) · [Español](README.es.md)

![英語と中国語を混在させたタイトルと、その変更を反映する NimoteShot のライブプレビュー](web/assets/redefine_promotion.png)

*タイトル・サブタイトル・レイアウトを結果の隣で編集。影響するプレビューだけをローカルで更新し、追加の AI 呼び出しは不要です。実際に動作している編集画面です。*

## NimoteShot を使う理由

- **自分の製品画面から制作。** PNG・JPEG・WebP をアップロードし、見えている機能を根拠に文言を下書きします。
- **生成後も編集可能。** 文言、テンプレート、色、順序を調整し、プレビューを確認してから書き出せます。
- **複数市場と端末に対応。** 17 言語の文言版と 6 種類の端末・向きの組み合わせを選べます。付属フォントが実際の文字に対応します。
- **自分に合う使い方。** Web または CLI で操作。手動デザインは API キー不要で、AI 分析にはクラウド・ローカルの視覚モデルを選べます。

ソフトウェアは無料・オープンソースです。クラウドモデルの API 利用には、別途料金が発生する場合があります。

## クイックスタート

**Python 3.11 以降**をインストールし、リポジトリをクローンします。

```bash
git clone https://github.com/mobiledevloperlab/nimoteshot.git
cd nimoteshot
```

Linux / macOS：

```bash
./install.sh
```

Windows PowerShell：

```powershell
powershell -ExecutionPolicy Bypass -File .\install.ps1
```

インストーラーが `.venv` と依存関係を準備して起動します。**ターミナルに表示された URL** を開いてください。既定は `http://127.0.0.1:8765` です。まず **Manual design** で、キーなしで編集を試せます。

## 画面からストア素材へ

1. アプリ名、説明または公開 HTTPS サイトを入力し、実画面を 1～40 枚追加します。
2. 出力言語、端末サイズ、デザイン方向を選び、AI 分析または手動デザインを開始します。
3. 各言語版を編集し、ライブプレビューで確認します。個別変更は対象画面だけ、全体設定の変更は現在のプレビュー全体を更新します。
4. **Export PNG / ZIP** で、検証済みの多解像度 RGB/sRGB 画像と編集可能な設定を書き出します。

| 元のアプリ画面 | 生成されたストア素材 |
| --- | --- |
| <img src="demo/nimotecode/originals/code-editor.png" alt="NimoteCode コードエディターの実画面" width="220"> | <img src="demo/nimotecode/previews/01_feature.png" alt="実画面から生成された App Store 用素材" width="220"> |

[デモ全体を見る](demo/nimotecode/)。文言の再作成、ローカルでのテンプレート再選択、画像の再分析は任意の調整としてまとめ、上書き範囲を説明します。

## 言語とフォント

出力選択・編集する言語版・AI 指示・プレビュー・書き出しは、同じ **17 言語**のカタログを使います。英語、簡体字中国語、繁体字中国語、日本語、韓国語、スペイン語、フランス語、ドイツ語、ブラジルポルトガル語、ロシア語、ギリシャ語、ベトナム語、アラビア語、ヒンディー語、ベンガル語、タイ語、ヘブライ語に対応します。英語は常に含まれ、追加言語は必要に応じて選択します。

各言語版の文言は個別に保持されます。フォントは入力文字から選ぶため、英語欄にも日本語や中国語を入力できます。計画後に追加した言語は仮の文言から始まり、編集または文言の再作成を案内します。入力変換が確定してからプレビューを更新します。

操作画面は英語・簡体字中国語・日本語・韓国語・スペイン語です。フォントで表現できない文字の組み合わせや、複雑な文字の組版機能がない環境では明確なエラーを表示します。

一部の macOS / Windows の Pillow 環境では、複雑な文字のために FriBiDi の追加設定が必要です。利用できない言語は出力選択で無効になり、設定リンクを表示します。英語・中国語・日本語・韓国語などは引き続き使えます。[Pillow の設定手順](https://pillow.readthedocs.io/en/stable/installation/building-from-source.html)を参照し、有効化後に再起動してください。

## 形式・モデル・CLI

iPhone・iPad・Android の縦横、4 基本スタイル、24 カテゴリパレット、編集可能なテンプレートに対応。各タスクは原画面、SHA-256 マニフェスト、設定、プレビュー、PNG、ZIP を `store_screenshots/runs/<task-id>/` に保存します。[出力サイズ](store_screenshots/targets.json)も確認できます。

DeepSeek（既定）、Qwen、GLM、Volcengine Ark、Hunyuan、OpenAI 互換 API、Gemini、Claude、Ollama、Codex CLI 統合を選べます。スクリーンショット分析には視覚モデルと利用権限が必要です。[モデル設定](docs/PROVIDERS.md)と [CLI の詳細](README.md#cli)を参照してください。

## 更新とプライバシー

更新後は `python -m pip install -r store_screenshots/requirements.txt` を実行し、サービスを再起動します。ポートが使用中なら、このプロジェクトの確認済み・待機中サービスを正常終了して再起動します。実行中タスクや他のサービスは保持し、新しいポートと URL を表示します。プロセスは強制終了しません。

レンダリングはローカルですが、**AI 分析時は画面と製品情報が選択したプロバイダーへ送信されます**。保存を選んだキーはユーザー設定に平文で保持されます。送信権限のある画面を使い、公開前に文言と翻訳を確認してください。詳細と問題の私的な報告先は [セキュリティ方針](.github/SECURITY.md)にあります。

## 一緒に改善する

自分のアプリで試し、[再現可能な不具合を報告](https://github.com/mobiledevloperlab/nimoteshot/issues/new/choose)したり、翻訳・フォント・テンプレートを改善したり、コードや文書の PR を送れます。大きな変更は先に Issue で相談してください。実行環境とテストは [貢献ガイド](.github/CONTRIBUTING.md)、技術情報は [設計と検証](docs/VISION_UPGRADE.md)を参照してください。

## ライセンス

[GNU AGPLv3 以降](LICENSE)で公開しています。ライセンス条件に従い、利用・研究・変更・共有できます。変更版をネットワーク経由で提供する場合は、ライセンスが要求する対応ソースを提供してください。フォントなどの素材は元の条件を保持します。[第三者の表記](docs/THIRD_PARTY_NOTICES.md)、[行動規範](.github/CODE_OF_CONDUCT.md)、[運営方針](docs/GOVERNANCE.md)も確認してください。
