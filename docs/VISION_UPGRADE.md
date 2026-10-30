# Vision pipeline upgrade — implementation and verification

Updated: 2026-10-28. This record describes the implemented code and local verification, not a claim that every possible input or operating system was tested.

## Audit and retained architecture

NimoteShot uses a localhost Python HTTP service, vanilla JavaScript/CSS, Pillow, OpenAI SDK and standard-library ZIP packaging. The audit covered provider profiles and credential handling, the four-step studio and localization, upload validation, AI prompts, configuration construction, rendering, source manifests and exports. The existing 28 styles, 10 design prompt presets, 17 publication languages, six device groups, native source overrides, CLI, original archives and RGB/sRGB validation are retained. No frontend framework or AI image-generation service was introduced.

The main gaps were unversioned copy-only AI proposals, duplicated template choices, a fixed English/iPhone preview, no independent regeneration controls, no bounded cache, and incomplete failure/browser coverage. The implementation extends those existing paths rather than replacing them. Existing task directories are never overwritten; exports create unique new task IDs. Legacy configs keep their original layout when no new template metadata is present.

## Responsibilities and actual files

| Files | Responsibility |
| --- | --- |
| `nimoteshot/providers.py`, `models.json` | Default DeepSeek Flash; retain other providers; real image blocks; SDK timeout/retry/error handling |
| `nimoteshot/captures.py` | Shared PNG/JPEG/WebP verification, size/dimension limits, safe upload filenames |
| `nimoteshot/analyzer.py` | JSON content-addressed analysis, expiry, size eviction, concurrency lock |
| `nimoteshot/planner.py` | Copy regeneration from recorded visual evidence and local layout recommendations |
| `nimoteshot/design.py`, `design.schema.json`, `templates.json` | Versioned schema, safe repair, closed design tokens and template registry |
| `nimoteshot/pipeline.py` | Shared orchestration, source/config/analysis archives, compatibility checks |
| `scripts/generate_store_screenshots.py` | Existing Pillow renderer; relative layouts and real-source compositions |
| `nimoteshot/export_service.py` | Existing multi-resolution render/validation calls plus ZIP completeness and CRC checks |
| `nimoteshot/server.py` | Separate plan, revise, preview and export APIs; existing localhost/Host/Origin protection |
| `web/app.js`, `editor-i18n.js`, `index.html`, `style.css` | Simple plan → edit/preview → export flow, five-language controls, independent actions |
| `tests/test_upgrade.py`, `test_design.py`, `test_i18n.py`, `test_visual_regression.py`, `test_browser_workflow.py` | Schema, cache, provider faults, layouts, localization and browser coverage |
| `tests/visual-baselines.json`, `update_visual_baselines.py` | 17 deterministic pixel-hash baselines; explicit update command |
| `.github/workflows/ci.yml`, dependency lists | Existing unit CI plus a Chromium job; Playwright is development-only |
| `README.md`, `README.zh-CN.md`, `store_screenshots/README.md`, `docs/CHANGELOG.md`, `docs/THIRD_PARTY_NOTICES.md` | Usage, cleanup, changes and dependency notices |

Removed `prompts/review.en.md` and `review.zh-CN.md`: they were optional human review briefs, not runtime prompts. Their only documentation link was removed. Runtime AI prompts remain in the pipeline/planner. Previous PNG golden fixtures are replaced by pixel hashes to avoid accumulating screenshot binaries in source control; reviewed previews are local test artifacts.

## AI, schema and security

Default endpoint: `https://api.deepseek.com`; model: `deepseek-flash`; environment variable: `DEEPSEEK_API_KEY`. User-entered keys live in page memory and go to the local service and chosen provider. Generation does not persist them. Explicit Save configuration retains the existing local profile behavior. Server-held keys are never sent to the browser. The app continues to bind to loopback and must not be exposed as a public proxy.

Pillow verifies actual PNG/JPEG/WebP contents, at most 32 MiB and 8192 pixels per side. Input collections accept 1–40 captures; device/language variants can be grouped into 1–10 promotional features. Bounded JPEG representations of the actual pixels are sent jointly with app context; filenames alone are not the analysis input. DeepSeek requests ask for JSON, limit output to 8192 tokens, use a 90-second SDK timeout and at most two SDK retries. SDK errors expose status/help instead of provider bodies that might echo credentials.

