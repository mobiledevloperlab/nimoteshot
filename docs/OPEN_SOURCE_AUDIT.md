# Publication readiness audit / 源码公开准备审计

Date: 2026-10-28. Baseline: `b79346f`. Scope: tracked source, web UI,
installation scripts, documentation, workflows, bundled asset metadata and
reachable local Git history. This is an engineering review, not a certification
of ownership or a guarantee that no vulnerability exists.

审计范围：已跟踪源码、网页、安装脚本、文档、工作流、素材元数据及本地可达 Git 历史。
这是工程审查，不是权属认证或“绝无漏洞”的保证。

## Licensing decision / 授权决定

The owner selected the **GNU Affero General Public License v3.0 or later**
(`AGPL-3.0-or-later`) for project-owned code and documentation. NimoteShot is
fully open source and free to use, modify, and distribute under that license.
Modified versions distributed to others or offered for network interaction must
provide corresponding source under AGPLv3+. Contributors keep their copyrights;
there is no automatic copyright assignment or blanket relicensing right for a
maintainer over other contributors' work.

所有者为自有代码和文档选择 **GNU Affero General Public License v3.0 或更高版本**
（`AGPL-3.0-or-later`）。NimoteShot 是完全开源、可免费使用、修改与分发的软件。向他人
分发修改版或将其作为网络服务提供时，必须依 AGPLv3+ 提供对应源码。贡献者保留版权，不存在
自动版权转让或维护者可任意重新授权他人贡献的条款。

AGPLv3 is an OSI-approved free and open-source license. Third-party fonts and
installed dependencies retain their original terms; see [notices](THIRD_PARTY_NOTICES.md).

AGPLv3 是 OSI 认可的自由及开源许可证。字体和依赖保留各自的原授权，详见[第三方声明](THIRD_PARTY_NOTICES.md)。

## Findings and changes / 发现与修复

| Area / 领域 | Finding and disposition / 发现及处理 |
| --- | --- |
| Community | Expanded bilingual contribution, conduct, security and governance policies; PR licensing declaration; changelog and release checklist. |
| CI | Read-only token, checkout credentials disabled, verified action commit pins, time limits; Python 3.11/3.12 on Linux/macOS/Windows; lint and repository checks. |
| Dependencies | Audit flagged Pillow 12.2.0; upgraded to 13.0.0. Runtime and development dependency audits then reported no known vulnerabilities. Python minimum raised to 3.11 to match Pillow metadata. |
| Supply chain | Dependabot for Python and Actions, recurring vulnerability audits of runtime and development requirements, text secret scanning including reachable Git blobs. |
| Local HTTP | Host allowlist on reads/writes prevents arbitrary rebinding hostnames; Origin/Fetch-Site checks; non-loopback binding refused; malformed JSON and lengths return client errors. |
| Provider URLs | Ollama URLs parsed by authority rather than prefix; credentials, path, query and fragment rejected. |
| Credentials | Private temporary file created before writing keys; atomic replacement; failed writes preserve existing config and do not overwrite symlink targets. |
| Assets | OFL files retained; missing embedded font copyright notices added. ICC metadata states “No copyright, use freely”. Demo broken preview link corrected. |
| Hygiene | Local input/output and credential file ignore rules; JSON, local Markdown links and demo SHA-256 integrity checks. |

## Remaining publication gates / 仍需落实的公开前置条件

1. **Demo authorization and privacy.** Original and preview images are tracked.
   Their manifest proves integrity, not permission. There is no recorded grant for
   embedded app UI/third-party content and no completed image-by-image privacy review.
   The owner must record the relevant permission and review the pixels, or replace
   them with synthetic captures. Include history in the decision. Font rights do
   not establish rights to the screenshots.
2. **Hosting controls.** `git remote -v` is empty. No GitHub setting has been changed
   or verified: private reporting, moderation contact, branch protections, required
   checks, alerts and contributor workflow approval remain launch tasks. See
   [RELEASING](RELEASING.md). Local policy files cannot enable these controls.
3. **Platform and live provider smoke tests.** Local verification uses Linux and
   mocked providers. Committed CI defines other platforms; those jobs have not run
   here. No paid external inference or Windows/macOS installer execution is claimed.

1. **示例素材授权与隐私**：哈希不是授权证明。需记录截图及内含第三方内容的再分发许可并
   逐张核验隐私，或替换为合成素材，同时处理将发布的 Git 历史。暂不称“可无条件发布”。
2. **托管平台控制**：没有远程仓库，未配置/验证 GitHub 私密报告、投诉渠道、分支保护、
   必需检查及安全功能。文件补齐不等于平台开关已经生效。
3. **平台与真实接口验证**：本地使用 Linux 与模拟接口，尚未实际执行远程 CI、其他平台
   安装器和付费推理。

## Known technical limits / 已知技术边界

- No multi-user authentication or quotas; do not expose the local service publicly.
- Website DNS validation and connection are separate operations; public-site input
  is not a complete SSRF defense against DNS changes. Only use trusted URLs.
- Secret scanning covers recognizable provider credentials/private keys/basic-auth
  patterns in UTF-8 text. Generic keyword and entropy detectors are disabled to
  avoid source literals and asset hashes; images, arbitrary secrets, unreachable
  Git objects and external hosting state require separate review.
- Dependency versions are not a fully hashed transitive lock. CI audits resolutions;
  packaged releases need an exact component/license inventory for their platform.
- Saved credentials are plaintext; Windows permissions depend on user directory
  ACLs. Review provider error messages and generated artifacts before sharing.

服务没有多用户认证及配额；网站 DNS 检查不能完全防御 DNS 变化；密钥扫描无法证明图片和
任意字符串没有秘密；依赖尚无全部传递版本与哈希锁定；Windows 凭证依赖用户目录权限。
这些边界均要求按本机单用户工具使用，而不是部署成公网服务。

## Verification / 验证

Final local results are recorded below after executing the checks. Findings are
point-in-time results, not future guarantees. Security automation deliberately
fails on newly reported vulnerable dependencies rather than silently ignoring them.

最终本地验证结果见下文，扫描只代表执行时点，不保证未来没有新增漏洞。

| Local check / 本地检查 | Result / 结果 |
| --- | --- |
| `python scripts/run_tests.py` | Unit and regression tests run without provider credentials; CI failures include their traceback in the check annotation. |
| `python -m ruff check .` | Passed. Correctness rule subset, not a full security analyzer. |
| `python scripts/check_repository.py` | 0 errors: required files, JSON, local Markdown links, tracked private-file policy and demo hashes. |
| `python scripts/check_secrets.py --history` | 0 findings in working-tree text and reachable history under the documented detectors; not a privacy clearance for images. |
| `python -m pip_audit -r store_screenshots/requirements.txt` | No known vulnerabilities in the resolved runtime dependencies after Pillow upgrade. |
| `python -m pip_audit -r requirements-dev.txt` | No known vulnerabilities in the resolved development dependencies. |
| `sh -n install.sh` / `node --check web/app.js` | Syntax checks passed; not an installer/UI end-to-end test. |
| `git diff --check` | Passed. |

Reference practices: [GitHub Actions security](https://docs.github.com/en/actions/reference/security/secure-use)
and [private vulnerability reporting](https://docs.github.com/en/code-security/how-tos/report-and-fix-vulnerabilities/report-privately).
