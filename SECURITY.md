# Security policy / 安全策略

## Supported versions / 支持范围

Security fixes target the latest default-branch code. There is currently no
supported stable release or backport promise. Use an up-to-date checkout.

安全修复面向默认分支最新代码，目前没有承诺长期维护的稳定版本或旧版本回补。

## Report privately / 私密报告

On the project's GitHub repository, open **Security → Advisories → Report a
vulnerability** when private vulnerability reporting is enabled. Include the
commit, platform, reproduction steps with synthetic inputs, impact and any fix.
Do not include live credentials or private screenshots.

在项目 GitHub 仓库通过 **Security → Advisories → Report a vulnerability** 私密报告，
提供提交版本、平台、使用合成输入的复现步骤、影响及修复建议，不附真实凭证或私密截图。

If that button is absent, open a public issue containing **only a request to enable
a private security reporting channel**, without vulnerability details. Wait for a
private channel before sharing the report. This checkout has no configured remote;
maintainers must enable the channel before public launch. We cannot promise a
response time; maintainers coordinate fixes and disclosure with the reporter.

若没有该按钮，仅公开请求维护者启用私密报告渠道，不披露漏洞细节，待渠道可用后再提交。
当前本地仓库未配置远程地址，公开前维护者须启用此功能。暂不承诺响应时限；维护者与报告者
协调修复和披露时间。

## Security boundary / 安全边界

The studio is a single-user local application, bound to loopback. It has no user
authentication, tenant isolation or public-server hardening. Do not expose it via
port forwarding, reverse proxies or shared hosts. Local processes with access to
your account can access it. Host and Origin checks reduce browser-based attacks;
they are not authentication.

工作台是单用户本地程序，仅监听回环地址，没有用户认证、租户隔离及公网服务防护。
不要通过端口转发、反向代理或共享主机公开它。本机同账户程序可访问服务，Host 与 Origin
校验仅降低浏览器攻击风险，不是身份认证。

Screenshots and product descriptions are sent to the selected model provider.
Website context makes an outbound HTTPS request; use trusted product sites only.
The public-address DNS check is not a network sandbox or a defense against all
DNS changes between lookup and connection. Custom provider endpoints receive
credentials: configure only endpoints you trust. Model responses and website text
are untrusted inputs; review generated copy before publishing.

截图和产品描述会发送到所选模型服务；网站上下文会发起外部 HTTPS 请求，仅使用可信网站。
公网 DNS 检查不是网络沙箱，不能防御查询和连接之间所有 DNS 变化。自定义服务地址会接收
凭证，应只配置可信地址。模型响应和网页文本均是不可信输入，上架前必须审核输出。

Saved keys are plaintext in your user configuration directory (owner-only files
on Unix; Windows relies on your user directory ACL). Temporary form credentials
are held in process memory. Generated runs include original captures and text;
treat them as private data. Review errors and logs before sharing. Delete local
runs and saved profiles when no longer needed; rotate credentials if exposed.

保存的密钥以明文放在用户配置目录（Unix 文件仅本人可读写；Windows 依赖用户目录 ACL）。
临时表单凭证保存在进程内存。任务目录含原图和文本，应按私密数据管理；分享前检查日志与
错误信息，不再使用时删除本地任务和配置，泄露后及时轮换凭证。
