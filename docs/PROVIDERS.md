# Provider setup / 模型服务商配置

[English README](../README.md) · [中文 README](../README.zh-CN.md)

Choose a provider in the studio, select a vision-capable model and run **Check model configuration**. Enter a key in the page for the current session, use an environment variable, or explicitly save a local profile. Model names and endpoints are defined in [models.json](../nimoteshot/models.json); account access and provider availability can change.

在工作台中选择服务商和具备视觉理解能力的模型，再检查模型配置。密钥可在页面临时输入、通过环境变量提供，或主动保存为本地配置。模型与接口预设以代码中的配置文件为准，账号权限和服务商可用性可能变化。

| Provider | ID / 环境变量 | Setup / 配置 |
| --- | --- | --- |
| DeepSeek | `deepseek` / `DEEPSEEK_API_KEY` | Default provider; select an enabled vision model. 默认服务商，选择已获授权的视觉模型。 |
| Qwen / 通义千问 | `qwen` / `DASHSCOPE_API_KEY` | Use a Model Studio key with access to the selected model. 使用有对应模型权限的百炼密钥。 |
| Zhipu GLM / 智谱 | `zhipu` / `ZAI_API_KEY` | Check model access and the API base URL. 核对模型权限与接口地址。 |
| Volcengine Ark / 火山方舟 | `doubao` / `ARK_API_KEY` | Provide an enabled vision model or endpoint ID. 填写已开通的视觉模型或接入点 ID。 |
| Tencent Hunyuan / 腾讯混元 | `hunyuan` / `HUNYUAN_API_KEY` | Use the configured TokenHub endpoint and an enabled vision model. 使用预设 TokenHub 接口和已开通的视觉模型。 |
| OpenAI | `openai` / `OPENAI_API_KEY` | Requires API access to the selected vision model. 需要所选视觉模型的 API 使用权限。 |
| Gemini | `gemini` / `GEMINI_API_KEY` | Select a supported vision model. 选择支持图像理解的模型。 |
| Claude | `claude` / `ANTHROPIC_API_KEY` | Select a supported vision model. 选择支持图像理解的模型。 |
| OpenAI-compatible API | `compatible` / `NIMOTESHOT_API_KEY` | Supply the model ID and an HTTPS API base URL. 填写模型 ID 与 HTTPS API 基础地址。 |
| Ollama | `ollama` / no cloud key | Run `ollama serve` and install the chosen local vision model. 启动本地服务并安装所选视觉模型。 |
| Codex CLI | `codex` / signed-in CLI | Install and sign in to the CLI. NimoteShot uses its local integration. 安装并登录 CLI，由本地集成调用。 |

## Store a profile / 保存配置

```bash
.venv/bin/python scripts/nimoteshot.py configure \
  --provider qwen --prompt-api-key --verify

.venv/bin/python scripts/nimoteshot.py doctor --provider qwen
```

On Windows, use `.venv\Scripts\python.exe`. Prompting for the key avoids putting it in shell history. Profiles live outside the repository:

- Linux / macOS: `~/.config/nimoteshot/config.json` (or under `XDG_CONFIG_HOME`).
- Windows: `%APPDATA%\NimoteShot\config.json`.

Saved keys are plaintext at rest; Unix profile files are owner-only. The UI does not return server-held keys to the browser. API access is separate from a consumer chat subscription, and cloud API charges follow your provider's terms. Review account access before analyzing private captures.

Windows 请使用 `.venv\Scripts\python.exe`。交互输入可以避免密钥进入命令历史；保存的密钥仍为明文，Unix 配置文件仅所有者可读写。服务端已有密钥不会回传浏览器。API 权限与消费级聊天订阅并不等同，云端费用以服务商规则为准。发送私有截图前请确认授权与权限。

Manual design, preview editing and export need no model key. See the [security policy](../.github/SECURITY.md) for credential and local-service boundaries.

手动设计、编辑预览与导出无需模型密钥。密钥管理与本地服务边界见[安全策略](../.github/SECURITY.md)。
