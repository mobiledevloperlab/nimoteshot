# NimoteCode demo / 示例

This isolated demo shows the original iPhone portrait design language that inspired NimoteShot. It contains real captures, their SHA-256 manifest, a bilingual config, and one contact sheet. Old exports and revision archives are omitted to keep the source repository small.

此独立示例展示 NimoteShot 参考的 iPhone 竖屏设计语言，保留真实原图、哈希清单、双语配置和一张总览图。旧的全尺寸导出与历史修订已移除。

- [Config / 配置](config.json)
- [Sample preview / 示例预览](previews/01_feature.png)
- [Design record / 设计记录](GENERATION_PROMPT.zh-CN.md)

To render the demo manually / 手动重新渲染示例：

```bash
python scripts/generate_store_screenshots.py --config demo/nimotecode/config.json --all
```

## Rights / 权利范围

These captures show NimoteCode and are not automatically covered by the source
code license. This checkout does not contain a verifiable redistribution grant
for the UI captures and embedded third-party content. Before public release,
record the owner's permission and inspect every image for private data, or replace
the images with synthetic, permissively licensed captures and update the manifest
and demo configuration. See [the audit](../../docs/OPEN_SOURCE_AUDIT.md).

截图不自动适用源码许可证。当前仓库未附 UI 截图及其内含第三方内容的可核验再分发授权。
公开前应记录权利人许可并逐张排查隐私，或替换为宽松授权的合成截图，同步清单与示例配置。
