<p align="center">
  <img src="web/assets/nimoteshot-logo.svg" alt="NimoteShot" width="392">
</p>

<p align="center"><strong>무료 AI App Store 및 Google Play 스크린샷 생성기</strong></p>

<p align="center">
  <a href="README.md">English</a> · <a href="README.zh-CN.md">简体中文</a> · <a href="README.ja.md">日本語</a> · 한국어 · <a href="README.es.md">Español</a>
</p>

NimoteShot은 무료 오픈 소스 AI 스크린샷 생성기입니다. 실제 제품 화면을 App Store 및 Google Play용으로 현지화된 스크린샷으로 바꿉니다. 선택한 비전 모델로 PNG, JPEG, WebP 화면을 분석해 스토어 문구 초안을 만들고, 레이아웃과 내보내기는 컴퓨터에서 처리합니다.

## 빠른 시작

저장소를 복제한 뒤 해당 폴더에서 설치 프로그램을 실행하세요. 앱 자체는 무료 오픈 소스이지만 클라우드 제공업체는 별도 API 액세스가 필요할 수 있습니다. 로컬 모델은 Ollama를 선택할 수 있습니다.

```bash
git clone https://github.com/mobiledevloperlab/nimoteshot.git nimoteshot
cd nimoteshot
./install.sh
```

```powershell
git clone https://github.com/mobiledevloperlab/nimoteshot.git nimoteshot
cd nimoteshot
powershell -ExecutionPolicy Bypass -File .\install.ps1
```

출력된 `http://127.0.0.1:8765` 주소를 여세요. 서버는 로컬 루프백에서만 수신합니다.

## 전후 비교

<table><tr>
<td width="56%" valign="top"><img src="web/assets/ui.png" alt="NimoteShot 홈 및 생성 예시" width="100%"><p align="center"><sub>홈페이지와 생성된 스토어 이미지 예시</sub></p></td>
<td width="44%" valign="top"><img src="web/assets/snapshot.png" alt="4단계 제작 흐름" width="100%"><p align="center"><sub>4단계 로컬 제작 흐름</sub></p></td>
</tr></table>

### 실제 화면 → 스토어 소재

<table><tr>
<td width="33.33%" align="center" valign="top"><strong>모바일 코드 편집기</strong><br><br><img src="demo/nimotecode/originals/code-editor.png" alt="코드 편집기 원본 화면" width="47%"> <img src="demo/nimotecode/previews/01_feature.png" alt="생성된 모바일 IDE 소재" width="47%"><br><sub>원본 화면 → 생성된 기능 소개 소재</sub></td>
<td width="33.33%" align="center" valign="top"><strong>SSH 작업 공간</strong><br><br><img src="demo/nimotecode/originals/ssh-workspace.png" alt="SSH 작업 공간 원본 화면" width="47%"> <img src="demo/nimotecode/previews/03_feature.png" alt="생성된 SSH 작업 공간 소재" width="47%"><br><sub>원본 화면 → 생성된 기능 소개 소재</sub></td>
<td width="33.33%" align="center" valign="top"><strong>AI 코딩 도우미</strong><br><br><img src="demo/nimotecode/originals/ai-assistant.png" alt="AI 도우미 원본 화면" width="47%"> <img src="demo/nimotecode/previews/02_feature.png" alt="생성된 AI 도우미 소재" width="47%"><br><sub>원본 화면 → 생성된 기능 소개 소재</sub></td>
</tr></table>

## NimoteShot의 차이점

- **실제 화면 기반:** 원본 화면을 작업에 저장하고 SHA-256 매니페스트를 기록합니다. 화면을 처음부터 만들어 내는 목업 생성기가 아닙니다.
- **AI 분석과 로컬 렌더링:** 선택한 모델은 화면을 분석하고 문구를 초안으로 만들며, 레이아웃, PNG 렌더링, 패키징, 내보내기는 내 컴퓨터에서 수행합니다.
- **편집 가능한 현지화:** 영어와 선택형 중국어, 일본어, 한국어, 스페인어 출력을 만들고 내보내기 전에 문구를 검토하고 수정할 수 있습니다.

