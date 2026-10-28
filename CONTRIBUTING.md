# Contributing / 参与贡献

Bug reports, documentation, translations and pull requests are welcome. Search
existing issues first; discuss large changes before implementation. Use the issue
templates for ordinary problems and [SECURITY.md](SECURITY.md) for vulnerabilities.
All participation follows the [Code of Conduct](CODE_OF_CONDUCT.md).

欢迎提交问题、文档、翻译和代码。先检索已有 Issue，较大的改动先讨论设计。
普通问题使用 Issue 模板；漏洞通过安全策略中的私密渠道报告。所有参与者遵守行为准则。

## Development / 开发

Fork the repository, clone your fork, and create a focused branch. Python 3.11+
is required. From the repository root:

Fork 仓库、克隆自己的副本，再创建独立分支。在项目根目录执行（Python 3.11+）：

```bash
python -m venv .venv
# Linux / macOS
. .venv/bin/activate
# Windows PowerShell: .venv\Scripts\Activate.ps1
python -m pip install -r requirements-dev.txt
python -m ruff check .
python -m unittest discover -s tests -v
python scripts/check_repository.py
python scripts/check_secrets.py --history
python -m pip_audit -r store_screenshots/requirements.txt
```

Tests mock provider calls: no paid account or real API key is needed. Dependency
auditing requires network access. Start the studio with
`python scripts/nimoteshot.py web`; there is no JavaScript build step.

测试模拟服务商调用，不需要真实密钥或付费账户。依赖审计需要联网。
运行上面的 web 命令即可启动工作台，无需 JavaScript 构建。

## Scope and quality / 范围与质量

- Put reusable Python in `nimoteshot/`, browser files in `web/`, commands and
  maintenance tools in `scripts/`, and tests in `tests/`.
- Follow `.editorconfig`. Ruff checks correctness rules; it does not require a
  wholesale reformat of the renderer. Keep unrelated formatting out of a fix.
- Add regression tests for behavior changes, especially URL validation, filesystem
  boundaries, credentials and provider adapters. Use synthetic captures.
- Update both README files for user-visible changes. Include before/after images
  for visual changes only after checking privacy and permission.
- Never commit keys, local profiles, private captures, generated runs or archives.
  Do not paste unredacted provider errors into issues.
- Add dependency and asset license notices with their source and redistribution
  permission. Do not copy code or assets with unknown or incompatible terms.

可复用代码、网页、命令和测试按上述目录归类。遵守编辑器配置，避免无关格式化。
行为变更应补回归测试，测试图片使用合成素材。用户可见变更同步维护中英文说明。
不得提交密钥、本地配置、私密截图和生成归档；新增依赖与素材必须有可核验授权。

## Pull requests / 提交合并请求

Use a focused title, explain the problem and resulting behavior, link related
issues and record checks run. Submit a PR from your fork to the default branch.
A maintainer reviews correctness, safety, licensing and tests; contributors do not
need repository write access. Address review comments before merge. Draft PRs are
welcome. CI runs on fork PRs without provider credentials.

PR 应说明问题、修改后的行为、关联 Issue 和验证结果。提交到默认分支，由维护者
检查正确性、安全性、授权与测试。外部贡献者无需仓库写权限；欢迎草稿 PR。

## Contribution license / 贡献授权

By submitting an original contribution for inclusion, you agree to license it
under the [GNU Affero General Public License v3.0 or later](LICENSE) and confirm you have the right to submit it. You keep your
copyright; no copyright assignment or separate CLA is required. Identify imported
third-party material and retain its original notices.

提交原创贡献即表示你有权提交并同意按本项目 GNU Affero General Public License v3.0 或更高版本授权；你保留版权，无需版权转让或额外 CLA。
引入第三方材料须标明来源并保留原授权。