`jsonschema` Draft 2020-12 validates version 1 before rendering. The configuration permits only known templates, finite size/alignment/typography/focus tokens and a validated hex brand accent. It cannot carry executable code, CSS or arbitrary coordinates. Filename and locale/target membership checks follow schema validation. Safe repairs convert factual string lists to canonical text and replace unknown template names with balanced. Unsupported instructions, invalid mappings and future schema versions are rejected. Malformed JSON surfaces a localized error and manual design remains usable. Legacy proposals without analysis metadata remain accepted for manual/config compatibility; new vision analysis must include evidence and a page type.

The prompts require visible evidence, distinguish menu visibility from successful behavior, retain uncertainty, and treat screenshot/website text as data. Recorded evidence is displayed for review. Copy regeneration sends evidence, not images, and preserves source mapping, analysis, design and order. Layout regeneration uses recorded page types locally without a model call.

Cache keys include schema/prompt version, actual image hashes, filenames, context, selected model and effective endpoint. `store_screenshots/runs/.vision-cache` uses non-executable JSON entries with a seven-day TTL, 64 MiB size limit, LRU eviction, atomic replacement and a per-key lock. Failed/invalid results are not cached. Reanalyze explicitly refreshes the entry. Delete the cache directory while idle to clear it. Each exported task also saves `analysis.json`, `config.json` and unchanged originals with SHA-256 manifest.

## Design and workflow

Analyze and plan produces a complete preview before high-resolution export. Manual mode starts with editable placeholders and needs no key. The editor supports all 17 publication languages, template/background/brand color selection, source selection for pairs, permitted single-image sizing/position controls and manual ordering. Debounced preview uses the selected language/device ratio and the same renderer as export, cancels stale requests and makes no AI call. Changed content hides stale downloads. Copy, layout and full vision regeneration are separate actions. Every new button, option, status, manual-mode label and editor caption has Chinese, English, Japanese, Korean and Spanish UI translations; language switching preserves edits.

The registry supports balanced, showcase, compact, detail and duo. Single screenshots remain the default. Detail uses a full unchanged capture plus an enlarged real crop. Duo uses a dominant full foreground capture and a subordinate, offset rear capture. Positions are normalized engine-owned tokens; compositions adapt to available space without stretching. Text gets a safe area; overly long copy is rejected instead of being shrunk to an unreadable size. A rear image in a deliberately layered pair is partly occluded; select a single layout if both complete screens must be visible at once.

