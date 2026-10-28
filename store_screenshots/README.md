# Rendering reference

[Project setup](../README.md) · [中文说明](../README.zh-CN.md)

The studio generates task IDs automatically. The renderer reads a `config.json` and exports each target size directly from archived originals. It checks source hashes, image dimensions, RGB mode and the embedded sRGB profile.

```bash
python scripts/generate_store_screenshots.py --config demo/nimotecode/config.json --target iphone_portrait --locale zh-CN --size 1320x2868
```

Use `--all` for every configured target and both languages; `--preview` builds contact sheets; `--validate` checks existing exports. A screen can provide `target_files` for native device captures and `localizations.zh-CN.screens` for Chinese copy or Chinese UI captures. [targets.json](targets.json) contains device size presets. [styles.json](../nimoteshot/styles.json) contains the selectable design presets.

The demo lives in [demo/nimotecode](../demo/nimotecode/) and is kept outside normal task output. Newly generated runs go to `store_screenshots/runs/`.