## 주요 기능

- 실제 PNG, JPEG, WebP 화면 1~40장을 현지화된 스토어 소재로 변환합니다.
- 영어와 함께 중국어, 일본어, 한국어, 스페인어 문구를 생성합니다.
- iPhone, Android, iPad의 세로 및 가로 대상 크기를 지원합니다.
- 4가지 기본 시각 스타일, 카테고리별 24가지 팔레트, 선택형 디자인 지시문을 제공합니다.
- 로컬 전용 웹 앱 또는 CLI로 실행하며 렌더링과 내보내기는 기기에서 이루어집니다.

## 설치 및 제공업체

설치 프로그램은 Python 3.11 이상을 확인하고 `.venv`와 의존성을 만든 뒤 스튜디오를 엽니다. 브라우저를 열지 않으려면 `./install.sh --no-browser`를 사용하세요. DeepSeek(기본), Qwen, Zhipu GLM, Volcengine Ark, Hunyuan, OpenAI 호환 API, Gemini, Claude, Ollama, 로그인된 Codex CLI를 선택할 수 있습니다. 각 제공업체의 API 키 또는 설정이 필요합니다.

## 스튜디오 사용법

1. 앱 이름과 짧은 제품 설명 또는 신뢰할 수 있는 공개 HTTPS 제품 페이지를 입력합니다.
2. 전송 권한이 있는 실제 PNG, JPEG, WebP 화면을 1~40장 업로드합니다.
3. 대상 언어, 스타일, 팔레트, 선택형 디자인 지시문을 고릅니다.
4. 비전 모델 제공업체를 선택하고 생성 전에 **Check setup**을 실행합니다.
5. **Analyze and plan**을 누른 뒤 각 출력 언어의 문구를 미리 보고 편집합니다.
6. **Export PNG / ZIP**으로 검증된 이미지를 내보냅니다. API 키가 없으면 **Manual design**에서 문구를 직접 작성할 수 있습니다.

각 작업은 `store_screenshots/runs/<task-id>/`에 저장되며 원본, `source_manifest.json`, 편집 가능한 `config.json`, 미리 보기, PNG, ZIP을 포함합니다. 제출 전 최신 [Apple 스크린샷 사양](https://developer.apple.com/help/app-store-connect/reference/app-information/screenshot-specifications/) 및 [Google Play 이미지 요구사항](https://support.google.com/googleplay/android-developer/answer/9866151)을 확인하세요.

## CLI

`screens/`에 PNG/JPEG/WebP 파일을 넣고 제공업체를 설정한 후 실행합니다.

```bash
.venv/bin/python scripts/nimoteshot.py generate \
  --brand "My App" \
  --description "SSH, Git, 터미널 도구가 있는 모바일 편집기" \
  --style editorial --provider qwen --locales ko-KR
```

Windows에서는 `.venv/bin/python` 대신 `.venv\Scripts\python.exe`를 사용합니다. 전체 옵션은 `python scripts/nimoteshot.py --help`에서 확인하세요.

## 개인정보 및 보안

- 렌더링, 패키징, 내보내기는 로컬에서 수행됩니다. 화면과 제품 설명은 분석을 위해 선택한 모델 제공업체에 전송됩니다.
- 생성 작업에는 원본 화면과 텍스트가 포함됩니다. 비공개 데이터로 취급하고 불필요해지면 제거하세요.
- 모델 출력은 신뢰할 수 없습니다. 게시 전 모든 문구, 주장, 번역, 기기 매핑을 검토하세요.
- API 키, 로컬 프로필, 비공개 화면, 생성 작업, 아카이브를 커밋하지 마세요. 전체 위협 모델은 [SECURITY.md](.github/SECURITY.md)를 참고하세요.

개발, 문제 해결, 제공업체 요구사항 및 전체 기술 정보는 [English README](README.md)를 참고하세요.
