<p align="center">
  <img src="web/assets/nimoteshot-logo.svg" alt="NimoteShot" width="320">
</p>

# NimoteShot — AI App Store Screenshot Generator

**Real app screens. Editable copy. Local PNG exports.**

Create localized **App Store and Google Play screenshots** from your own app captures. Let a vision model draft the story, refine the copy and layout in a live editor, then export images for iPhone, iPad and Android. Built for indie developers and product teams preparing their next app release.

**Python 3.11+ · Linux / macOS / Windows · 17 output languages · AGPLv3+**

English · [简体中文](README.zh-CN.md) · [日本語](README.ja.md) · [한국어](README.ko.md) · [Español](README.es.md)

[Get started](#quick-start) · [See the workflow](#from-capture-to-store-artwork) · [Languages](#languages) · [Contribute](#build-with-us)

![NimoteShot live screenshot editor showing mixed English and Chinese title edits beside the rendered App Store preview](web/assets/redefine_promotion.png)

*Edit the title, subtitle or layout beside the result. Changes update the affected previews locally, without another AI call. The image above is the working editor.*

## Why use NimoteShot?

- **Start with your actual product.** Upload real PNG, JPEG or WebP captures. The model drafts copy from visible features; your source screens become the artwork.
- **Keep control after generation.** Edit text, templates, color and order. Preview changes automatically, retry a failed preview, and export when the result is ready.
- **Prepare more than one listing.** Choose from 17 language versions and six device/orientation groups. Mixed Chinese/English input and common writing systems use bundled fonts.
- **Use it your way.** Work in the browser or CLI. Manual design needs no API key; AI analysis supports cloud and local vision providers. Rendering and ZIP packaging run locally.

NimoteShot is free, open-source software. Cloud model providers may charge separately for API usage.

## Quick start

Install **Python 3.11 or newer**, then clone the repository:

```bash
git clone https://github.com/mobiledevloperlab/nimoteshot.git
cd nimoteshot
```

**Linux / macOS**

```bash
./install.sh
```

**Windows PowerShell**

```powershell
powershell -ExecutionPolicy Bypass -File .\install.ps1
```

The installer creates `.venv`, installs dependencies and starts the studio. Open the **URL printed in your terminal**; the default is `http://127.0.0.1:8765`.

Choose **Manual design** to try the editor without a model key. For AI-assisted copy, select a provider, enter its credentials and run **Check model configuration**.

<details>
<summary>Manual installation, updates and startup options</summary>

```bash
python -m venv .venv
# Linux / macOS:
. .venv/bin/activate
# Windows PowerShell:
# .venv\Scripts\Activate.ps1
python -m pip install -r store_screenshots/requirements.txt
python scripts/nimoteshot.py web
```

After updating the repository, reinstall the requirements and restart the studio. `--no-browser` starts without opening a browser; `--port 8766` sets a preferred port.

If the port is occupied, a verified idle studio from this checkout is shut down normally and replaced. Active tasks, other programs and older instances without verification stay running; the new studio selects a free local port. No process is force-killed.

</details>

## From capture to store artwork

1. **Add your product.** Enter an app name and a short description or public HTTPS website. Upload 1–40 real captures.
2. **Choose the output.** Select languages, device sizes and a design direction. Use AI analysis or start with manual design.
3. **Preview and refine.** Edit each language version, adjust templates and compare the live result. Copy and per-screen layout edits render only the affected screens; global changes refresh the current preview set.
4. **Export PNG / ZIP.** Download validated RGB/sRGB images at the selected resolutions, together with an editable task configuration.

| Original app capture | Generated store screenshot |
| --- | --- |
| <img src="demo/nimotecode/originals/code-editor.png" alt="Original NimoteCode mobile code editor screenshot" width="220"> | <img src="demo/nimotecode/previews/01_feature.png" alt="NimoteCode App Store screenshot generated from the real code editor capture" width="220"> |

[Explore the NimoteCode demo](demo/nimotecode/) for more source captures and example artwork.

### Refine without starting over

**Copy version to edit** selects an independent language version. Each version keeps its edits; fonts follow the text you type, so an English field can also render Chinese. Select additional output languages in **Product context**. Languages added after planning start with clearly identified placeholder copy to edit or regenerate.

Optional adjustments explain their scope: **Regenerate copy** rewrites selected-language copy using saved visual evidence; **Recommend layouts** resets templates locally while keeping copy; **Analyze screenshots again** replaces the design through a new vision-model request.

## Languages

The output picker, copy-version selector, AI prompt, preview and export share the same **17-language catalog**:

| | Output languages |
| --- | --- |
| English + East Asia | English, Simplified Chinese, Traditional Chinese, Japanese, Korean |
| Europe and the Americas | Spanish, French, German, Brazilian Portuguese, Russian, Greek |
| South / Southeast Asia | Hindi, Bengali, Vietnamese, Thai |
| Middle East | Arabic, Hebrew |

English is included by default; choose the additional versions you need. The **interface** is available in English, Simplified Chinese, Japanese, Korean and Spanish.

Bundled fonts are selected by actual character coverage for app names, titles and subtitles. Preview and export use the same text rendering. IME composition completes before a preview request is scheduled. Complex scripts use [Pillow's libraqm shaping](https://pillow.readthedocs.io/en/stable/reference/ImageFont.html); unavailable shaping or unsupported character combinations produce a clear error instead of silent missing-glyph boxes.

## Formats and design

| Capability | Included |
| --- | --- |
| Input | 1–40 PNG, JPEG or WebP captures, grouped into up to 10 feature screens |
| Devices | iPhone, iPad and Android; portrait and landscape |
| Design | 4 base styles, 24 category palettes, design prompts and editable templates |
| Preview | Local rendering, updates for affected screens, stale-response protection and retry |
| Export | Multi-resolution PNGs, sRGB profiles, ZIP completeness checks and editable configuration |
| Traceability | Archived originals and a SHA-256 source manifest for every generated task |

Tasks are saved in `store_screenshots/runs/<task-id>/`. See [target definitions](store_screenshots/targets.json) for exact sizes. Review your copy and current [Apple screenshot specifications](https://developer.apple.com/help/app-store-connect/reference/app-information/screenshot-specifications/) / [Google Play image requirements](https://support.google.com/googleplay/android-developer/answer/9866151) before submission.

## Providers

Choose DeepSeek (default), Qwen, Zhipu GLM, Volcengine Ark, Tencent Hunyuan, OpenAI-compatible APIs, Gemini, Claude, Ollama or the signed-in Codex CLI integration. Availability depends on your selected model and account. The studio exposes provider setup and connection checks; [model presets](nimoteshot/models.json) are the configuration source.

Use a **vision-capable model** for screenshot analysis. Manual editing and export do not call a model. Configure cloud credentials in the studio or through environment variables / a local profile. See [provider setup details](docs/PROVIDERS.md).

## CLI

Put your captures in `screens/`, configure a provider, then generate:

```bash
.venv/bin/python scripts/nimoteshot.py configure \
  --provider qwen --prompt-api-key --verify

.venv/bin/python scripts/nimoteshot.py generate \
  --brand "My App" \
  --description "A mobile editor with SSH, Git and terminal tools" \
  --provider qwen --style editorial --locales zh-CN,fr-FR,ja-JP
```

On Windows, use `.venv\Scripts\python.exe` in place of `.venv/bin/python`. Run `python scripts/nimoteshot.py generate --help` for all output locale IDs and options. Re-render an edited task without AI:

```bash
python scripts/generate_store_screenshots.py \
  --config store_screenshots/runs/<task-id>/config.json --all
```

## Privacy and troubleshooting

The web service listens on localhost. Rendering stays on your computer; **AI analysis sends captures and product context to your selected provider**. Website input fetches that public page. Keys entered in the UI are kept in page memory unless you explicitly save configuration; saved profiles are plaintext files in your user configuration directory. Treat task folders and ZIPs as private.

| Problem | Try this |
| --- | --- |
| Missing Python / `venv` | Install Python 3.11+ with pip and venv support; rerun the installer. |
| Provider rejected a key or model | Check account access, model ID and endpoint, then run the model configuration check. |
| Preview fails or text is too long | Shorten the copy or adjust the layout; inspect the preview message and retry. Manual design remains available. |
| Old page or missing new languages | Update requirements, restart the service and open the printed URL in a new tab. |
| Port already occupied | Startup verifies an idle old studio or selects another port. Use the URL it prints. |

Use only captures you have permission to send. Review model-generated claims and translations before publishing. Keep keys and private captures out of Git. See the [security policy](.github/SECURITY.md) for the threat model and vulnerability-reporting instructions.

## Build with us

Useful contributions come in many forms:

- **Try it on your app.** [Report a reproducible bug](https://github.com/mobiledevloperlab/nimoteshot/issues/new/choose) with the command or UI steps, expected result and redacted error.
- **Improve a language or layout.** Help review translations, font behavior, device formats and templates. Discuss larger changes in an issue first.
- **Contribute code or docs.** Fork the repository and open a focused PR. [CONTRIBUTING.md](.github/CONTRIBUTING.md) covers setup, checks and review; draft PRs are welcome.

```bash
python -m pip install -r requirements-dev.txt
python -m ruff check .
python scripts/run_tests.py
python scripts/check_repository.py
```

The default suite uses synthetic data or bundled demo captures with mocked providers; real provider calls are opt-in. Browser and visual regression tests cover editing, language switching, previews and exports. See the [architecture and verification notes](docs/VISION_UPGRADE.md), [changelog](docs/CHANGELOG.md), [governance](docs/GOVERNANCE.md) and [code of conduct](.github/CODE_OF_CONDUCT.md).

## License

NimoteShot is licensed under the [GNU Affero General Public License v3.0 or later](LICENSE) (`AGPL-3.0-or-later`). Use, study, modify and share it under those terms. Modified versions offered over a network must provide their corresponding source as required by the license. Fonts and other third-party assets retain their own licenses; see [third-party notices](docs/THIRD_PARTY_NOTICES.md).
