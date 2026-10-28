# Governance / 项目治理

NimoteShot uses maintainer-led review. Maintainers are people granted repository
write/admin access by the repository owner; this document does not appoint new
maintainers. Contributors propose changes through issues and fork pull requests.
Maintainers decide scope and merge changes after review and successful checks.
Significant compatibility or licensing changes should be discussed publicly before
implementation. Security reports stay private until coordinated disclosure.

NimoteShot 采用维护者审核模式。维护者为仓库所有者授予写入或管理权限的成员，本文不新增
任命。贡献者通过 Issue 和 Fork PR 提议改动，由维护者审核并在检查通过后合并。
重大兼容性或授权变更应先公开讨论；漏洞报告在协调披露前保持私密。

Review disputes should be explained in the issue/PR with concrete evidence; ask
another uninvolved maintainer to review where possible. The repository owner is
the final escalation point. Maintainers should recuse themselves from conduct
reports involving them when another responsible maintainer is available. No
response SLA, release cadence or paid support is implied.

争议在 Issue/PR 中说明事实，尽可能请未涉事维护者复核，仓库所有者为最终协调人。
行为投诉涉及维护者本人时，有其他负责人可接手则应回避。不承诺响应 SLA、发布周期或付费支持。

Before a release, follow [the release checklist](docs/RELEASING.md). Record visible
changes in [CHANGELOG.md](CHANGELOG.md). Tagged releases should use semantic
versions; breaking changes during 0.x increment the minor version. Do not rewrite
published tags. This policy does not claim that a release already exists.

发布前执行发布清单，用户可见变更记入变更日志。标签版本使用语义化版本，0.x 阶段的
不兼容变更提升次版本号；不覆盖已发布标签。本规范不表示已有正式发布版本。