The design review examined real store assets from [Canva](https://apps.apple.com/us/app/canva-ai-photo-video-editor/id897446215), [CapCut](https://apps.apple.com/us/app/capcut-photo-video-editor/id1500855883) and [Spotify](https://apps.apple.com/us/app/spotify-music-and-podcasts/id324684580). These are research references, not bundled assets or copied templates. The useful patterns were a dominant product view, concise copy close to the image, related operation/detail panels and consistent visual language; these apps do not universally use two complete phones on each slide. CapCut's public [Google Play listing](https://play.google.com/store/apps/details?id=com.lemon.lvoverseas) displayed a 1B+ install tier during review; no private iOS download counts are claimed.

Apple requirements checked 2026-10-28 against [official screenshot specifications](https://developer.apple.com/help/app-store-connect/reference/app-information/screenshot-specifications/) and [asset guidance](https://developer.apple.com/app-store/asset-best-practices/): accepted PNG/JPEG output, no transparency, 1–10 screenshots per relevant set. Device sizes remain in `store_screenshots/targets.json`; new designs read that registry, while existing archives retain their stored iPhone sizes. The [official DeepSeek vision protocol](https://api-docs.deepseek.com/guides/vision/) was also checked.

## Verification completed locally

Only `code-editor.png` and `terminal.png` were selected as real test inputs. Paid test credentials were read from ignored `test.md`; no credentials, profiles, downloaded references, generated outputs or caches are committed.

- Unit/regression suite: 44 discovered, 39 passed, five browser tests skipped by default. Covers existing behavior, JSON/schema failures and repairs, filename/locale/template compatibility, PNG/JPEG/WebP, cache hits/refresh/expiry/corruption, factual-evidence requirements, independent copy/layout behavior, all 17 publication languages, all six device groups, text safety and 17 Linux pixel baselines.
- SDK fault injection uses the real OpenAI SDK with HTTPX MockTransport: 429/503 retries, timeout, connection failure, 401 without retries, recovery after a 429, JSON response request and bounded token output. Submitted credentials are absent from user-facing errors.
- Dedicated Chromium suite: four tests passed, one live test skipped. Covers no-key manual editing, English/Chinese editing, detail/duo selection, order changes, mobile overflow, light/dark logo loading, ZIP download, malformed-JSON failure followed by manual design, all five interface languages with edits retained, and styled project documentation pages.
- Opt-in live Chromium test: passed with real DeepSeek Flash joint analysis of the two captures, a separate text-only copy request, local layout recommendation, editing, preview and 28 validated PNGs. Editor/terminal recommendations differ (compact/showcase); no browser JavaScript errors were recorded.
- Live single-image analysis and a cache replay with the model function disabled: passed, using the same code-editor input. A real response returned evidence as a list; canonicalization was added and tested rather than making another image-analysis call just to reformat it.
- Final composition export: two captures × two languages × 21 iPhone/iPad portrait/landscape resolutions = 84 RGB/sRGB PNGs. Dimensions, ZIP count/CRC and byte-for-byte original SHA-256 checks passed. iPhone and both iPad contact sheets were visually inspected. The iPad composition test deliberately retains the same real phone captures; it does not establish native iPad capture coverage.
- Ruff, JavaScript syntax checks, repository-link/JSON checks and diff whitespace checks passed.

Local versions at the time of the review: Python 3.12, Pillow 13.0.0, OpenAI SDK 2.54.0, jsonschema 4.26.0 and Playwright 1.64.1. Chromium was run locally; the configured Windows/macOS CI matrix and other browsers were not run in this environment. Design quality and factual copy still benefit from human review; no claim of guaranteed App Store approval or exhaustive device coverage is made.

Local review artifacts are in ignored `test_outputs/`: `final-overview_2.png`, the iPad contact sheets, `final-app-store.zip`, `live-single-and-cache.json`, `browser-live-result.json` and `final-multidevice-export.json`.

## Repeat checks

```bash
python -m pip install -r requirements-dev.txt
python -m unittest discover -s tests -v
python -m playwright install chromium
SHOTNIMOTE_BROWSER_TEST=1 python -m unittest discover -s tests -p test_browser_workflow.py -v
# Explicit paid test; reads the local ignored test.md file:
SHOTNIMOTE_BROWSER_TEST=1 SHOTNIMOTE_LIVE_TEST=1 PYTHONPATH=tests python -m unittest test_browser_workflow.BrowserWorkflowTests.test_live_two_image_analysis_copy_layout_and_export -v
```

Regenerate pixel baselines only for an intentional, visually reviewed rendering change with `python tests/update_visual_baselines.py`. Never update expected hashes merely to hide a failing regression. Restart an already-running local service after updating Python code.

## Incremental preview and text updates

The editor queues affected screen indices and retains uncommitted indices across debounce, aborts and retries. The preview API validates these indices and renders them against the complete configuration, preserving numbering, localization and paired-source context. Global changes and ordering refresh the current preview set. Preview/export use the same renderer and character-coverage font selection; missing fonts or complex-script shaping report errors instead of missing-glyph artwork.

`nimoteshot/locales.json` is the catalog for 17 output languages. The local options API supplies that catalog to the output and copy-version selectors; the closed design schema, planner, manual placeholders and export support matching fields. Interface translations remain separate. New language versions added after planning receive editable placeholders and a notice.

The startup path verifies a project-specific private runtime credential before requesting an idle server's cooperative shutdown. Queued or running jobs prevent replacement; unverified listeners remain running while another loopback port is selected. Tests include real CLI subprocess replacement, cross-project preservation, preview races, all output-language selectors and validated 17-language PNG/ZIP exports.
