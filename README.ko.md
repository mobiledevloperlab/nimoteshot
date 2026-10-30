<p align="center">
  <img src="web/assets/nimoteshot-logo.svg" alt="NimoteShot" width="320">
</p>

# NimoteShot — AI 앱스토어 스크린샷 생성기

**실제 앱 화면, 편집 가능한 문구, 로컬 PNG 내보내기.**

앱 캡처를 **App Store와 Google Play** 등록 이미지로 만드세요. 비전 모델로 문구를 작성하고, 실시간 편집기에서 텍스트와 레이아웃을 조정한 뒤 iPhone·iPad·Android용 이미지를 내보냅니다. 앱 출시를 준비하는 개인 개발자와 제품 팀을 위한 도구입니다.

**Python 3.11+ · Linux / macOS / Windows · 출력 언어 17개 · AGPLv3+**

[English](README.md) · [简体中文](README.zh-CN.md) · [日本語](README.ja.md) · 한국어 · [Español](README.es.md)

![영어와 중국어가 섞인 제목을 수정하면 옆의 스크린샷 미리 보기에 반영되는 NimoteShot 실시간 편집기](web/assets/redefine_promotion.png)

*제목, 부제목, 레이아웃을 결과 옆에서 편집합니다. 해당 미리 보기만 로컬에서 갱신하며 추가 AI 호출은 없습니다. 실제 실행 화면입니다.*

## NimoteShot을 사용하는 이유

- **내 제품 화면으로 시작합니다.** PNG·JPEG·WebP를 업로드하면 보이는 기능을 바탕으로 문구를 작성하고 원본 화면으로 이미지를 구성합니다.
- **생성 후에도 수정할 수 있습니다.** 문구, 템플릿, 색상, 순서를 바꾸고 자동 미리 보기를 확인한 후 내보냅니다.
- **여러 시장과 기기를 준비합니다.** 17개 언어 버전과 6개 기기·방향 조합을 선택하며 입력 문자에 맞는 내장 글꼴을 사용합니다.
- **원하는 방식으로 사용합니다.** 웹 또는 CLI로 실행합니다. 수동 디자인은 API 키가 필요 없고, AI 분석은 클라우드나 로컬 비전 모델을 선택합니다.

소프트웨어는 무료 오픈 소스입니다. 클라우드 모델 API 사용료는 제공업체가 별도로 청구할 수 있습니다.

## 빠른 시작

**Python 3.11 이상**을 설치한 후 저장소를 복제합니다.

```bash
git clone https://github.com/mobiledevloperlab/nimoteshot.git
cd nimoteshot
```

Linux / macOS:

```bash
./install.sh
```

Windows PowerShell:

```powershell
powershell -ExecutionPolicy Bypass -File .\install.ps1
```

설치 프로그램이 `.venv`와 의존성을 준비하고 서비스를 시작합니다. **터미널에 표시된 실제 URL**을 여세요. 기본 주소는 `http://127.0.0.1:8765`입니다. **Manual design**에서 키 없이 편집기를 먼저 체험할 수 있습니다.

## 캡처에서 스토어 이미지까지

1. 앱 이름, 설명 또는 공개 HTTPS 사이트를 입력하고 실제 화면 1~40장을 추가합니다.
2. 출력 언어, 기기 크기, 디자인 방향을 선택한 뒤 AI 분석 또는 수동 디자인을 시작합니다.
3. 언어별 문구와 레이아웃을 수정하고 실시간 미리 보기를 확인합니다. 개별 수정은 해당 화면만, 전역 설정 변경은 현재 미리 보기 전체를 갱신합니다.
4. **Export PNG / ZIP**으로 검증된 다중 해상도 RGB/sRGB 이미지와 편집 가능한 설정을 내보냅니다.

| 원본 앱 화면 | 생성된 스토어 이미지 |
| --- | --- |
| <img src="demo/nimotecode/originals/code-editor.png" alt="NimoteCode 모바일 코드 편집기 원본 화면" width="220"> | <img src="demo/nimotecode/previews/01_feature.png" alt="실제 화면으로 생성한 App Store 이미지" width="220"> |

