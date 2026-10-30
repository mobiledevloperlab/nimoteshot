<p align="center">
  <img src="web/assets/nimoteshot-logo.svg" alt="NimoteShot" width="320">
</p>

# NimoteShot — 开源 AI 应用商店截图生成器

**真实界面，文案可改，多语言截图在本地导出。**

把自己的应用截图，制作成适用于 **App Store 和 Google Play** 的上架素材。让视觉模型起草卖点，在实时编辑器中调整文案与布局，再导出 iPhone、iPad、Android 所需的图片。适合准备发布应用的独立开发者与产品团队。

**Python 3.11+ · Linux / macOS / Windows · 17 种输出语言 · AGPLv3+**

[English](README.md) · 简体中文 · [日本語](README.ja.md) · [한국어](README.ko.md) · [Español](README.es.md)

[快速开始](#快速开始) · [查看效果](#从真实界面到上架素材) · [语言支持](#语言支持) · [参与共建](#参与共建)

![NimoteShot 实时截图编辑器：在标题中编辑中英混排文字，旁边同步显示 App Store 截图预览](web/assets/redefine_promotion.png)

*直接在结果旁修改标题、副标题和布局，只重新渲染受影响的预览，无需再次调用 AI。上图为实际运行中的编辑界面。*

## 为什么使用 NimoteShot？

- **从你的真实产品开始。** 上传 PNG、JPEG、WebP 界面截图，模型依据可见功能起草文案，使用原始界面制作宣传图。
- **生成后仍能自由调整。** 文案、模板、品牌色和顺序均可编辑。自动预览，失败可重试，确认效果后再导出。
- **一次准备多个市场和设备。** 可选 17 种语言版本及六组设备／方向组合；内置字体支持中英混排和常见文字体系。
- **按自己的方式使用。** 网页和 CLI 共用流程。手动设计无需密钥，AI 分析可选云端或本地视觉模型，渲染和 ZIP 打包在本地完成。

NimoteShot 是免费、开源的软件；云端模型服务商可能单独收取 API 费用。

## 快速开始

安装 **Python 3.11 或更新版本**，然后克隆项目：

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

安装脚本会创建 `.venv`、安装依赖并启动工作台。打开**终端实际输出的地址**，默认是 `http://127.0.0.1:8765`。

想先体验编辑器，可选择 **手动设计**，无需模型密钥。使用 AI 起草文案时，选择服务商、配置凭据，再点击 **检查模型配置**。

<details>
<summary>手动安装、更新与启动选项</summary>

```bash
python -m venv .venv
# Linux / macOS：
. .venv/bin/activate
# Windows PowerShell：
# .venv\Scripts\Activate.ps1
python -m pip install -r store_screenshots/requirements.txt
python scripts/nimoteshot.py web
```

更新代码后，重新安装依赖并重启服务。`--no-browser` 可关闭自动打开浏览器，`--port 8766` 可指定首选端口。

端口被占用时，程序会验证是否为本项目的旧服务。已验证且空闲的服务会正常退出并重启；有任务的服务、其他程序和不支持验证的旧版本会保留，新服务自动换用本地空闲端口，不会强杀进程。

</details>

## 从真实界面到上架素材

1. **添加产品信息。** 填写应用名称、功能简介或公开 HTTPS 网站，上传 1–40 张真实界面截图。
2. **选择输出方向。** 勾选语言、设备尺寸和设计风格，使用 AI 分析或手动设计。
3. **预览与微调。** 分别编辑各语言版本，调整模板并查看效果。修改文案或单张布局只更新对应截图；全局修改刷新当前预览集。
4. **导出 PNG / ZIP。** 下载经过校验的多分辨率 RGB/sRGB 图片，以及可继续编辑的任务配置。

| 原始应用界面 | 生成的商店截图 |
| --- | --- |
| <img src="demo/nimotecode/originals/code-editor.png" alt="NimoteCode 移动代码编辑器原始截图" width="220"> | <img src="demo/nimotecode/previews/01_feature.png" alt="基于真实代码编辑器界面生成的 App Store 宣传截图" width="220"> |

[查看 NimoteCode 完整示例](demo/nimotecode/)，了解更多原图与生成效果。

### 继续调整，无需从头生成

**编辑语言版本** 用于选择独立保存的文案。切换语言会显示对应版本；字体按实际文字选择，因此英文栏也能直接输入中文。需要更多版本时，在 **产品信息** 中勾选输出语言。方案生成后新增的语言会填入占位文案，并提示先编辑或重新生成文案。

可选调整均说明作用范围：**重新生成文案** 复用视觉证据，重写所选语言的文案；**重新推荐布局** 在本地重选模板，保留文案；**重新分析截图** 再次调用视觉模型，替换整套设计。

## 语言支持

输出选择、语言版本切换、AI 提示词、预览和导出使用同一份 **17 种语言目录**：

| 分组 | 可选输出语言 |
| --- | --- |
| 英语与东亚语言 | 英文、简体中文、繁体中文、日文、韩文 |
| 欧洲与美洲语言 | 西班牙文、法文、德文、巴西葡萄牙文、俄文、希腊文 |
| 南亚与东南亚语言 | 印地文、孟加拉文、越南文、泰文 |
| 中东语言 | 阿拉伯文、希伯来文 |

英文默认包含，其他版本按需勾选。**操作界面**支持英文、简体中文、日文、韩文和西班牙文。

应用名称、标题和副标题按实际字符选择内置字体，预览与导出共用同一套文字渲染。输入法组词完成后才触发更新。复杂文字使用 [Pillow 的 libraqm 排版能力](https://pillow.readthedocs.io/en/stable/reference/ImageFont.html)；缺少排版能力或字体无法覆盖的字符组合会明确提示，避免静默显示缺字方框。

部分 macOS/Windows 的 Pillow 安装需要单独配置 FriBiDi 才能处理复杂文字。工作台会禁用缺少排版能力的语言并提供配置入口，英文、中日韩等受支持文字仍可正常使用。可用 `python -c "from PIL import features; print(features.check('raqm'))"` 检查，按 [Pillow 安装指南](https://pillow.readthedocs.io/en/stable/installation/building-from-source.html)启用后重启服务。

## 格式与设计

| 能力 | 支持范围 |
| --- | --- |
| 输入 | 1–40 张 PNG、JPEG、WebP，可归组为最多 10 张功能宣传图 |
| 设备 | iPhone、iPad、Android，均支持竖屏与横屏 |
| 设计 | 4 套基础风格、24 套分类配色、设计提示词与可编辑模板 |
| 预览 | 本地渲染、局部更新、旧请求结果保护与失败重试 |
| 导出 | 多分辨率 PNG、sRGB 色彩配置、ZIP 完整性校验与可编辑配置 |
| 可追溯 | 每次任务保留原图及 SHA-256 源文件清单 |

任务保存于 `store_screenshots/runs/<任务ID>/`。具体尺寸见[输出规格](store_screenshots/targets.json)。上架前请审阅文案，并核对最新的 [Apple 截图规范](https://developer.apple.com/help/app-store-connect/reference/app-information/screenshot-specifications/) 与 [Google Play 图片要求](https://support.google.com/googleplay/android-developer/answer/9866151)。

## 模型服务商

可选 DeepSeek（默认）、通义千问、智谱 GLM、火山方舟、腾讯混元、OpenAI 兼容 API、Gemini、Claude、Ollama 和已登录的 Codex CLI。可用性取决于具体模型与账号权限；工作台提供配置及连接检查，[模型预设](nimoteshot/models.json)是配置依据。

分析截图需选择**具备视觉理解能力的模型**。手动编辑与导出不调用模型。云端凭据可通过工作台、环境变量或本地配置档案设置，详见[服务商配置说明](docs/PROVIDERS.md)。

## 命令行使用

把截图放入 `screens/`，配置服务商后生成：

```bash
.venv/bin/python scripts/nimoteshot.py configure \
  --provider qwen --prompt-api-key --verify

.venv/bin/python scripts/nimoteshot.py generate \
  --brand "My App" \
  --description "支持 SSH、Git 和终端的移动编辑器" \
  --provider qwen --style editorial --locales zh-CN,fr-FR,ja-JP
```

Windows 请将 `.venv/bin/python` 换为 `.venv\Scripts\python.exe`。完整语言 ID 与选项见 `python scripts/nimoteshot.py generate --help`。编辑配置后，可直接在本地重新渲染：

```bash
python scripts/generate_store_screenshots.py \
  --config store_screenshots/runs/<任务ID>/config.json --all
```

## 隐私与常见问题

网页服务仅监听本机回环地址。渲染在本地完成，**AI 分析会将截图和产品上下文发送给你选择的服务商**；填写网站时会读取该公开页面。工作台输入的密钥保留在页面内存中，只有主动保存配置时才写入用户配置目录；保存的配置为明文文件。请将任务目录和 ZIP 视为私有数据。

| 问题 | 处理方法 |
| --- | --- |
| 缺少 Python 或 `venv` | 安装包含 pip、venv 的 Python 3.11+，再运行安装脚本。 |
| 服务商拒绝密钥或模型 | 核对账号授权、模型 ID 与接口地址，再检查模型配置。 |
| 预览失败或文字过长 | 缩短文案或调整布局，查看预览提示后重试；也可使用手动设计。 |
| 页面仍是旧版或缺少新增语言 | 更新依赖、重启服务，并在新标签页打开终端输出的地址。 |
| 端口已被占用 | 程序会验证空闲旧服务或自动换端口，以实际输出的地址为准。 |

仅上传有权发送的截图，发布前复核 AI 生成的功能描述与翻译。不要提交密钥或私有截图。威胁模型及漏洞反馈渠道见[安全策略](.github/SECURITY.md)。

## 参与共建

你可以从这些具体事情开始：

- **用自己的应用试一遍。** [报告可复现的问题](https://github.com/mobiledevloperlab/nimoteshot/issues/new/choose)，附操作步骤或命令、预期结果及已脱敏的错误信息。
- **完善一种语言或版型。** 帮助检查翻译、字体、设备尺寸与模板，较大的改动先通过 Issue 讨论。
- **贡献代码或文档。** Fork 项目后提交范围清晰的 PR。[贡献指南](.github/CONTRIBUTING.md)包含环境配置、检查和评审方式，欢迎 Draft PR。

```bash
python -m pip install -r requirements-dev.txt
python -m ruff check .
python scripts/run_tests.py
python scripts/check_repository.py
```

默认测试使用合成素材或仓库示例，并模拟模型调用；真实服务商测试需显式启用。浏览器与视觉回归覆盖编辑、语言切换、预览及导出。更多信息见[架构与验证](docs/VISION_UPGRADE.md)、[更新日志](docs/CHANGELOG.md)、[治理规则](docs/GOVERNANCE.md)及[行为准则](.github/CODE_OF_CONDUCT.md)。

## 许可证

NimoteShot 采用 [GNU Affero General Public License v3.0 或更高版本](LICENSE)（`AGPL-3.0-or-later`）。你可以在许可证约定下使用、研究、修改和分享。通过网络提供修改版时，需按许可证要求提供对应源码。字体及其他第三方素材保留原有授权，见[第三方声明](docs/THIRD_PARTY_NOTICES.md)。
