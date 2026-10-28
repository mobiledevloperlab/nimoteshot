# Publication and release checklist / 公开与发布清单

## Before making the repository public / 首次公开前

- [ ] Confirm all project-owned contributions may be licensed under the current
  [LICENSE](../LICENSE). The owner has confirmed the previous MIT draft was never
  publicly released. Keep evidence for any separately supplied third-party code.
- [ ] Resolve the demo capture rights and privacy gate in the [audit](OPEN_SOURCE_AUDIT.md).
  If replacing captures, update configs, previews and SHA-256 manifest together.
  Review reachable Git history too: removing a file from HEAD does not remove it
  from published history. Do not publish unresolved assets through old commits.
- [ ] Configure the canonical remote and public repository description. Describe
  this as **fully open source under AGPLv3+**. Verify that GitHub detects the
  `AGPL-3.0-or-later` license correctly.
- [ ] Enable private vulnerability reporting under Settings → Security. Verify the
  “Report a vulnerability” route as a non-maintainer. Publish an actual private
  moderation contact in `.github/CODE_OF_CONDUCT.md`.
- [ ] Protect the default branch: require PR review by at least one maintainer,
  dismiss stale approvals, require resolved conversations and successful CI/test
  matrix plus Security/audit. Block force pushes and deletion. Review admin bypass.
- [ ] Enable dependency graph, Dependabot alerts/security updates, secret scanning
  and push protection where available. Verify the committed Dependabot config runs.
- [ ] Keep workflow token permissions read-only, require approval for outside
  contributors' workflows, and do not expose secrets or self-hosted runners to PRs.
- [ ] Set the actual maintainer/team in CODEOWNERS if review routing is desired.
  No fake account or placeholder ownership rule is shipped in this checkout.

首次公开前：确认全部自有贡献的授权权限；核验示例素材与隐私（包括 Git 历史）；配置正式
远程仓库；准确标为“AGPLv3+ 完全开源”；确认 GitHub 正确识别 `AGPL-3.0-or-later`；启用私密漏洞报告并公布行为投诉私密渠道；开启分支
保护、PR 审核、状态检查和可用的依赖/密钥安全功能；外部 PR 不提供密钥或自托管运行器。
CODEOWNERS 只能填写真实维护者或团队，不用占位账号假装已配置。

## Every release / 每次发布

```bash
python -m pip install -r requirements-dev.txt
python -m ruff check .
python scripts/check_repository.py
python scripts/check_secrets.py --history
python scripts/run_tests.py
python -m pip_audit -r store_screenshots/requirements.txt
python -m pip_audit -r requirements-dev.txt
```

- [ ] Inspect dependency changes and licenses, including native libraries if bundling
  wheels. Resolve audit findings rather than adding blanket ignores.
- [ ] Verify install.sh on Linux/macOS and install.ps1 on Windows from a clean clone.
  Run the web UI and CLI; use synthetic images and trusted providers for smoke tests.
- [ ] Wait for all platform/Python CI jobs. Local Linux results alone do not verify Windows.
- [ ] Update CHANGELOG and both READMEs; state breaking changes and known limitations.
- [ ] Tag the reviewed commit using a semantic version. Create release notes with
  source access, license, changes and checksums for any artifacts. Include LICENSE,
  THIRD_PARTY_NOTICES and bundled font notices in distributions.
- [ ] If distributing executables or offering a modified network service, comply
  with the corresponding-source obligations in LICENSE.

每次发布均运行上述检查，核验依赖许可证、干净安装及跨平台 CI；更新双语文档和变更日志，
只为已审核提交打版本标签。发布包附完整许可证与第三方声明；分发可执行文件或提供网络服务
须履行对应源码义务。不要将本地检查结果当成已经完成远程平台配置。
