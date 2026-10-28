# License scope and third-party notices / 授权范围与第三方声明

Original NimoteShot contributions are offered under the
[GNU Affero General Public License v3.0 or later](../LICENSE) (`AGPL-3.0-or-later`).
The project is fully open source and free to use, modify, and distribute under
that license. Distribution and network-service use of modified versions require
corresponding source under the same terms. The license does not grant rights to
third-party trademarks, screenshots, fonts, or service accounts. The following
materials retain their own terms; the project license does not override them.

NimoteShot 原创贡献采用 [GNU Affero General Public License v3.0 或更高版本](../LICENSE)
（`AGPL-3.0-or-later`）。项目完全开源，可依该许可证免费使用、修改和分发；分发修改版或
将其作为网络服务提供时，必须以相同条款提供对应源码。本许可证不授予第三方商标、截图、
字体或服务账户的权利。第三方材料仍受各自授权约束，项目许可证不会覆盖它们。

| Material / 材料 | License / 授权 | Evidence / 声明位置 |
| --- | --- | --- |
| `store_screenshots/assets/fonts/Inter.ttf` | SIL OFL 1.1 | [Bundled notice](../store_screenshots/assets/fonts/OFL-Inter.txt), [upstream](https://github.com/rsms/inter) |
| `store_screenshots/assets/fonts/NotoSansCJKsc-*.otf` | SIL OFL 1.1 | [Bundled notice](../store_screenshots/assets/fonts/OFL-NotoSansCJK.txt), [upstream](https://github.com/notofonts/noto-cjk) |
| `store_screenshots/assets/sRGB.icc` | Embedded copyright: “No copyright, use freely” | Profile description: `sRGB built-in`; embedded metadata inspected during audit |
| `demo/nimotecode/originals/` and `previews/` | Redistribution permission not established by this repository / 仓库内尚无可核验的再分发授权记录 | [Demo](../demo/nimotecode/README.md); release gate in [audit](OPEN_SOURCE_AUDIT.md) |
| Pillow (installed dependency) | HPND; bundled native libraries have additional notices | [Upstream license](https://github.com/python-pillow/Pillow/blob/main/LICENSE) |
| jsonschema (installed dependency) | MIT | [Upstream license](https://github.com/python-jsonschema/jsonschema/blob/main/COPYING) |
| Playwright Python (development-only dependency) | Apache-2.0 | [Upstream license](https://github.com/microsoft/playwright-python/blob/main/LICENSE) |
| OpenAI Python SDK (installed dependency) | Apache-2.0 | [Upstream license](https://github.com/openai/openai-python/blob/main/LICENSE) |

Dependencies are installed separately, not relicensed by this project. The table
is not a complete transitive dependency inventory. Before distributing a bundled
application, inventory the exact resolved wheels, native libraries and their
license files. Font redistribution must retain OFL notices; modified fonts must
respect any reserved font names. Service access remains subject to provider terms.

依赖单独安装，不随项目改换许可证；表格不是完整的传递依赖清单。若分发打包应用，
应按实际版本收集全部依赖、原生库及其许可证。字体再分发需保留 OFL 声明，修改字体需
遵守保留名称要求。使用模型服务仍需遵守服务商条款。

The project owner confirmed before publication that the project is unreleased.
The previous MIT file was an unpublished draft and has been replaced for
project-owned code and documentation. New contributions use the same AGPLv3+
license. No project license change overrides third-party rights.

项目所有者确认项目尚未对外发布；先前的 MIT 文件为未发布草案，现已将自有代码和文档
统一改用本项目 AGPLv3+ 许可证，新增贡献遵循相同条款。第三方材料的权利不受影响。
