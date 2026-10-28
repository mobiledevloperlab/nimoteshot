# NimoteCode 十张图片设计记录与复现指令

当前为单张编辑器主视觉的最终上传序列。8 张使用中的原图及哈希清单保留在此示例目录中；未使用的插件原图、旧草稿和修订已移除。

## 第一张设计

- 标题：Your IDE. / Anywhere.
- 副标题：Editor · SSH · AI · Git · Terminal。能力由后续真实截图支持。
- 主视觉：仅使用 `code-editor.png` 编辑器真实截图，裁切区域由 `config.json` 的 `crop` 参数定义；代码与菜单未重绘或修改。
- 布局：浅暖灰背景、统一圆角、单张居中界面；无悬浮装饰卡片。

## 全套排版

- 前三张：IDE 能力概览 → SSH → AI。
- 单项截图水平居中；Inter Bold 标题 116 px、行距 128 px；Inter Regular 副标题 62 px（均按画布宽度缩放）。
- 背景为浅暖灰、冷灰和淡玫红；截图容器圆角为画布宽度的 3.1%。
- 第 8 张从编辑器原图裁切，突出真实代码导航菜单。

## 十张图与文案

| 序号 | 原图 | 主标题 | 副标题 |
|---|---|---|---|
| 01 | `code-editor.png` | Your IDE. / Anywhere. | Editor · SSH · AI · Git · Terminal |
| 02 | `ssh-workspace.png` | Code over / SSH. | Remote files. Real work. |
| 03 | `ai-assistant.png` | Ask AI about / your code. | Reads your project files. |
| 04 | `code-editor.png` | Code on / your phone. | Edit real projects. |
| 05 | `source-control.png` | Git at a / glance. | Changes and history. |
| 06 | `terminal.png` | A terminal / for touch. | Commands at hand. |
| 07 | `workspaces.png` | Choose your / workspace. | Local or remote projects. |
| 08 | `code-editor.png` | Navigate / your code. | Definitions and references. |
| 09 | `diagnostics.png` | Find issues / as you code. | LSP diagnostics in context. |
| 10 | `settings.png` | Make it / yours. | Theme, language, scale. |

## 一键复现

```bash
python -m pip install -r store_screenshots/requirements.txt
python scripts/generate_store_screenshots.py --config demo/nimotecode/config.json --all
```

此目录仅保留原图、配置、清单和一张十图总览；旧的多轮导出已从仓库移除。新应用请使用 NimoteShot 网页或命令行入口。
