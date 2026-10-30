# Changelog / 变更日志

## Unreleased

- Detect optional Raqm/FriBiDi support before enabling complex-script output, preserve UTF-8 diagnostics on Windows, and avoid reverse-DNS waits during loopback startup.
- 在启用复杂文字输出前检测可选排版能力，保持 Windows 日志的 UTF-8 输出，并避免本机服务启动时等待反向 DNS 查询。

- Add 17 output-language versions shared by the picker, closed copy schema, AI prompts, preview and PNG/ZIP export. Select fonts by actual Unicode coverage and support IME composition; bundle licensed fonts for additional major writing systems.
- Render only affected previews for per-screen edits, preserve pending changes across interrupted requests, group optional rework controls, and safely restart verified idle studios or choose an available local port.
- Rebuild the five READMEs around the real live-editing demo, quick start and contribution paths; keep provider setup in a separate guide.
- 将输出选择、受限文案 Schema、AI 提示词、预览及 PNG/ZIP 导出统一为 17 种语言版本；按实际字符选择字体，支持输入法组词，并补充具备授权的常用文字字体。
- 单张编辑仅更新受影响预览，保留被中断请求的待更新内容，归并可选重做操作；安全重启已验证的空闲旧服务，或自动选择本地空闲端口。
- 五份 README 改为以真实编辑演示、快速开始和共建入口为中心，详细模型配置独立成文。

- Complete the DeepSeek Flash vision → validated design → deterministic preview/export workflow, with bounded JSON cache reuse, independent copy/layout actions and five-language editing.
- Add shared capture validation, safe template tokens, refined detail/paired layouts, text readability limits, multi-device ZIP completeness checks and Chromium/visual/fault-injection coverage.
- Replace DiskCache after its unsafe-pickle disclosure with an atomic, size-bounded JSON cache; update CI actions to Node 24 and keep exact pixel baselines on their Linux reference platform.
- Remove unused optional review briefs from `prompts/`; runtime prompts remain in the application.
- 完善 DeepSeek Flash 视觉分析、Schema 设计校验、本地预览与导出链路，增加有界缓存、独立文案／布局操作和五语言编辑。
- 补齐图片校验、受限模板、特写／双图构图、文字可读性保护、多设备 ZIP 校验及浏览器／视觉／异常测试；移除未使用的人工复核说明目录。
- 针对 DiskCache 的不安全 pickle 公告，改用原子写入且限制容量的 JSON 缓存；CI Actions 升级至 Node 24，精确像素基线限定在 Linux 参考平台。

- Re-license project-owned code and documentation under GNU AGPLv3 or later, making NimoteShot fully open source and free to use, modify, and share. Modified versions offered as network services must provide corresponding source under AGPLv3+.
- 将自有代码和文档改为 GNU AGPLv3 或更高版本：NimoteShot 现为完全开源、可免费使用、修改与分享的软件；以网络服务提供修改版时，须依 AGPLv3+ 提供对应源码。

## v1.3.0 — 2026-10-28

- Adopt a noncommercial share-alike source-available license for original contributions; replace the unpublished MIT draft and retain third-party notices.
- Document contribution, governance, security and release procedures in English and Chinese.
- Harden local HTTP access, request validation, Ollama URLs and credential file writes.
- Add lint, repository hygiene, dependency auditing and dependency update automation.

- 原创贡献采用非商业同条件共享源码可用许可证，替换未发布的 MIT 草案，保留第三方声明。
- 补齐双语贡献、治理、安全和发布流程。
- 加固本地 HTTP 访问、请求校验、Ollama 地址和凭证写入。
- 增加静态检查、仓库检查、依赖审计与更新自动化。

- Upgrade Pillow to 13.0.0 to address dependency audit findings. **Breaking:** Python
  3.11+ is now required by Pillow; recreate Python 3.10 virtual environments.
- 将 Pillow 升级至 13.0.0 以修复依赖审计发现。**不兼容变更**：Pillow 要求 Python
  3.11+；旧 Python 3.10 虚拟环境需重新创建。

- Rename the product to NimoteShot, the Python package and CLI to `nimoteshot`,
  and the custom provider credential to `NIMOTESHOT_API_KEY`. Local configuration,
  browser preference keys and new export names now use the new name. Existing
  local profiles are not automatically migrated; configure the provider again.
- 项目统一更名为 NimoteShot，Python 包和 CLI 使用 `nimoteshot`，自定义接口环境变量
  使用 `NIMOTESHOT_API_KEY`。本地配置目录、浏览器偏好键和新导出名称同步更新；既有本地
  配置不自动迁移，需重新配置服务商。

- Simplify the studio to open sections, underlined fields and linear selection
  markers; retain keyboard focus, light/dark themes and mobile navigation.
- 工作台改为无轮廓容器、底线表单和线性选中标记，保留键盘焦点、明暗主题与移动端导航。

- Add subtle header/footer dividers and localized footer links to usage,
  contribution, security, licensing and third-party notices. Serve only explicitly
  approved public documents as UTF-8 text from the local studio.
- 添加标题栏与页脚细分隔线，以及多语言使用、贡献、安全、授权和第三方声明入口。
  本地工作台仅开放白名单内的公开文档，并以 UTF-8 纯文本展示。
