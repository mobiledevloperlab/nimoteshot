<p align="center">
  <img src="web/assets/nimoteshot-logo.svg" alt="NimoteShot" width="392">
</p>

<p align="center"><strong>無料の AI App Store / Google Play スクリーンショットジェネレーター</strong></p>

<p align="center">
  <a href="README.md">English</a> · <a href="README.zh-CN.md">简体中文</a> · 日本語 · <a href="README.ko.md">한국어</a> · <a href="README.es.md">Español</a>
</p>

NimoteShot は無料・オープンソースの AI スクリーンショットジェネレーターです。実際の製品画面を App Store と Google Play 向けのローカライズされたスクリーンショットへ変換します。選択した視覚モデルで PNG、JPEG、WebP を分析してストア用文言を下書きし、レイアウトと書き出しはローカルで処理します。

## クイックスタート

リポジトリをクローンしてから、そのフォルダー内でインストーラーを実行します。アプリは無料・オープンソースですが、クラウドプロバイダーは別途 API 利用権が必要になる場合があります。ローカルモデルには Ollama を選択できます。

```bash
git clone https://github.com/mobiledevloperlab/nimoteshot.git nimoteshot
cd nimoteshot
./install.sh
```

```powershell
git clone https://github.com/mobiledevloperlab/nimoteshot.git nimoteshot
cd nimoteshot
powershell -ExecutionPolicy Bypass -File .\install.ps1
```

表示された `http://127.0.0.1:8765` を開いてください。サーバーはローカルループバックのみで待ち受けます。

## Before / after

<table>
  <tr>
    <td width="56%" valign="top"><img src="web/assets/ui.png" alt="NimoteShot のホームと生成例" width="100%"><p align="center"><sub>ホームと生成済みストア画像の例</sub></p></td>
    <td width="44%" valign="top"><img src="web/assets/snapshot.png" alt="4 ステップの制作フロー" width="100%"><p align="center"><sub>4 ステップのローカル制作フロー</sub></p></td>
  </tr>
</table>

### 実画面 → ストア素材

<table><tr>
<td width="33.33%" align="center" valign="top"><strong>モバイルコードエディタ</strong><br><br><img src="demo/nimotecode/originals/code-editor.png" alt="コードエディタの元画面" width="47%"> <img src="demo/nimotecode/previews/01_feature.png" alt="生成されたモバイル IDE 素材" width="47%"><br><sub>元画面 → 生成された機能紹介素材</sub></td>
<td width="33.33%" align="center" valign="top"><strong>SSH ワークスペース</strong><br><br><img src="demo/nimotecode/originals/ssh-workspace.png" alt="SSH ワークスペースの元画面" width="47%"> <img src="demo/nimotecode/previews/03_feature.png" alt="生成された SSH ワークスペース素材" width="47%"><br><sub>元画面 → 生成された機能紹介素材</sub></td>
<td width="33.33%" align="center" valign="top"><strong>AI コーディングアシスタント</strong><br><br><img src="demo/nimotecode/originals/ai-assistant.png" alt="AI アシスタントの元画面" width="47%"> <img src="demo/nimotecode/previews/02_feature.png" alt="生成された AI アシスタント素材" width="47%"><br><sub>元画面 → 生成された機能紹介素材</sub></td>
</tr></table>

## NimoteShot の違い

- **実画面を根拠にする:** 元画面をタスクに保存し、SHA-256 マニフェストを記録します。画面を空から生成するモックアップツールではありません。
- **AI 分析とローカルレンダリング:** 選択したモデルが画面を分析して文言を下書きし、レイアウト、PNG レンダリング、パッケージ化、書き出しは自分のコンピューターで行います。
- **編集できるローカライゼーション:** 英語と、中国語、日本語、韓国語、スペイン語の任意出力を作成し、書き出し前に文言を確認・修正できます。

## 主な機能

- 1～40 枚の実際の PNG、JPEG、WebP 画面からローカライズ済みストア素材を生成。
- 英語に加え、中国語・日本語・韓国語・スペイン語の文言を出力。
- iPhone、Android、iPad の縦横両方のターゲットサイズに対応。
- 4 種類の基本ビジュアルスタイル、24 種類のカテゴリ別パレット、任意のデザイン指示を提供。
- ローカル専用の Web アプリまたは CLI として動作。レンダリングと書き出しは端末内で完結。

## インストールとプロバイダー

インストーラーは Python 3.11 以降を確認し、`.venv` と依存関係を作成してスタジオを開きます。ブラウザを開かずに起動する場合は `./install.sh --no-browser` を実行してください。DeepSeek（既定）、Qwen、Zhipu GLM、Volcengine Ark、Hunyuan、OpenAI 互換 API、Gemini、Claude、Ollama、ログイン済み Codex CLI を選択できます。各プロバイダーの API キーまたはセットアップが必要です。

## スタジオの使い方

1. アプリ名と、短い製品説明または信頼できる公開 HTTPS 製品ページを入力します。
2. 権利を持つ実際の PNG、JPEG、WebP 画面を 1～40 枚アップロードします。
3. 出力言語、スタイル、パレット、任意のデザイン指示を選択します。
4. 視覚モデルのプロバイダーを選び、生成前に **Check setup** を実行します。
5. **Analyze and plan** をクリックして、各出力言語の文言をプレビュー・編集します。
6. **Export PNG / ZIP** で検証済みの画像を出力します。API キーがない場合は **Manual design** を選び、文言を自分で入力できます。

タスクは `store_screenshots/runs/<task-id>/` に保存され、元画面、`source_manifest.json`、編集可能な `config.json`、プレビュー、PNG、ZIP を含みます。提出前に、最新の [Apple のスクリーンショット仕様](https://developer.apple.com/help/app-store-connect/reference/app-information/screenshot-specifications/) と [Google Play の画像要件](https://support.google.com/googleplay/android-developer/answer/9866151) を必ず確認してください。

## CLI

`screens/` に PNG/JPEG/WebP を置いてプロバイダーを設定し、次を実行します。

```bash
.venv/bin/python scripts/nimoteshot.py generate \
  --brand "My App" \
  --description "SSH、Git、ターミナルを備えたモバイルエディタ" \
  --style editorial --provider qwen --locales ja-JP
```

Windows では `.venv/bin/python` を `.venv\Scripts\python.exe` に置き換えます。すべてのオプションは `python scripts/nimoteshot.py --help` で確認できます。

## プライバシーとセキュリティ

- レンダリング、パッケージ化、書き出しはローカルで実行されます。画面と製品説明は、分析のため選択したモデルへ送信されます。
- 生成物には元画面と文言が含まれます。非公開データとして扱い、不要になったら削除してください。
- モデルの出力は信頼できません。公開前にすべての文言、主張、翻訳、端末対応を確認してください。
- API キー、ローカルプロファイル、非公開画面、生成タスク、アーカイブをコミットしないでください。完全な脅威モデルは [SECURITY.md](.github/SECURITY.md) を参照してください。

開発、トラブルシューティング、プロバイダー要件、完全な技術情報は [English README](README.md) を参照してください。