[전체 데모 보기](demo/nimotecode/). 문구 재작성, 로컬 템플릿 재선택, 원본 재분석은 선택형 조정으로 묶고 덮어쓰기 범위를 설명합니다.

## 언어와 글꼴

출력 선택, 편집할 언어 버전, AI 지시, 미리 보기, 내보내기는 같은 **17개 언어 목록**을 사용합니다. 영어, 중국어 간체·번체, 일본어, 한국어, 스페인어, 프랑스어, 독일어, 브라질 포르투갈어, 러시아어, 그리스어, 베트남어, 아랍어, 힌디어, 벵골어, 태국어, 히브리어를 지원합니다. 영어는 기본 포함되며 추가 언어는 필요에 따라 선택합니다.

언어별 문구는 독립적으로 유지됩니다. 글꼴은 입력 문자에 따라 선택하므로 영어 칸에도 한국어나 중국어를 입력할 수 있습니다. 계획 후 추가한 언어는 임시 문구로 시작하고 편집 또는 재생성 안내를 표시합니다. 입력기 조합이 완료된 후 미리 보기를 갱신합니다.

조작 화면은 영어·중국어 간체·일본어·한국어·스페인어입니다. 내장 글꼴이 지원하지 않는 문자 조합이나 복합 문자 조판을 지원하지 않는 환경에서는 오류를 명확하게 표시합니다.

## 형식, 모델, CLI

iPhone·iPad·Android의 세로·가로 형식, 기본 스타일 4개, 분류별 팔레트 24개와 편집 가능한 템플릿을 제공합니다. 각 작업은 원본, SHA-256 매니페스트, 설정, 미리 보기, PNG, ZIP을 `store_screenshots/runs/<task-id>/`에 보관합니다. [출력 규격](store_screenshots/targets.json)을 참고하세요.

DeepSeek(기본), Qwen, GLM, Volcengine Ark, Hunyuan, OpenAI 호환 API, Gemini, Claude, Ollama, Codex CLI 통합을 선택할 수 있습니다. 이미지 분석에는 비전 모델과 사용 권한이 필요합니다. [모델 설정](docs/PROVIDERS.md)과 [CLI 안내](README.md#cli)를 참고하세요.

## 업데이트와 개인정보

업데이트 후 `python -m pip install -r store_screenshots/requirements.txt`를 실행하고 서비스를 다시 시작하세요. 포트가 사용 중이면 현재 프로젝트의 확인된 유휴 서비스를 정상 종료 후 다시 시작합니다. 진행 중인 작업과 다른 프로그램은 유지하며 새 포트의 실제 URL을 표시합니다. 프로세스를 강제 종료하지 않습니다.

렌더링은 로컬에서 실행하지만 **AI 분석 시 캡처와 제품 정보는 선택한 제공업체로 전송됩니다**. 저장한 키는 사용자 설정에 평문으로 보관됩니다. 전송 권한이 있는 캡처를 사용하고 게시 전 문구와 번역을 검토하세요. 자세한 내용과 비공개 취약점 제보 방법은 [보안 정책](.github/SECURITY.md)에 있습니다.

## 함께 개선하기

자신의 앱으로 사용해 보고 [재현 가능한 문제를 제보](https://github.com/mobiledevloperlab/nimoteshot/issues/new/choose)하거나 번역·글꼴·템플릿을 개선하고 코드·문서 PR을 보낼 수 있습니다. 큰 변경은 Issue에서 먼저 논의하세요. 개발 환경과 테스트는 [기여 가이드](.github/CONTRIBUTING.md), 기술 정보는 [설계 및 검증](docs/VISION_UPGRADE.md)을 참고하세요.

## 라이선스

[GNU AGPLv3 이상](LICENSE)으로 배포합니다. 라이선스 조건에 따라 사용, 연구, 수정, 공유할 수 있습니다. 수정 버전을 네트워크 서비스로 제공할 경우 라이선스에서 요구하는 해당 소스를 제공해야 합니다. 글꼴 등 외부 자료는 원래 조건을 유지합니다. [외부 자료 고지](docs/THIRD_PARTY_NOTICES.md), [행동 강령](.github/CODE_OF_CONDUCT.md), [운영 규칙](docs/GOVERNANCE.md)도 확인하세요.
