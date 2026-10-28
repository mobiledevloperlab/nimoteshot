<p align="center">
  <img src="public/nimoteshot-logo.svg" alt="NimoteShot" width="392">
</p>

<p align="center">
  <img src="public/hero-v1.png" alt="Abstract mobile screenshot cards on a dark blue background" width="100%">
</p>

<p align="center"><strong>App Store Screenshot Studio</strong></p>

<p align="center">
  English · <a href="README.zh-CN.md">简体中文</a>
</p>

<p align="center">
  Turn genuine product captures into clear, localized screenshots for your App Store and Google Play listings.
</p>

<p align="center"><em>Real PNG captures&nbsp;&nbsp;•&nbsp;&nbsp;Vision-assisted store copy&nbsp;&nbsp;•&nbsp;&nbsp;Local rendering and export</em></p>

<p align="center">
  <a href="#quick-start">Quick start</a> · <a href="#cli-workflow">CLI workflow</a> · <a href="demo/nimotecode/">Demo</a> · <a href="CHANGELOG.md">Changelog</a>
</p>

<p align="center">
  Fully open source · Free to use, modify, and share · <a href="LICENSE">GNU AGPLv3</a> · <a href="SECURITY.md">Security</a>
</p>

---

NimoteShot analyzes genuine PNG, JPEG or WebP captures with a vision model, drafts localized store copy, and renders the final artwork on your computer. Each task creates an editable folder containing source captures, a manifest, configuration, previews, exports, and a ZIP archive.

## Preview

<table>
  <tr>
    <td width="56%" valign="top">
      <img src="public/ui.png" alt="NimoteShot landing page and generated NimoteCode store screenshots" width="100%">
      <p align="center"><sub>Homepage and generated store-screenshot example</sub></p>
    </td>
    <td width="44%" valign="top">
      <img src="public/snapshot.png" alt="NimoteShot four-step screenshot builder" width="100%">
      <p align="center"><sub>Four-step local creation workflow</sub></p>
    </td>
  </tr>
</table>

### Real captures → store artwork

<table>
  <tr>
    <td width="33.33%" align="center" valign="top">
      <strong>Mobile code editor</strong><br><br>
      <img src="demo/nimotecode/originals/code-editor.png" alt="Original NimoteCode code editor capture" width="47%">
      <img src="demo/nimotecode/previews/01_feature.png" alt="Generated mobile IDE store screenshot" width="47%"><br>
      <sub>Source capture → generated feature artwork</sub>
    </td>
    <td width="33.33%" align="center" valign="top">
      <strong>SSH workspace</strong><br><br>
      <img src="demo/nimotecode/originals/ssh-workspace.png" alt="Original NimoteCode SSH workspace capture" width="47%">
      <img src="demo/nimotecode/previews/02_feature.png" alt="Generated SSH workspace store screenshot" width="47%"><br>
      <sub>Source capture → generated feature artwork</sub>
    </td>
    <td width="33.33%" align="center" valign="top">
      <strong>AI coding assistant</strong><br><br>
      <img src="demo/nimotecode/originals/ai-assistant.png" alt="Original NimoteCode AI assistant capture" width="47%">
      <img src="demo/nimotecode/previews/03_feature.png" alt="Generated AI assistant store screenshot" width="47%"><br>
      <sub>Source capture → generated feature artwork</sub>
    </td>
  </tr>
</table>

## Features

- Converts 1–40 real PNG, JPEG or WebP captures into localized store artwork.
- Produces English plus optional Chinese, Japanese, Korean, and Spanish copy.
- Renders iPhone, Android, and iPad portrait/landscape targets.
- Includes four visual styles, 28 category-aware palettes, and optional design-direction prompts.
- Defaults to DeepSeek Flash and supports Qwen, GLM, Volcengine Ark, Hunyuan, OpenAI-compatible APIs, Gemini, Claude, Ollama, and a signed-in Codex CLI workflow.
- Runs as a loopback-only local web app or a command-line tool; no Node.js build is required.
- Saves a SHA-256 source manifest and editable task configuration with each export.

## Requirements

| Component | Required version / access | Why it is needed |
| --- | --- | --- |
| Operating system | Linux, macOS, or Windows 10/11 | Runs the local studio and renderer. |
| Python | **3.11 or newer** | Required by Pillow 13 and the project scripts. |
| pip + venv | Included with a standard Python installation | Creates an isolated environment and installs dependencies. |
| Browser | A current desktop browser | Opens the local studio at `http://127.0.0.1:8765`. |
| Disk space | At least 500 MB free; more for large export sets | Holds the virtual environment, original captures, and rendered PNGs. |
| Network | Required for dependency installation and cloud providers | Local rendering stays on your computer; cloud providers receive analysis inputs. |
| Vision provider | A supported API key, configured endpoint, Ollama, or Codex CLI sign-in | Analyzes captures and drafts copy. |

### Provider prerequisites

| Provider | Credential or setup | Default model / note |
| --- | --- | --- |
| [DeepSeek](https://api-docs.deepseek.com/guides/vision/) | `DEEPSEEK_API_KEY` | DeepSeek Flash (default) |
| [Qwen](https://help.aliyun.com/en/model-studio/qwen-api-via-dashscope) | `DASHSCOPE_API_KEY` | Qwen3-VL Plus |
| [Zhipu GLM](https://docs.bigmodel.cn/cn/guide/develop/openai/introduction) | `ZAI_API_KEY` | GLM-5.3-Flash |
| Volcengine Ark | `ARK_API_KEY` | Provide an enabled vision model or endpoint ID. |
| [Tencent TokenHub](https://cloud.tencent.com/document/product/1823/136956) | `HUNYUAN_API_KEY` | HY-Vision 2.0 Instruct |
| OpenAI-compatible API | `OPENAI_API_KEY` or `NIMOTESHOT_API_KEY` | Requires an HTTPS base URL and vision-capable model. |
| Gemini / Claude | Their provider API key | Select the provider in the studio. |
| Ollama | `ollama serve`, then a local vision model | Example: `ollama pull qwen3-vl:8b`; no cloud key required. |
| Codex CLI | Install Codex CLI and run `codex login` | Uses the signed-in account; no API key is copied into NimoteShot. |

An API subscription is separate from a consumer chat subscription. Confirm your account can call the selected vision model before generating.

## Quick start

### Linux and macOS

```bash
git clone <your-repository-url> nimoteshot
cd nimoteshot
./install.sh
```

The script verifies Python 3.11+, creates `.venv`, installs runtime dependencies, and opens the studio. To start without opening a browser:

```bash
./install.sh --no-browser
```

### Windows PowerShell

```powershell
git clone <your-repository-url> nimoteshot
Set-Location nimoteshot
powershell -ExecutionPolicy Bypass -File .\install.ps1
```

If PowerShell is restricted by organizational policy, ask your administrator for an approved execution-policy workflow rather than downloading an untrusted script.

### Manual setup

```bash
python -m venv .venv
# Linux/macOS
. .venv/bin/activate
# Windows PowerShell: .venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r store_screenshots/requirements.txt
python scripts/nimoteshot.py web
```

Open the printed `http://127.0.0.1:8765` address. The server deliberately binds to loopback only; do not publish it through a proxy, port-forwarding service, or shared host.

## Use the studio

1. Enter an app name and either a brief product description or a trusted public HTTPS product page.
2. Upload 1–40 genuine PNG, JPEG or WebP captures. Use screenshots you have the right to send to your chosen provider.
3. Choose target languages, style, palette, and an optional design prompt.
4. Select a vision provider and use **Check setup** before generating.
5. Click **Analyze and plan**, then preview and edit the copy in each output language. Adjust templates, brand color and order without another AI call.
6. **Regenerate copy** uses recorded visual evidence without resending images; **Recommend layouts** uses that evidence locally. **Analyze screenshots again** explicitly refreshes the vision cache.
7. Click **Export PNG / ZIP** for validated multi-resolution downloads. Without a key, select **Manual design** and write your own copy.

The five interface languages apply to the editor, template options, buttons and status messages. Publication languages are selected separately. Single-capture layouts remain the default; paired layouts are optional and should support the same selling point. See [the architecture and verification record](docs/VISION_UPGRADE.md).

Every task is saved under `store_screenshots/runs/<task-id>/`. It contains originals, `source_manifest.json`, editable `config.json`, previews, target-sized PNGs, and a ZIP. Re-render an existing task after editing its configuration:

```bash
python scripts/generate_store_screenshots.py \
  --config store_screenshots/runs/<task-id>/config.json --all
```

Always validate current [Apple screenshot specifications](https://developer.apple.com/help/app-store-connect/reference/app-information/screenshot-specifications/) and [Google Play image requirements](https://support.google.com/googleplay/android-developer/answer/9866151) before submission.

## CLI workflow

Place PNG/JPEG/WebP captures in `screens/` (the directory is intentionally ignored by Git), configure a provider, then generate:

```bash
# Diagnose a provider configuration without uploading captures.
.venv/bin/python scripts/nimoteshot.py doctor --provider qwen

# Save a local profile without echoing the key.
.venv/bin/python scripts/nimoteshot.py configure \
  --provider qwen --prompt-api-key --verify

# Create English and Chinese exports.
.venv/bin/python scripts/nimoteshot.py generate \
  --brand "My App" \
  --description "A mobile editor with SSH, Git, and terminal tools" \
  --style editorial --provider qwen --locales zh-CN
```

On Windows, replace `.venv/bin/python` with `.venv\Scripts\python.exe`. Run `python scripts/nimoteshot.py --help` for `--website`, `--model`, `--base-url`, and `--design-prompt`.

Profiles are stored outside the repository: `~/.config/nimoteshot/config.json` on Linux/macOS and `%APPDATA%\NimoteShot\config.json` on Windows. Unix profile files are owner-only; keys are still plaintext at rest, so use an encrypted user account and rotate exposed keys.

## Privacy and security

- Rendering, packaging, and exports stay local. Captures and product descriptions are sent to the selected model for analysis.
- A product website causes an outbound HTTPS request. Use only a trusted, public site.
- Generated runs contain source captures and text; treat them as private and remove them when no longer needed.
- Model output is untrusted. Review all copy, claims, translations, and device mapping before publishing.
- Do not commit API keys, local profiles, private captures, generated runs, or archives. The supplied `.gitignore` excludes these paths.

See [SECURITY.md](SECURITY.md) for the full threat model and private vulnerability-reporting guidance.

## Development

```bash
python -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements-dev.txt
python -m ruff check .
python -m unittest discover -s tests -v
python scripts/check_repository.py
python scripts/check_secrets.py --history
```

Tests use mocked providers, so they do not require a paid model account or real API key. See [CONTRIBUTING.md](CONTRIBUTING.md) for coding conventions, test expectations, and pull-request guidance.

## Project layout

```text
nimoteshot/          Core pipeline, provider adapters, settings, and local server
web/                 Browser UI served by the local Python server
scripts/             CLI entry points, renderer, and repository checks
store_screenshots/   Target definitions, fonts, color profile, and generated runs
demo/nimotecode/     Audited demonstration captures and example output
public/              README preview images
tests/               Unit and security tests
```

## Troubleshooting

| Symptom | Likely cause | Resolution |
| --- | --- | --- |
| `Python 3.11 or newer is required` | The default `python` command targets an older interpreter. | Install Python 3.11+ and recreate `.venv`; use `python3.11` explicitly if needed. |
| `Could not create virtual environment` or `No module named venv` | Python virtual-environment support is missing. | Install your platform's Python venv package, then run the installer again. |
| `Address already in use` | Port 8765 is occupied. | Start with `python scripts/nimoteshot.py web --port 8766`, then open the printed URL. |
| The page does not open from another computer | The studio accepts local loopback hosts only by design. | Use it on the machine where it runs; do not expose it publicly. |
| Provider check says a key or model was rejected | The key lacks access, is expired, or the model ID is incorrect. | Confirm access in the provider console, choose an enabled vision model, and run `doctor` again. |
| An OpenAI-compatible endpoint fails validation | The endpoint is not HTTPS or the base URL/model is wrong. | Use the provider's HTTPS API base URL and a vision-capable model ID. |
| Ollama is not ready | The server or selected model is missing. | Run `ollama serve`, then `ollama pull qwen3-vl:8b` (or your selected model). |
| `Codex CLI was not found` | Codex is not installed or not on `PATH`. | Install the CLI, run `codex login` in a terminal, then check setup again. |
| Generation fails after upload | A capture is invalid, provider request failed, or model output was not valid JSON. | Use valid captures, verify provider setup, then retry or switch to manual design. |
| The output copy is inaccurate | Models can misread interfaces or invent claims. | Edit the task configuration, re-render, and manually review every claim before store submission. |

## Contributing and license

Contributions are welcome via forks and pull requests. Please read [CONTRIBUTING.md](CONTRIBUTING.md), [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md), and [GOVERNANCE.md](GOVERNANCE.md). Releases follow [docs/RELEASING.md](docs/RELEASING.md).

NimoteShot is fully open source and licensed under the [GNU Affero General Public License v3.0 or later](LICENSE) (AGPLv3+). You may use, study, modify, and share it at no charge; modified versions offered to users over a network must provide their corresponding source under the same license. Bundled fonts and other third-party material retain their own terms; see [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).
