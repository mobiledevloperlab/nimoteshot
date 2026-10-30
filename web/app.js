const copy = {
  zh: {
    local: '本地优先', eyebrow: '应用商店截图工作台', headline: '把真实产品体验，<br><em>变成清晰的商店故事。</em>', intro: '上传真实界面，选择视觉模型与设计方向，一次生成多语言、多设备尺寸的上架截图。', start: '开始制作', localNote: '图片与密钥只在本地服务中处理', formatMetric: '设备规格', languageMetric: '输出语言', captureMetric: '真实 PNG', builderEyebrow: '截图生成器', builderTitle: '用四步完成一套截图', builderNote: '先补足产品上下文，再让模型从真实界面中提炼准确文案。', stepProduct: '产品信息', stepCaptures: '真实截图', stepStyle: '视觉风格', stepModel: '视觉模型', productTitle: '告诉我们产品是什么', productNote: '填写功能简介，或提供公开官网。两者都提供时，模型会交叉参考。', appName: '应用名称', description: '核心功能与目标用户', descriptionHint: '建议写 1–3 句话；有官网时可以留空。', website: '公开产品官网（可选）', websiteHint: '只读取公开 HTML 文本，作为文案参考。', capturesTitle: '上传真实产品界面', capturesNote: '支持 1–40 张 PNG。设备和语言变体请使用清晰的文件名。', dropTitle: '选择 PNG，或拖放到这里', dropHint: '建议包含手机、横屏、iPad 和不同语言的真实界面', styleTitle: '选择设计方向', styleNote: '一个风格会保持所有设备与语言输出的一致性。', modelTitle: '选择视觉模型', modelNote: '模型只分析截图并起草文案；排版、图片和 ZIP 在本地完成。', providerNoteTitle: '国内与国际模型均可使用', providerNote: '已预设通义、智谱、豆包、混元、OpenAI、Gemini、Claude 和本地 Ollama。', provider: '服务商', modelPick: '视觉模型', apiKey: 'API 密钥', advanced: '高级设置：模型 ID 或接口地址', customModel: '自定义模型或接入点 ID', baseUrl: 'API 基础地址', baseUrlHint: '仅在需覆盖预设地址时填写。', configTitle: '也可以通过本地配置使用模型', configPage: '当前页输入的密钥只用于本次生成。', configEnvironment: '正在使用系统环境变量，无需重复输入密钥。', configProfile: '正在使用本地 CLI 配置档案，无需重复输入密钥。', configCodex: '使用已登录的 Codex CLI，无需 API 密钥。', configOllama: '使用本地 Ollama 服务，无需 API 密钥。', copyConfig: '复制 CLI 配置命令', copied: '已复制', readiness: '填写信息后即可检查配置', check: '检查配置', submitTitle: '准备生成', submitNote: '自动创建任务目录、校验导出并打包 ZIP。', generate: '生成全部截图', working: '正在生成', progressNote: '请保持本地服务运行，完成后可下载 ZIP。', ready: '生成完成', resultTitle: '商店截图已经准备好', download: '下载 ZIP', previewEn: '查看英文总览', previewZh: '查看中文总览', cliTitle: '也可以从终端一键运行', cliNote: '网页和命令行共享相同的模型、校验与输出流程。', footer: '真实界面，准确表达。', missingInfo: '请填写功能简介或公开官网。', missingFiles: '请上传至少 1 张 PNG。', tooMany: '最多上传 40 张 PNG。', checking: '正在检查配置…', readyStatus: '配置已就绪', upload: '正在上传原图…', resultSummary: '张截图 · 多语言 · 四类设备', openaiAccount: '需要 OpenAI API 密钥；ChatGPT 网页订阅不能直接作为 API 密钥使用。', endpointModel: '请在下方填写已开通的模型或接入点 ID。', customProvider: '请填写模型 ID 与 HTTPS 接口地址。'
  },
  en: {
    local: 'LOCAL FIRST', eyebrow: 'APP STORE SCREENSHOT STUDIO', headline: 'Turn real product moments<br><em>into a clear store story.</em>', intro: 'Add real captures, choose a vision model and a design direction, then create store-ready screenshots for every format and language.', start: 'Start building', localNote: 'Captures and keys stay in your local service', formatMetric: 'DEVICE FORMATS', languageMetric: 'OUTPUT LANGUAGES', captureMetric: 'REAL PNGS', builderEyebrow: 'SCREENSHOT BUILDER', builderTitle: 'Build a full store set in four steps', builderNote: 'Add enough product context, then let the model draw accurate copy from the real interface.', stepProduct: 'Product context', stepCaptures: 'Real captures', stepStyle: 'Design style', stepModel: 'Vision model', productTitle: 'Tell us what the product does', productNote: 'Add a short description or a public website. When both are present, the model cross-checks them.', appName: 'App name', description: 'Core capabilities and intended users', descriptionHint: 'One to three sentences work well. Leave it blank if you provide a website.', website: 'Public product website (optional)', websiteHint: 'Only public HTML text is read as copy context.', capturesTitle: 'Add real product captures', capturesNote: 'Add 1–40 PNG files. Use clear names for device and language variants.', dropTitle: 'Choose PNG files or drop them here', dropHint: 'Phone, landscape, iPad, and language variants are all useful', styleTitle: 'Choose a design direction', styleNote: 'One style keeps every device and language output consistent.', modelTitle: 'Choose a vision model', modelNote: 'The model analyzes captures and drafts copy. Layout, image exports, and ZIP packaging run locally.', providerNoteTitle: 'Mainland China and global models are supported', providerNote: 'Presets include Qwen, GLM, Doubao, Hunyuan, OpenAI, Gemini, Claude, and local Ollama.', provider: 'Provider', modelPick: 'Vision model', apiKey: 'API key', advanced: 'Advanced: model ID or API endpoint', customModel: 'Custom model or endpoint ID', baseUrl: 'API base URL', baseUrlHint: 'Only fill this in to override the preset address.', configTitle: 'You can also configure this model locally', configPage: 'A key entered here is used only for this generation.', configEnvironment: 'A system environment variable is ready; no key is needed here.', configProfile: 'A local CLI profile is ready; no key is needed here.', configCodex: 'Your signed-in Codex CLI will be used; no API key is needed.', configOllama: 'Your local Ollama service is used; no API key is needed.', copyConfig: 'Copy CLI setup command', copied: 'Copied', readiness: 'Complete the form to check setup', check: 'Check setup', submitTitle: 'Ready to generate', submitNote: 'A task folder, validated exports, and a ZIP are created automatically.', generate: 'Generate all screenshots', working: 'GENERATING', progressNote: 'Keep the local service running until the ZIP is ready.', ready: 'COMPLETE', resultTitle: 'Your store set is ready', download: 'Download ZIP', previewEn: 'View English overview', previewZh: 'View Chinese overview', cliTitle: 'Prefer one command in the terminal?', cliNote: 'The web UI and CLI share providers, validation, and output.', footer: 'Real interfaces, accurately expressed.', missingInfo: 'Add an app description or a public website.', missingFiles: 'Add at least one PNG capture.', tooMany: 'Upload at most 40 PNG files.', checking: 'Checking setup…', readyStatus: 'Setup is ready', upload: 'Uploading captures…', resultSummary: 'screens · English + Chinese · four formats', openaiAccount: 'An OpenAI API key is required. A ChatGPT web subscription cannot be used as an API key.', endpointModel: 'Enter an enabled model or endpoint ID below.', customProvider: 'Enter both a model ID and an HTTPS API base URL.'
  }
};

Object.assign(copy.zh, {
  designPrompt: '自定义版型与设计提示词（可选）',
  designPromptHint: '例如：突出手机样机；采用杂志感大标题与留白；避免渐变。此要求会和所选风格一起交给模型。',
  configTitle: '配置、测试并复用模型', copyConfig: '复制配置提示词', saveConfig: '验证并保存到本机',
  configSaved: '已保存，可在下次生成时复用。', configTesting: '正在检查并保存配置…',
  appNameHint: '示例：Nimote Code、Focus Habit', outputLanguages: '输出语言', outputLanguagesHint: '英文始终生成；再选择 1–4 种本地化文案。', englishDefault: '英语 · 默认', apiKeyExample: '示例：sk-... 或服务商 API Key', modelExample: '示例：gpt-4o 或 ep-2025xxxx', switchTheme: '切换为深色主题', switchThemeLight: '切换为浅色主题', sourceProfile: '原始截图设备与方向', sourceProfileHint: '选择最接近上传图片的设备与方向；系统会优先匹配相同画面比例。', sourceIphone: 'iPhone · 竖屏', sourceIphoneLandscape: 'iPhone · 横屏', sourceAndroid: 'Android · 竖屏', sourceAndroidLandscape: 'Android · 横屏', sourceTabletPortrait: 'iPad / 平板 · 竖屏', sourceTablet: 'iPad / 平板 · 横屏', exportTargets: '要生成的商店规格', exportTargetsHint: '按需多选。每个规格会导出其对应 App Store 或 Google Play 的常用分辨率。', targetIphone: 'iPhone 竖屏', targetIphoneLandscape: 'iPhone 横屏', targetAndroid: 'Android 竖屏', targetAndroidLandscape: 'Android 横屏', targetTabletPortrait: 'iPad 竖屏', targetTablet: 'iPad 横屏', missingTargets: '请至少选择一个商店规格。'
});
Object.assign(copy.en, {
  designPrompt: 'Custom layout and design direction (optional)',
  designPromptHint: 'For example: prioritize phone mockups, magazine-style headlines and whitespace, or avoid gradients. It is sent to the model alongside the selected style.',
  configTitle: 'Configure, test, and reuse a model', copyConfig: 'Copy setup prompt', saveConfig: 'Verify and save locally',
  configSaved: 'Saved for future runs.', configTesting: 'Checking and saving configuration…',
  appNameHint: 'Example: Nimote Code or Focus Habit', outputLanguages: 'Output languages', outputLanguagesHint: 'English is always generated; choose 1–4 localized copy sets.', englishDefault: 'English · Default', apiKeyExample: 'Example: sk-... or your provider API key', modelExample: 'Example: gpt-4o or ep-2025xxxx', switchTheme: 'Switch to dark theme', switchThemeLight: 'Switch to light theme', sourceProfile: 'Source device and orientation', sourceProfileHint: 'Select the closest device and orientation so matching captures are preferred.', sourceIphone: 'iPhone · Portrait', sourceIphoneLandscape: 'iPhone · Landscape', sourceAndroid: 'Android · Portrait', sourceAndroidLandscape: 'Android · Landscape', sourceTabletPortrait: 'iPad / tablet · Portrait', sourceTablet: 'iPad / tablet · Landscape', exportTargets: 'Store formats to generate', exportTargetsHint: 'Select the formats you need. Each includes the common App Store or Google Play resolutions.', targetIphone: 'iPhone portrait', targetIphoneLandscape: 'iPhone landscape', targetAndroid: 'Android portrait', targetAndroidLandscape: 'Android landscape', targetTabletPortrait: 'iPad portrait', targetTablet: 'iPad landscape', missingTargets: 'Choose at least one store format.'
});

Object.assign(copy, {
  ja: {
    local:'ローカル処理',eyebrow:'APP STORE SCREENSHOT STUDIO',headline:'本物のプロダクト体験を、<br><em>伝わるストーリーに。</em>',intro:'実際の画面を追加し、ビジョンモデルとデザインを選ぶだけで、各形式・言語のストア用スクリーンショットを生成します。',start:'制作を始める',localNote:'画像とキーはローカルサービス内だけで処理されます',formatMetric:'デバイス形式',languageMetric:'出力言語',captureMetric:'実際の PNG',builderEyebrow:'SCREENSHOT BUILDER',builderTitle:'4 ステップでストアセットを作成',builderNote:'製品の文脈を入力すると、モデルが実際の画面から正確なコピーを作成します。',stepProduct:'製品情報',stepCaptures:'実際の画面',stepStyle:'デザイン',stepModel:'ビジョンモデル',productTitle:'製品について教えてください',productNote:'短い説明または公開サイトを追加してください。両方ある場合は相互に参照します。',appName:'アプリ名',description:'主な機能と対象ユーザー',descriptionHint:'1〜3 文がおすすめです。サイトがある場合は空欄でも構いません。',website:'公開製品サイト（任意）',websiteHint:'コピーの文脈として公開 HTML テキストのみ読み取ります。',designPrompt:'レイアウトとデザイン指示（任意）',designPromptHint:'例：スマホモックアップを強調し、雑誌風の見出しと余白を使う。グラデーションは避ける。',outputLanguages:'出力言語',outputLanguagesHint:'英語は常に生成されます。1〜4 種類のローカライズを選択してください。',englishDefault:'英語・標準',capturesTitle:'実際の製品画面を追加',capturesNote:'PNG を 1〜40 枚追加できます。デバイスと言語が分かる名前にしてください。',dropTitle:'PNG を選択、またはここにドロップ',dropHint:'スマホ、横向き、iPad、言語バリエーションが有用です',styleTitle:'デザインの方向性を選択',styleNote:'ひとつのスタイルが、すべてのデバイスと言語で一貫性を保ちます。',modelTitle:'ビジョンモデルを選択',modelNote:'モデルは画面を分析しコピーを下書きします。レイアウトと書き出しはローカルで行われます。',providerNoteTitle:'国内・海外モデルに対応',providerNote:'Qwen、GLM、Doubao、Hunyuan、OpenAI、Gemini、Claude、ローカル Ollama を利用できます。',provider:'プロバイダー',modelPick:'ビジョンモデル',apiKey:'API キー',advanced:'詳細設定：モデル ID または API エンドポイント',customModel:'カスタムモデルまたはエンドポイント ID',baseUrl:'API ベース URL',baseUrlHint:'プリセットのアドレスを変更する場合のみ入力してください。',configTitle:'モデルの設定・テスト・再利用',configPage:'ここで入力したキーは今回の生成だけに使用されます。',configEnvironment:'システム環境変数を使用しています。キーの再入力は不要です。',configProfile:'ローカル CLI プロファイルを使用しています。',configCodex:'ログイン済み Codex CLI を使用します。API キーは不要です。',configOllama:'ローカル Ollama サービスを使用します。API キーは不要です。',copyConfig:'セットアップ文をコピー',saveConfig:'検証してローカルに保存',configSaved:'次回以降に再利用できるよう保存しました。',configTesting:'設定を確認して保存しています…',readiness:'フォームを完了して設定を確認',check:'設定を確認',submitTitle:'生成の準備完了',submitNote:'タスクフォルダー、検証済みの出力、ZIP を自動作成します。',generate:'すべてのスクリーンショットを生成',working:'生成中',progressNote:'ZIP の準備が完了するまでローカルサービスを実行してください。',ready:'完了',resultTitle:'ストア用セットの準備ができました',download:'ZIP をダウンロード',previewEn:'英語の概要を見る',previewZh:'中国語の概要を見る',cliTitle:'ターミナルからも実行できます',cliNote:'Web UI と CLI はプロバイダー、検証、出力を共有します。',footer:'本物の画面を、正確に伝える。',missingInfo:'アプリの説明または公開サイトを追加してください。',missingFiles:'PNG を 1 枚以上追加してください。',tooMany:'アップロードは最大 40 枚です。',checking:'設定を確認中…',readyStatus:'設定の準備ができました',upload:'画面をアップロード中…',resultSummary:'枚の画面・複数言語・4 形式',switchTheme:'ダークテーマに切り替え',switchThemeLight:'ライトテーマに切り替え'
  },
  ko: {
    local:'로컬 우선',eyebrow:'APP STORE SCREENSHOT STUDIO',headline:'실제 제품 경험을<br><em>명확한 스토어 이야기로 만드세요.</em>',intro:'실제 화면을 추가하고 비전 모델과 디자인 방향을 선택하면, 모든 형식과 언어에 맞는 스토어 스크린샷을 만듭니다.',start:'제작 시작',localNote:'캡처와 키는 로컬 서비스에서만 처리됩니다',formatMetric:'기기 형식',languageMetric:'출력 언어',captureMetric:'실제 PNG',builderEyebrow:'SCREENSHOT BUILDER',builderTitle:'4단계로 완성하는 스토어 세트',builderNote:'제품 정보를 더하면 모델이 실제 인터페이스를 바탕으로 정확한 카피를 작성합니다.',stepProduct:'제품 정보',stepCaptures:'실제 화면',stepStyle:'디자인 스타일',stepModel:'비전 모델',productTitle:'제품이 무엇인지 알려주세요',productNote:'짧은 설명 또는 공개 웹사이트를 추가하세요. 둘 다 있으면 서로 교차 참조합니다.',appName:'앱 이름',description:'핵심 기능 및 대상 사용자',descriptionHint:'1~3문장이 적당합니다. 웹사이트가 있다면 비워 둘 수 있습니다.',website:'공개 제품 웹사이트 (선택)',websiteHint:'카피 맥락을 위해 공개 HTML 텍스트만 읽습니다.',designPrompt:'사용자 지정 레이아웃 및 디자인 방향 (선택)',designPromptHint:'예: 휴대폰 목업과 큰 제목, 여백을 강조하고 그라데이션은 피하세요.',outputLanguages:'출력 언어',outputLanguagesHint:'영어는 항상 생성됩니다. 1~4개 현지화 카피를 선택하세요.',englishDefault:'영어 · 기본',capturesTitle:'실제 제품 화면 추가',capturesNote:'PNG 파일을 1~40개 추가하세요. 기기와 언어가 드러나는 이름을 사용하세요.',dropTitle:'PNG를 선택하거나 여기에 놓으세요',dropHint:'휴대폰, 가로 화면, iPad, 언어별 화면이 모두 유용합니다',styleTitle:'디자인 방향 선택',styleNote:'하나의 스타일이 모든 기기와 언어 출력의 일관성을 지킵니다.',modelTitle:'비전 모델 선택',modelNote:'모델은 화면을 분석하고 카피 초안을 만듭니다. 레이아웃과 내보내기는 로컬에서 처리됩니다.',providerNoteTitle:'중국 및 글로벌 모델 지원',providerNote:'Qwen, GLM, Doubao, Hunyuan, OpenAI, Gemini, Claude 및 로컬 Ollama가 제공됩니다.',provider:'제공자',modelPick:'비전 모델',apiKey:'API 키',advanced:'고급: 모델 ID 또는 API 엔드포인트',customModel:'사용자 지정 모델 또는 엔드포인트 ID',baseUrl:'API 기본 URL',baseUrlHint:'기본 주소를 재정의할 때만 입력하세요.',configTitle:'모델 구성, 테스트 및 재사용',configPage:'여기에 입력한 키는 이번 생성에만 사용됩니다.',configEnvironment:'시스템 환경 변수가 준비되었습니다. 키가 필요 없습니다.',configProfile:'로컬 CLI 프로필을 사용합니다.',configCodex:'로그인한 Codex CLI를 사용합니다. API 키가 필요 없습니다.',configOllama:'로컬 Ollama 서비스를 사용합니다. API 키가 필요 없습니다.',copyConfig:'설정 프롬프트 복사',saveConfig:'확인 후 로컬에 저장',configSaved:'다음 실행을 위해 저장했습니다.',configTesting:'구성을 확인하고 저장하는 중…',readiness:'양식을 완료하여 설정 확인',check:'설정 확인',submitTitle:'생성 준비 완료',submitNote:'작업 폴더, 검증된 내보내기 및 ZIP이 자동으로 만들어집니다.',generate:'모든 스크린샷 생성',working:'생성 중',progressNote:'ZIP이 준비될 때까지 로컬 서비스를 실행하세요.',ready:'완료',resultTitle:'스토어 세트가 준비되었습니다',download:'ZIP 다운로드',previewEn:'영문 개요 보기',previewZh:'중문 개요 보기',cliTitle:'터미널에서 한 번에 실행할 수도 있습니다',cliNote:'웹 UI와 CLI는 제공자, 검증 및 출력을 공유합니다.',footer:'실제 인터페이스를 정확하게 표현합니다.',missingInfo:'앱 설명 또는 공개 웹사이트를 추가하세요.',missingFiles:'PNG 화면을 하나 이상 추가하세요.',tooMany:'최대 40개 PNG를 업로드할 수 있습니다.',checking:'설정 확인 중…',readyStatus:'설정 준비 완료',upload:'화면 업로드 중…',resultSummary:'개 화면 · 여러 언어 · 4개 형식',switchTheme:'다크 테마로 전환',switchThemeLight:'라이트 테마로 전환'
  },
  es: {
    local:'PRIMERO LOCAL',eyebrow:'ESTUDIO DE CAPTURAS PARA APP STORE',headline:'Convierte momentos reales<br><em>en una historia clara para tu tienda.</em>',intro:'Añade capturas reales, elige un modelo visual y una dirección de diseño para crear imágenes listas para la tienda en cada formato e idioma.',start:'Empezar',localNote:'Las capturas y claves se procesan solo en tu servicio local',formatMetric:'FORMATOS',languageMetric:'IDIOMAS',captureMetric:'PNG REALES',builderEyebrow:'CREADOR DE CAPTURAS',builderTitle:'Crea un set completo en cuatro pasos',builderNote:'Añade contexto del producto para que el modelo extraiga textos precisos de la interfaz real.',stepProduct:'Producto',stepCaptures:'Capturas reales',stepStyle:'Estilo visual',stepModel:'Modelo visual',productTitle:'Cuéntanos qué hace el producto',productNote:'Añade una descripción breve o un sitio público. Si incluyes ambos, el modelo los contrasta.',appName:'Nombre de la app',description:'Funciones principales y público objetivo',descriptionHint:'Bastan de una a tres frases. Déjalo vacío si incluyes un sitio web.',website:'Sitio web público (opcional)',websiteHint:'Solo se lee el texto HTML público como contexto.',designPrompt:'Diseño y dirección visual personalizados (opcional)',designPromptHint:'Por ejemplo: prioriza maquetas de móvil, titulares editoriales y espacio en blanco; evita degradados.',outputLanguages:'Idiomas de salida',outputLanguagesHint:'El inglés siempre se genera; elige entre 1 y 4 versiones localizadas.',englishDefault:'Inglés · Predeterminado',capturesTitle:'Añade capturas reales del producto',capturesNote:'Añade de 1 a 40 PNG. Usa nombres claros para las variantes de dispositivo e idioma.',dropTitle:'Elige archivos PNG o suéltalos aquí',dropHint:'Las variantes de móvil, horizontal, iPad e idioma son útiles',styleTitle:'Elige una dirección de diseño',styleNote:'Un estilo mantiene la coherencia en todos los dispositivos e idiomas.',modelTitle:'Elige un modelo visual',modelNote:'El modelo analiza las capturas y redacta el texto. La maquetación y exportación se hacen localmente.',providerNoteTitle:'Modelos chinos e internacionales compatibles',providerNote:'Incluye Qwen, GLM, Doubao, Hunyuan, OpenAI, Gemini, Claude y Ollama local.',provider:'Proveedor',modelPick:'Modelo visual',apiKey:'Clave API',advanced:'Avanzado: ID de modelo o endpoint API',customModel:'Modelo personalizado o ID de endpoint',baseUrl:'URL base de la API',baseUrlHint:'Rellénalo solo para sustituir la dirección predeterminada.',configTitle:'Configura, prueba y reutiliza un modelo',configPage:'La clave introducida aquí se usa solo para esta generación.',configEnvironment:'Hay una variable de entorno lista; no hace falta clave.',configProfile:'Se está usando un perfil CLI local.',configCodex:'Se usará Codex CLI conectado; no se necesita clave API.',configOllama:'Se usa tu servicio Ollama local; no se necesita clave API.',copyConfig:'Copiar mensaje de configuración',saveConfig:'Verificar y guardar localmente',configSaved:'Guardado para futuros usos.',configTesting:'Comprobando y guardando la configuración…',readiness:'Completa el formulario para comprobar la configuración',check:'Comprobar configuración',submitTitle:'Listo para generar',submitNote:'Se crean automáticamente una carpeta de tarea, exportaciones validadas y un ZIP.',generate:'Generar todas las capturas',working:'GENERANDO',progressNote:'Mantén el servicio local activo hasta que el ZIP esté listo.',ready:'COMPLETADO',resultTitle:'Tu set para la tienda está listo',download:'Descargar ZIP',previewEn:'Ver resumen en inglés',previewZh:'Ver resumen en chino',cliTitle:'¿Prefieres usar un comando en la terminal?',cliNote:'La interfaz web y la CLI comparten proveedores, validación y salida.',footer:'Interfaces reales, expresadas con precisión.',missingInfo:'Añade una descripción de la app o un sitio web público.',missingFiles:'Añade al menos una captura PNG.',tooMany:'Sube como máximo 40 PNG.',checking:'Comprobando la configuración…',readyStatus:'La configuración está lista',upload:'Subiendo capturas…',resultSummary:'capturas · varios idiomas · cuatro formatos',switchTheme:'Cambiar a tema oscuro',switchThemeLight:'Cambiar a tema claro'
  }
});

const $ = id => document.getElementById(id);
// Footer labels share the existing locale fallback and local document routes.
Object.assign(copy.zh, { footerGuide: '使用指南', footerContribute: '参与贡献', footerSecurity: '安全与数据', footerLicense: '许可证', footerNotices: '第三方声明', footerTerms: '完全开源 · GNU AGPLv3+', footerResources: '项目资料' });
Object.assign(copy.en, { footerGuide: 'User guide', footerContribute: 'Contribute', footerSecurity: 'Security & data', footerLicense: 'License', footerNotices: 'Third-party notices', footerTerms: 'Fully open source · GNU AGPLv3+', footerResources: 'Project resources' });
Object.assign(copy.ja, { footerGuide: '使い方', footerContribute: '貢献する', footerSecurity: 'セキュリティとデータ', footerLicense: 'ライセンス', footerNotices: '第三者の権利表示', footerTerms: '完全オープンソース · GNU AGPLv3+', footerResources: 'プロジェクト資料' });
Object.assign(copy.ko, { footerGuide: '사용 안내', footerContribute: '기여하기', footerSecurity: '보안 및 데이터', footerLicense: '라이선스', footerNotices: '제3자 고지', footerTerms: '완전한 오픈 소스 · GNU AGPLv3+', footerResources: '프로젝트 자료' });
Object.assign(copy.es, { footerGuide: 'Guía de uso', footerContribute: 'Contribuir', footerSecurity: 'Seguridad y datos', footerLicense: 'Licencia', footerNotices: 'Avisos de terceros', footerTerms: 'Totalmente de código abierto · GNU AGPLv3+', footerResources: 'Recursos del proyecto' });

function preferredLanguage() {
  const saved=localStorage.getItem('nimoteshot-language');
  if(Object.hasOwn(editorMessages,saved))return saved;
  return (navigator.languages||[navigator.language]).map(locale=>locale.toLowerCase().split(/[-_]/)[0]).find(locale=>Object.hasOwn(editorMessages,locale))||'en';
}
function catalogText(item,field) { return item[`${field}_${state.language}`]??item[`${field}_en`]??''; }
function languageLabel(locale) { return new Intl.DisplayNames([state.language],{type:'language'}).of(locale); }
const state = { language: preferredLanguage(), theme: localStorage.getItem('nimoteshot-theme') || (matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light'), options: null, lastProvider: null };
const sleep = ms => new Promise(resolve => setTimeout(resolve, ms));
const words = () => new Proxy(copy.en, { get: (fallback, key) => copy[state.language]?.[key] ?? fallback[key] });

function applyTheme() {
  document.documentElement.dataset.theme = state.theme;
  document.querySelector('meta[name="theme-color"]')?.setAttribute('content', state.theme === 'dark' ? '#121316' : '#f8f9fa');
  $('theme').textContent = state.theme === 'dark' ? '☀' : '◐';
  $('theme').title = state.theme === 'dark' ? words().switchThemeLight : words().switchTheme;
  $('theme').setAttribute('aria-label', $('theme').title);
}

function translate() {
  Object.assign(copy.zh, {demoBadge:'截图生成示例',demoSource:'基于 NimoteCode 真实界面，由 NimoteShot 生成的应用商店截图。',demoEyebrow:'精选应用 · 真实作品',demoIntro:'把开发工作台，装进口袋。',demoHint:'浏览真实界面，点击截图查看大图。',optionalDesign:'设计提示词与补充要求（可选）',localNote:'本地排版与导出 · 截图发送至所选模型分析',check:'检查模型配置',saveConfig:'检查并保存配置',promptPreset:'设计提示词预设',appCategory:'按应用类型选择配色'});
  Object.assign(copy.en, {demoBadge:'Generated screenshot demo',demoSource:'App store screenshots generated by NimoteShot from real NimoteCode screens.',demoEyebrow:'FEATURED APP · REAL SCREENS',demoIntro:'Your development workspace. In your pocket.',demoHint:'Explore real screens. Select an image to view it full size.',optionalDesign:'Design presets and extra requirements (optional)',localNote:'Local rendering · Captures sent to your selected model',check:'Check model configuration',saveConfig:'Check and save configuration',promptPreset:'Design prompt preset',appCategory:'Palettes by app category'});
  Object.keys(editorMessages).forEach(lang=>Object.assign(copy[lang],editorMessages[lang],{resultTitle:editorMessages[lang].refine}));
  document.documentElement.lang = ({zh:'zh-CN', en:'en', ja:'ja', ko:'ko', es:'es'})[state.language] || 'en';
  document.querySelectorAll('[data-i18n]').forEach(node => { node.textContent = words()[node.dataset.i18n]; });
  document.querySelectorAll('[data-i18n-html]').forEach(node => { node.innerHTML = words()[node.dataset.i18nHtml]; });
  $('language').value = state.language;
  $('footer-guide').href = state.language === 'zh' ? '/docs/guide-zh' : '/docs/guide';
  document.querySelector('.footer-links').setAttribute('aria-label', words().footerResources);
  applyTheme();
  if (document.body.dataset.wizardReady) updateWizard();
  $('brand').placeholder=ui('appPlaceholder');
  $('description').placeholder=ui('descriptionPlaceholder');
  $('design-prompt').placeholder=ui('designPlaceholder');
  $('language').setAttribute('aria-label',ui('interfaceLanguage'));
  document.querySelector('.language-select .visually-hidden').textContent=ui('interfaceLanguage');
  Array.from($('language').options).forEach(option=>{option.textContent=languageLabel(option.value);});
  $('api-key').placeholder = words().apiKeyExample;
  $('model-custom').placeholder = words().modelExample;
  if (state.options) { renderDesignControls(); renderStyles(); renderLocales(); renderProviders(); }
}

$('language').addEventListener('change', () => { state.language = $('language').value; localStorage.setItem('nimoteshot-language', state.language); translate(); if(editingProposal)showDesignEditor(); });
$('theme').addEventListener('click', () => { state.theme = state.theme === 'dark' ? 'light' : 'dark'; localStorage.setItem('nimoteshot-theme', state.theme); applyTheme(); });

function renderStyles() {
  const selected = document.querySelector('input[name="design-style"]:checked')?.value || localStorage.getItem('nimoteshot-style') || state.options.styles.default;
  $('style-list').replaceChildren();
  state.options.styles.styles.filter(style => !$('app-category').value || style.category === $('app-category').value).forEach((style, index) => {
    const label = document.createElement('label'); label.className = 'style-card';
    const input = document.createElement('input'); input.type = 'radio'; input.name = 'design-style'; input.value = style.id; input.checked = style.id === selected || (index === 0 && !state.options.styles.styles.some(item => item.id === selected && (!$('app-category').value || item.category === $('app-category').value)));
    input.addEventListener('change', () => localStorage.setItem('nimoteshot-style', style.id));
    const swatch = document.createElement('span'); swatch.className = 'style-swatch';
    style.swatches.forEach(color => { const item = document.createElement('i'); item.style.background = color; swatch.append(item); });
    const name = document.createElement('strong'); name.textContent = catalogText(style,'name');
    const description = document.createElement('small'); description.textContent = catalogText(style,'description');
    label.append(input, swatch, name, description); $('style-list').append(label);
  });
}

function renderDesignControls() {
  const zh = state.language === 'zh';
  const category = $('app-category').value;
  const preset = $('prompt-preset').value;
  const categories = new Map(state.options.styles.styles.filter(item => item.category).map(item => [item.category, catalogText(item,'category')]));
  $('app-category').replaceChildren(new Option(ui('allPalettes',{count:state.options.styles.styles.length}), ''), ...Array.from(categories, ([id, name]) => new Option(name, id)));
  $('app-category').value = category;
  $('prompt-preset').replaceChildren(new Option(ui('customDirection'), ''), ...state.options.styles.prompt_presets.map(item => new Option(catalogText(item,'name'), item.id)));
  $('prompt-preset').value = preset;
  updatePromptDescription();
}
function updatePromptDescription() {
  const preset = state.options?.styles.prompt_presets.find(item => item.id === $('prompt-preset').value);
  $('preset-description').textContent=preset?catalogText(preset,'prompt'):ui('presetHelp');
}
$('prompt-preset').addEventListener('change', updatePromptDescription);
$('app-category').addEventListener('change', renderStyles);

function renderLocales() {
  const selected = new Set(JSON.parse(localStorage.getItem('nimoteshot-locales') || '["zh-CN"]'));
  $('locale-list').replaceChildren();
  Object.keys(localeCodes).forEach(id => {
    const locked=id==='en-US';
    const unavailable=state.options.text_shaping===false&&state.options.output_locales?.[id]?.requires_shaping;
    const label = locked ? words().englishDefault : languageLabel(id);
    const option = document.createElement('label'); option.className = 'locale-option';
    if (locked) option.classList.add('locked');
    const input = document.createElement('input'); input.type = 'checkbox'; input.value = id; input.checked = locked || (!unavailable&&selected.has(id)); input.disabled = Boolean(locked||unavailable);
    if(unavailable)option.title=ui('shapingUnavailable');
    input.addEventListener('change', () => localStorage.setItem('nimoteshot-locales', JSON.stringify(Array.from(document.querySelectorAll('#locale-list input:checked'), item => item.value))));
    option.append(input, document.createTextNode(label)); $('locale-list').append(option);
  });
  if(state.options.text_shaping===false){
    const note=document.createElement('p');note.id='language-availability';note.textContent=ui('shapingUnavailable')+' ';
    const link=document.createElement('a');link.textContent=ui('textSetup');link.href=state.language==='zh'?'/docs/guide-zh#语言支持':'/docs/guide#languages';link.target='_blank';link.rel='noopener';note.append(link);$('locale-list').append(note);
  }
}

function selectedProvider() { return state.options.models.providers.find(item => item.id === $('provider').value); }

function configurationMessage(provider) {
  if (provider.protocol === 'codex_cli') return words().configCodex;
  if (provider.protocol === 'ollama') return words().configOllama;
  const source = state.options.credential_source[provider.id];
  if (source === 'environment') return words().configEnvironment;
  if (source === 'profile') return words().configProfile;
  return words().configPage;
}

function renderProviders() {
  const remembered = $('provider').value || localStorage.getItem('nimoteshot-provider') || state.options.models.default_provider;
  $('provider').replaceChildren();
  state.options.models.providers.forEach(provider => { const option = document.createElement('option'); option.value = provider.id; option.textContent = catalogText(provider,'label'); $('provider').append(option); });
  $('provider').value = state.options.models.providers.some(item => item.id === remembered) ? remembered : state.options.models.default_provider;
  renderModels();
}

function renderModels() {
  const provider = selectedProvider(); if (!provider) return;
  const providerChanged = state.lastProvider !== null && state.lastProvider !== provider.id;
  const previous = $('model-select').value;
  $('model-select').replaceChildren();
  provider.models.forEach(model => { const option = document.createElement('option'); option.value = model.id; option.textContent = `${model.label} · ${catalogText(model,'note')}`; $('model-select').append(option); });
  if (provider.models.some(model => model.id === previous)) $('model-select').value = previous;
  $('model-select').disabled = provider.models.length === 0;
  $('model-select').closest('.field').classList.toggle('hidden', provider.models.length === 0);
  $('key-field').classList.toggle('hidden', provider.protocol === 'ollama' || provider.protocol === 'codex_cli');
  if (state.lastProvider !== provider.id) {
    const saved = state.options.profiles?.[provider.id];
    $('base-url').value = saved?.base_url || provider.base_url || '';
    $('model-custom').value = saved?.model || '';
  }
  if (providerChanged) { $('api-key').value = ''; }
  $('base-url').placeholder = provider.protocol === 'ollama' ? 'http://127.0.0.1:11434' : 'https://api.example.com/v1';
  $('advanced').open = Boolean($('model-custom').value) || provider.models.length === 0 || provider.id === 'compatible';
  $('key-note').textContent = provider.env ? `${ui('environmentVariable')}: ${provider.env}` : '';
  $('model-help').textContent = provider.id === 'openai' ? words().openaiAccount : provider.models.length === 0 ? (provider.id === 'compatible' ? words().customProvider : words().endpointModel) : '';
  $('config-source').textContent = configurationMessage(provider);
  $('copy-config').classList.toggle('hidden', provider.protocol === 'ollama');
  $('readiness-text').textContent = words().readiness; $('readiness').classList.remove('ready');
  state.lastProvider = provider.id;
}

$('provider').addEventListener('change', () => { localStorage.setItem('nimoteshot-provider', $('provider').value); renderModels(); });
['check', 'save-config', 'copy-config', 'generate'].forEach(id => $(id).disabled = true);
fetch('/api/options').then(response => { if (!response.ok) throw new Error('Could not load configuration. Refresh the page after checking the local server.'); return response.json(); }).then(data => {
  state.options = data;
  if(data.output_locales){Object.keys(localeCodes).forEach(id=>delete localeCodes[id]);Object.entries(data.output_locales).forEach(([id,options])=>localeCodes[id]=options.code);}
  translate();
  ['check', 'save-config', 'copy-config', 'generate'].forEach(id => $(id).disabled = false);
}).catch(error => showError(error.message));
translate();

function initDemoCarousel() {
  const gallery = $('demo-gallery');
  const previous = $('demo-previous');
  const next = $('demo-next');
  const dots = $('demo-dots');
  const carousel = document.querySelector('.demo-carousel');
  if (!gallery || !previous || !next || !dots || !carousel) return;
  const slides = Array.from(gallery.querySelectorAll('img'));
  const viewport = gallery.parentElement;
  let index = 0;
  const visible = () => Math.max(1, Math.floor((gallery.parentElement.clientWidth + Number.parseFloat(getComputedStyle(gallery).gap || '0')) / slideDistance()));
  const maxIndex = () => Math.max(0, slides.length - visible());
  const slideDistance = () => (slides[0].getBoundingClientRect().width || 166) + Number.parseFloat(getComputedStyle(gallery).gap || '0');
  const renderDots = () => {
    dots.replaceChildren(...Array.from({length: maxIndex() + 1}, (_, position) => {
      const dot = document.createElement('button'); dot.type = 'button'; dot.className = 'carousel-dot';
      dot.setAttribute('aria-label', `Show example ${position + 1}`); dot.setAttribute('aria-current', String(position === index));
      dot.addEventListener('click', () => { index = position; update(); }); return dot;
    }));
  };
  const update = () => {
    index = Math.min(index, maxIndex());
    viewport.scrollTo({left: index * slideDistance(), behavior: 'instant'});
    Array.from(dots.children).forEach((dot, position) => dot.setAttribute('aria-current', String(position === index)));
  };
  const move = direction => { index = direction > 0 ? (index >= maxIndex() ? 0 : index + 1) : (index <= 0 ? maxIndex() : index - 1); update(); };
  previous.addEventListener('click', () => { move(-1); });
  next.addEventListener('click', () => { move(1); });
  viewport.addEventListener('scroll', () => {
    index = Math.min(maxIndex(), Math.round(viewport.scrollLeft / slideDistance()));
    Array.from(dots.children).forEach((dot, position) => dot.setAttribute('aria-current', String(position === index)));
  });
  new ResizeObserver(() => { renderDots(); update(); }).observe(viewport);
  slides.forEach(slide => slide.addEventListener('load', () => { renderDots(); update(); }));
  renderDots(); update();
}

initDemoCarousel();

const wizardSteps = ['product', 'captures', 'style', 'model'];
let currentStep = 0;
const visitedSteps = new Set();
function updateWizard() {
  const zh = state.language === 'zh';
  const labels = [words().stepProduct, words().stepCaptures, words().stepStyle, words().stepModel];
  const hints=['productHint','captureHint','styleHint','modelHint'].map(key=>ui(key));
  wizardSteps.forEach((id, index) => { $(id).classList.toggle('hidden', index !== currentStep); });
  document.querySelectorAll('[data-step-target]').forEach((button, index) => {
    button.closest('li').classList.toggle('active', index === currentStep);
    button.closest('li').classList.toggle('visited', visitedSteps.has(index) && index !== currentStep);
    if (index === currentStep) button.setAttribute('aria-current', 'step'); else button.removeAttribute('aria-current');
    button.setAttribute('aria-controls', wizardSteps[index]);
  });
  $('step-counter').textContent = ui('stepCount',{current:currentStep+1});
  $('step-guidance').textContent = hints[currentStep];
  $('step-summary').textContent = ui('stepKeep');
  $('step-back').textContent = ui('stepBack');
  $('step-back').disabled = currentStep === 0;
  $('step-next').classList.toggle('hidden', currentStep === 3);
  $('step-next').textContent = ui('stepNext',{name:labels[currentStep+1]||''});
  document.querySelector('.submit').classList.toggle('hidden', currentStep !== 3);
}
function goToStep(index, focus = true) {
  visitedSteps.add(currentStep); currentStep = index;
  $('step-error').textContent = ''; clearError(); updateWizard();
  if (focus) { $(wizardSteps[index]).focus({preventScroll: true}); $('workspace').scrollIntoView({block: 'start', behavior: 'instant'}); }
}
function validateStep(index) {
  const fail = (id, message) => { goToStep(index); $('step-error').textContent = message; $(id).focus(); return false; };
  if (index === 0) {
    if (!$('brand').value.trim()) return fail('brand', state.language === 'zh' ? '请先填写应用名称。' : 'Enter your app name.');
    if (!$('description').value.trim() && !$('website').value.trim()) return fail('description', words().missingInfo);
    if ($('website').value && !$('website').validity.valid) return fail('website', state.language === 'zh' ? '请输入完整的网址，例如 https://example.com。' : 'Enter a full URL, such as https://example.com.');
  }
  if (index === 1) {
    if (!$('files').files.length) return fail('files', words().missingFiles);
    if (!$('files').files.length || $('files').files.length > 40) return fail('files', words().tooMany);
    if (!document.querySelector('.export-targets input:checked')) { goToStep(1); $('step-error').textContent = words().missingTargets; document.querySelector('.export-targets input').focus(); return false; }
  }
  return true;
}
$('step-next').addEventListener('click', () => { if (validateStep(currentStep)) goToStep(Math.min(currentStep + 1, 3)); });
$('step-back').addEventListener('click', () => goToStep(Math.max(0, currentStep - 1)));
document.querySelectorAll('[data-step-target]').forEach((button, index) => button.addEventListener('click', () => goToStep(index)));
document.body.dataset.wizardReady = 'true';
updateWizard();

$('copy-config').addEventListener('click', async () => {
  const provider = selectedProvider();
  const command = provider.protocol === 'codex_cli' ? 'codex login' : `python scripts/nimoteshot.py configure --provider ${provider.id} --prompt-api-key --verify`;
  const prompt = `Set up NimoteShot to use ${provider.label_en}. Do not reveal or paste secrets into chat. In a terminal, run:\n\n${command}\n\nThen return to NimoteShot and choose “Check setup”.`;
  try { await navigator.clipboard.writeText(prompt); $('copy-config').textContent = words().copied; window.setTimeout(() => { $('copy-config').textContent = words().copyConfig; }, 1400); } catch { showError(prompt); }
});

$('save-config').addEventListener('click', async () => {
  clearError(); const fields = requestFields(); const button = $('save-config');
  button.disabled = true; $('config-status').textContent = words().configTesting;
  try {
    const response = await fetch('/api/configure', {method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify(fields)});
    const result = await response.json(); if (!response.ok) throw new Error(result.error || 'Configuration failed');
    $('config-status').textContent = `${words().configSaved} · ${result.model}`;
    state.options.credential_source[fields.provider] = 'profile';
    state.options.profiles[fields.provider] = {model: fields.model, base_url: fields.base_url};
    $('config-source').textContent = configurationMessage(selectedProvider());
  } catch (error) { $('config-status').textContent = ''; showModelError(error.message); }
  finally { button.disabled = false; }
});

// Workflow labels describe planning separately from validated export.
Object.assign(copy.zh, {generate:'分析并生成方案',submitNote:'先预览和微调，再批量导出 PNG / ZIP。',capturesNote:'支持 1–40 张 PNG、JPEG、WebP。设备与语言变体会按功能归组。',dropTitle:'选择 PNG、JPEG、WebP，或拖放到这里',missingFiles:'请上传至少一张 PNG、JPEG 或 WebP。',tooMany:'最多上传 40 张截图。',providerNote:'默认 DeepSeek Flash，也支持现有云端与本地视觉模型。',configPage:'密钥仅保留在当前页面内存中，发送到本地服务及所选模型；只有点击保存配置才会写入本机。',resultTitle:'预览与微调'});
Object.assign(copy.en, {generate:'Analyze and plan',submitNote:'Preview and refine, then export PNG / ZIP.',capturesNote:'Add 1–40 PNG, JPEG or WebP captures. Device and language variants are grouped by feature.',dropTitle:'Choose PNG, JPEG or WebP files, or drop them here',missingFiles:'Add at least one PNG, JPEG or WebP capture.',tooMany:'Upload at most 40 captures.',providerNote:'DeepSeek Flash is the default. Existing cloud and local vision providers remain available.',configPage:'Keys stay in page memory and are sent to your local service and selected provider. Only Save configuration persists them locally.',resultTitle:'Preview and refine'});
translate();
const input = $('files'); const zone = $('dropzone');
let selectedFiles = [];
let previewUrls = [];
const uploadMessage = () => ui('uploadInvalid');
function showFiles() {
  invalidateDesign();
  previewUrls.forEach(url => URL.revokeObjectURL(url)); previewUrls = [];
  const transfer = new DataTransfer(); selectedFiles.forEach(file => transfer.items.add(file)); input.files = transfer.files;
  $('file-list').replaceChildren();
  selectedFiles.forEach((file, index) => {
    const card = document.createElement('div'); card.className = 'upload-card';
    const image = document.createElement('img'); image.alt = ''; image.src = URL.createObjectURL(file); previewUrls.push(image.src);
    const name = document.createElement('span'); name.textContent = file.name;
    const remove = document.createElement('button'); remove.type = 'button'; remove.textContent = '×';
    const label = ({zh:'移除', en:'Remove', ja:'削除', ko:'삭제', es:'Eliminar'})[state.language] || 'Remove';
    remove.setAttribute('aria-label', `${label} ${file.name}`);
    remove.addEventListener('click', () => { selectedFiles.splice(index, 1); showFiles(); const buttons = $('file-list').querySelectorAll('button'); (buttons[Math.min(index, buttons.length - 1)] || input).focus(); });
    card.append(image, name, remove); $('file-list').append(card);
  });
}
function addFiles(files) {
  const incoming = Array.from(files);
  const merged = [...selectedFiles];
  for (const file of incoming) {
    if (!merged.some(item => item.name === file.name && item.size === file.size && item.lastModified === file.lastModified)) merged.push(file);
  }
  if (incoming.some(file => !/\.(png|jpe?g|webp)$/i.test(file.name)) || merged.length > 40 || new Set(merged.map(file=>file.name.toLowerCase())).size !== merged.length) {
    $('upload-error').textContent = uploadMessage(); showFiles(); return;
  }
  $('upload-error').textContent = ''; selectedFiles = merged; showFiles();
}
input.addEventListener('change', () => addFiles(input.files));
['dragenter', 'dragover'].forEach(name => zone.addEventListener(name, event => { event.preventDefault(); zone.classList.add('dragging'); }));
['dragleave', 'drop'].forEach(name => zone.addEventListener(name, event => { event.preventDefault(); zone.classList.remove('dragging'); }));
zone.addEventListener('drop', event => { addFiles(event.dataTransfer.files); });

function showError(message) { $('error').textContent = localizeFailure(message); $('error').classList.remove('hidden'); }
function clearError() { $('error').classList.add('hidden'); $('error').textContent = ''; }
function requestFields() { return { analysis_language: state.language, brand: $('brand').value.trim(), description: $('description').value.trim(), website_url: $('website').value.trim(), design_prompt: [state.options?.styles.prompt_presets.find(item => item.id === $('prompt-preset').value)?.prompt, $('design-prompt').value.trim()].filter(Boolean).join('\n\n'), locales: Array.from(document.querySelectorAll('#locale-list input:checked:not(:disabled)'), item => item.value), source_profile: document.querySelector('input[name="source-profile"]:checked')?.value || 'iphone_portrait', targets: Array.from(document.querySelectorAll('.export-targets input:checked'), item => item.value), style: document.querySelector('input[name="design-style"]:checked')?.value || 'editorial', provider: $('provider').value, model: $('model-custom').value.trim() || $('model-select').value, base_url: $('base-url').value.trim(), api_key: $('api-key').value }; }
async function preflight(modelOnly = false) { clearError(); const fields = requestFields(); if (!modelOnly && !fields.brand) { $('brand').focus(); throw new Error(words().appName); } if (!modelOnly && !fields.description && !fields.website_url) { $('description').focus(); throw new Error(words().missingInfo); } if (!modelOnly && !fields.targets.length) throw new Error(words().missingTargets); $('readiness-text').textContent = words().checking; const response = await fetch(modelOnly ? '/api/check-model' : '/api/preflight', { method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify(fields) }); const result = await response.json(); if (!response.ok) throw new Error(result.error || 'Preflight failed'); $('readiness-text').textContent = `${result.message} · ${result.model}`; $('readiness').classList.add('ready'); return fields; }
$('check').addEventListener('click', async () => {
  $('check').disabled = true; $('model-diagnostic').classList.add('hidden');
  try { await preflight(true); } catch (error) { showModelError(error.message); }
  finally { $('check').disabled = false; }
});
function showModelError(message) {
  const zh = state.language === 'zh';
  const rules = [
    [/401|403|key|credential/i, '密钥缺失、无效或权限不足。检查当前服务商密钥和模型授权，再重试。', 'The key may be missing, invalid, or unauthorized. Check the provider key and model permissions, then retry.'],
    [/404|model.*(missing|ID|not found)/i, '模型或接口路径可能不正确。核对模型 ID、接入点及基础地址；本地模型请先安装。', 'Check the model ID, endpoint and base URL. Install the selected model if using Ollama.'],
    [/429|quota|rate/i, '可能达到额度或请求频率限制。检查服务商余额与配额，稍后重试。', 'Check provider balance and quotas; wait before retrying.'],
    [/timeout|reach|fetch|network|running|connect/i, '连接未完成。检查本地服务、网络、代理和接口地址，再重试。', 'Check the local service, network, proxy and endpoint, then retry.'],
    [/https|URL/i, '接口地址格式不正确。云服务使用 HTTPS，Ollama 使用本机地址。', 'Use an HTTPS cloud endpoint, or a localhost address for Ollama.'],
    [/codex/i, '检查 CLI 安装与登录状态，在终端完成登录后重试。', 'Check the CLI installation and sign in from the terminal before retrying.']
  ];
  const match = rules.find(([pattern]) => pattern.test(message));
  const diagnostic = $('model-diagnostic'); diagnostic.replaceChildren();
  const title = document.createElement('strong'); title.textContent = zh ? '配置未通过检查' : 'Configuration needs attention';
  const help = document.createElement('p'); help.textContent = match ? match[zh ? 1 : 2] : (zh ? '请核对服务商、模型和接口配置。下面保留原始错误，便于定位；修正后重新检查。' : 'Review the provider, model and endpoint. Use the original error below to diagnose, then check again.');
  const detail = document.createElement('p'); detail.textContent = message;
  diagnostic.append(title, help, detail); diagnostic.classList.remove('hidden');
  $('readiness').classList.remove('ready'); $('readiness-text').textContent = title.textContent;
}
['api-key', 'model-select', 'model-custom', 'base-url'].forEach(id => $(id).addEventListener('input', () => { $('readiness').classList.remove('ready'); $('readiness-text').textContent = words().readiness; }));
const toBase64 = file => new Promise((resolve, reject) => { const reader = new FileReader(); reader.onload = () => resolve(reader.result.split(',')[1]); reader.onerror = reject; reader.readAsDataURL(file); });
function renderTrace(events = []) { $('agent-trace').replaceChildren(...events.slice(-8).map(event => { const item = document.createElement('li'); item.textContent = localizeProgress(event.message); return item; })); }
const targetLabels = {iphone_portrait: 'targetIphone', iphone_landscape: 'targetIphoneLandscape', ipad_portrait: 'targetTabletPortrait', ipad_landscape: 'targetTablet', android_portrait: 'targetAndroid', android_landscape: 'targetAndroidLandscape'};
function renderPreviews(result) {
  const previews = $('result-previews'); previews.replaceChildren();
  (result.targets || []).forEach(target => {
    const path = result.previews?.[target]; if (!path) return;
    const link = document.createElement('a'); link.className = 'preview-card'; link.href = `/files/${path.split('/').map(encodeURIComponent).join('/')}`; link.target = '_blank'; link.rel = 'noopener';
    const image = document.createElement('img'); image.loading = 'lazy'; image.alt = `${words()[targetLabels[target]] || target} overview`; image.src = link.href;
    const label = document.createElement('span'); label.textContent = words()[targetLabels[target]] || target;
    link.append(image, label); previews.append(link);
  });
}
async function poll(jobId) { for (;;) { await sleep(900); const response = await fetch(`/api/jobs/${jobId}`); const job = await response.json(); const percent=Math.max(0,Math.min(100,Number(job.progress)||0));$('export-progress').value=percent;$('export-progress-value').textContent=`${percent}%`;$('progress-title').textContent = localizeProgress(job.message) || words().working; renderTrace(job.events); if (job.status === 'error') throw new Error(job.message); if (job.status === 'complete') return job.result; } }

let editingProposal = null;
let previewTimer, previewRevision = 0, previewController;
const pendingPreviewIndices = new Set();
let editorLocale = 'en', editorTarget = 'iphone_portrait', busy = false;
const localeCodes = {'en-US':'en','zh-CN':'zh','ja-JP':'ja','ko-KR':'ko','es-ES':'es'};
function ui(key,parameters={}) { return Object.entries(parameters).reduce((text,[name,value])=>text.replaceAll('{'+name+'}',String(value)),editorMessages[state.language]?.[key]||editorMessages.en[key]||key); }
const encodedFiles = new WeakMap();
const sourcePreviewUrls = new WeakMap();
function sourcePreview(file) {
  if (!sourcePreviewUrls.has(file)) sourcePreviewUrls.set(file,URL.createObjectURL(file));
  return sourcePreviewUrls.get(file);
}
async function uploadFiles() {
  return Promise.all(selectedFiles.map(async file=>{
    if (!encodedFiles.has(file)) encodedFiles.set(file,toBase64(file));
    return {name:file.name,data:await encodedFiles.get(file)};
  }));
}
function invalidateDesign() {
  editingProposal = null; ++previewRevision; clearTimeout(previewTimer); previewController?.abort();pendingPreviewIndices.clear();
  $('result').classList.add('hidden');
}
function markEdited(screenIndex = null) {
  $('download').classList.add('hidden');
  $('open-export').classList.add('hidden');
  $('export-location').classList.add('hidden');
  $('result-summary').textContent = ui('changed');
  queueDesignPreview(screenIndex === null ? null : [screenIndex]);
}
function manualProposal(files) {
  return {schema_version:1,screens:files.slice(0,10).map(file=>{
    const screen={file:file.name,title_en:['Your feature'],subtitle_en:'Describe what is visible',design:{template:'balanced',background:0}};
    Object.entries(localeCodes).forEach(([locale,code])=>{const options=state.options.output_locales?.[locale],messages=editorMessages[code]||editorMessages.en;screen['title_'+code]=[options?.placeholder_title||messages.featurePlaceholder];screen['subtitle_'+code]=options?.placeholder_subtitle||messages.visiblePlaceholder;});
    return screen;
  })};
}
async function runJob(route, fields) {
  const response = await fetch(route,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(fields)});
  const accepted=await response.json();if(!response.ok)throw new Error(accepted.error||'Request failed');
  return poll(accepted.job_id);
}
async function withProgress(task) {
  if(busy)return;
  busy=true;if($('design-editor'))$('design-editor').inert=true;clearError();$('generate').disabled=true;$('export-progress').value=0;$('export-progress-value').textContent='0%';$('progress').classList.remove('hidden');
  document.querySelectorAll('[data-design-action]').forEach(button=>button.disabled=true);
  try {await task();}
  catch(error){showError(error.message);$('error').scrollIntoView({behavior:'smooth',block:'center'});}
  finally {busy=false;if($('design-editor'))$('design-editor').inert=false;$('generate').disabled=false;$('progress').classList.add('hidden');document.querySelectorAll('[data-design-action]').forEach(button=>button.disabled=false);}
}
async function createPlan(refresh=false) {
  const fields=requestFields(); fields.files=await uploadFiles(); fields.refresh=refresh;
  const result=await runJob('/api/plan',fields);
  editingProposal=result.proposal;showDesignEditor();
}
$('studio-form').addEventListener('submit',async event=>{
  event.preventDefault();
  if(currentStep<3){if(validateStep(currentStep))goToStep(currentStep+1);return;}
  if(!validateStep(0)||!validateStep(1))return;
  await withProgress(async()=>{
    if($('manual-mode').checked){editingProposal=manualProposal(selectedFiles);showDesignEditor();}
    else await createPlan();
    $('result').scrollIntoView({behavior:'smooth',block:'start'});
  });
});
function actionButton(text,action) {
  const button=document.createElement('button');button.type='button';button.className='button quiet';button.dataset.designAction='true';button.textContent=text;
  button.onclick=()=>withProgress(action);return button;
}
function selectControl(label, options, value, changed) {
  const wrapper=document.createElement('label');wrapper.className='field';
  const caption=document.createElement('span');caption.textContent=label;
  const select=document.createElement('select');select.setAttribute('aria-label',label);
  options.forEach(([id,text])=>{const option=document.createElement('option');option.value=id;option.textContent=text;select.append(option);});
  select.value=value;select.onchange=()=>changed(select.value);wrapper.append(caption,select);return wrapper;
}
function showDesignEditor(previewIndices = null) {
  // A template change rebuilds its controls but keeps the other rendered images.
  const previousImages=previewIndices === null ? [] : Array.from(document.querySelectorAll('.design-rendered-preview'));
  ++previewRevision; previewController?.abort();
  let panel=$('design-editor');if(!panel){panel=document.createElement('div');panel.id='design-editor';$('result').append(panel);}
  panel.replaceChildren();$('result').classList.remove('hidden');$('download').classList.add('hidden');$('open-export').classList.add('hidden');$('export-location').classList.add('hidden');$('result-previews').replaceChildren();
  $('result-summary').textContent=ui('designReady');
  const heading=$('result').querySelector('h2');heading.textContent=ui('refine');
  const selected=requestFields();
  let addedLanguage=false;
  selected.locales.forEach(locale=>{
    const code=localeCodes[locale],options=state.options.output_locales?.[locale],messages=editorMessages[code]||editorMessages.en;
    editingProposal.screens.forEach(screen=>{
      if(!Object.hasOwn(screen,'title_'+code)){screen['title_'+code]=[options?.placeholder_title||messages.featurePlaceholder];addedLanguage=true;}
      if(!Object.hasOwn(screen,'subtitle_'+code)){screen['subtitle_'+code]=options?.placeholder_subtitle||messages.visiblePlaceholder;addedLanguage=true;}
    });
  });
  if(addedLanguage)$('result-summary').textContent=ui('addedLanguage');
  const languages=['en-US',...selected.locales];if(!languages.some(locale=>localeCodes[locale]===editorLocale))editorLocale='en';
  if(!selected.targets.includes(editorTarget))editorTarget=selected.targets[0];
  const toolbar=document.createElement('div');toolbar.className='design-toolbar';
  const copyVersion=selectControl(ui('copyLocale'),languages.map(locale=>[localeCodes[locale],languageLabel(locale)]),editorLocale,value=>{editorLocale=value;showDesignEditor();});
  copyVersion.querySelector('select').id='copy-language';copyVersion.querySelector('select').setAttribute('aria-describedby','copy-language-help');
  toolbar.append(copyVersion,selectControl(ui('previewDevice'),selected.targets.map(id=>[id,words()[targetLabels[id]]||id]),editorTarget,value=>{editorTarget=value;queueDesignPreview();}));
  const accentLabel=document.createElement('label');accentLabel.className='field';accentLabel.textContent=ui('accent');
  const accent=document.createElement('input');accent.type='color';accent.setAttribute('aria-label',ui('accent'));accent.value=editingProposal.brand_accent||state.options.styles.styles.find(s=>s.id===selected.style)?.colors.accent||'#6554e8';accent.oninput=()=>{editingProposal.brand_accent=accent.value;markEdited();};accentLabel.append(accent);toolbar.append(accentLabel);panel.append(toolbar);
  const languageHelp=document.createElement('p');languageHelp.id='copy-language-help';languageHelp.textContent=ui('copyLocaleHelp');panel.append(languageHelp);
  const previewBar=document.createElement('div');previewBar.className='design-preview-status';
  const status=document.createElement('p');status.id='preview-status';status.setAttribute('role','status');
  const retry=document.createElement('button');retry.type='button';retry.id='retry-preview';retry.className='button quiet hidden';retry.textContent=ui('retryPreview');retry.onclick=()=>queueDesignPreview([]);
  previewBar.append(status,retry);panel.append(previewBar);
  editingProposal.screens.forEach((screen,index)=>{
    const row=document.createElement('fieldset');row.className='design-screen';
    const legend=document.createElement('legend');legend.textContent=`${index+1}. ${screen.file}`;row.append(legend);
    const editorBody=document.createElement('div');editorBody.className='design-screen-body';
    const source=document.createElement('figure');source.className='design-source';
    const sourceFile=selectedFiles.find(file=>file.name===screen.file);
    const preview=previousImages[index]||document.createElement('img');preview.className='design-rendered-preview';preview.hidden=!preview.getAttribute('src');source.append(preview);
    const sourceCaption=document.createElement('figcaption');sourceCaption.textContent=ui('livePreview');source.append(sourceCaption);
    if(sourceFile){
      const original=document.createElement('details');original.className='design-original';
      const summary=document.createElement('summary');summary.textContent=ui('sourceCapture');
      const image=document.createElement('img');image.src=sourcePreview(sourceFile);image.alt=`${ui('sourceCapture')}: ${screen.file}`;
      original.append(summary,image);source.append(original);
    }
    editorBody.append(source);
    const configuration=document.createElement('div');configuration.className='design-configuration';
    const details=document.createElement('details');const summary=document.createElement('summary');summary.textContent=ui('evidence');
    const evidence=document.createElement('p');evidence.textContent=screen.analysis?.evidence||ui('manualEvidence');
    const uncertainty=document.createElement('p');uncertainty.textContent=screen.analysis?.uncertainty||'';details.append(summary,evidence,uncertainty);configuration.append(details);
    const copyGrid=document.createElement('div');copyGrid.className='field-grid';
    ['title','subtitle'].forEach(type=>{
      const key=`${type}_${editorLocale}`;
      const label=document.createElement('label');label.className='field';const text=document.createElement('span');text.textContent=type==='title'?ui('editTitle'):ui('editSubtitle');
      const field=document.createElement(type==='title'?'textarea':'input');if(type==='title')field.rows=2;
      field.value=Array.isArray(screen[key])?screen[key].join('\n'):screen[key]||'';field.setAttribute('aria-label',`${ui(type==='title'?'editTitle':'editSubtitle')} ${index+1} (${editorLocale})`);field.dataset.copyKey=key;field.dataset.screenIndex=String(index+1);field.maxLength=type==='title'?161:180;
      let composing=false;const updateCopy=()=>{screen[key]=type==='title'?field.value.split('\n').slice(0,2):field.value;markEdited(index);};
      field.oncompositionstart=()=>{composing=true;};
      field.oninput=event=>{if(!composing&&!event.isComposing)updateCopy();};field.oncompositionend=()=>{composing=false;updateCopy();};
      label.append(text,field);copyGrid.append(label);
    });configuration.append(copyGrid);
    const templates=Object.keys(state.options.templates).map(id=>[id,ui(id)]);
    const design=screen.design||(screen.design={template:'balanced',background:0});
    configuration.append(selectControl(ui('editTemplate'),templates,design.template,value=>{
      design.template=value;if(value==='detail')design.focus_region=design.focus_region||'center';
      if(value==='duo')design.secondary_file=selectedFiles.find(f=>f.name!==screen.file)?.name;
      showDesignEditor([index]);markEdited(index);
    }));
    const advanced=document.createElement('details');const advancedTitle=document.createElement('summary');advancedTitle.textContent=ui('advancedLayout');advanced.append(advancedTitle);
    [['scale',ui('screenshotSize'),['small','standard','large']],['alignment',ui('screenshotPosition'),['left','center','right']],['typography',ui('editorTypography'),['standard','compact']]].filter(([key])=>key==='typography'||!['detail','duo'].includes(design.template)).forEach(([key,label,values])=>{
      advanced.append(selectControl(label,values.map(value=>[value,ui(value)]),design[key]||({scale:'standard',alignment:'center',typography:'standard'})[key],value=>{design[key]=value;markEdited(index);}));
    });
    advanced.append(selectControl(ui('editorBackground'),[0,1,2,3].map(i=>[String(i),String(i+1)]),String(design.background||0),value=>{design.background=Number(value);markEdited(index);}));
    if(design.template==='detail')advanced.append(selectControl(ui('detailRegion'),['top','center','bottom'].map(v=>[v,ui(v)]),design.focus_region||'center',value=>{design.focus_region=value;markEdited(index);}));
    if(design.template==='duo')advanced.append(selectControl(ui('secondCapture'),selectedFiles.filter(f=>f.name!==screen.file).map(f=>[f.name,f.name]),design.secondary_file,value=>{design.secondary_file=value;markEdited(index);}));
    configuration.append(advanced);
    const moves=document.createElement('div');moves.className='design-actions';
    [-1,1].forEach(delta=>{const move=document.createElement('button');move.type='button';move.className='button quiet';move.textContent=delta<0?'↑':'↓';move.setAttribute('aria-label',`${ui(delta<0?'moveUp':'moveDown')} ${index+1}`);move.disabled=index+delta<0||index+delta>=editingProposal.screens.length;
      move.onclick=()=>{const screens=editingProposal.screens;[screens[index],screens[index+delta]]=[screens[index+delta],screens[index]];showDesignEditor();markEdited();};moves.append(move);});configuration.append(moves);editorBody.append(configuration);row.append(editorBody);panel.append(row);
  });
  const actions=document.createElement('div');actions.className='design-actions';
  if(editingProposal.screens.every(screen=>screen.analysis?.evidence?.trim())){
    const optional=document.createElement('details');optional.className='design-rework';
    const summary=document.createElement('summary');summary.textContent=ui('optionalRework');optional.append(summary);
    [['regenerateCopy','copyHelp',()=>regenerate('copy')],['recommendLayouts','layoutHelp',()=>regenerate('layout')],['reanalyze','reanalyzeHelp',()=>createPlan(true)]].forEach(([label,help,action])=>{
      const row=document.createElement('div');row.className='design-rework-action';
      const note=document.createElement('p');note.textContent=ui(help);row.append(actionButton(ui(label),action),note);optional.append(row);
    });panel.append(optional);
  }
  const exportButton=actionButton(ui('exportDesign'),exportDesign);exportButton.className='button primary';exportButton.id='export-design';actions.append(exportButton);panel.append(actions);
  queueDesignPreview(previewIndices);
}
async function regenerate(action) {
  const fields=requestFields();fields.files=await uploadFiles();fields.proposal=editingProposal;fields.action=action;
  const result=await runJob('/api/revise',fields);editingProposal=result.proposal;showDesignEditor();
}
async function exportDesign() {
  const revision=previewRevision;
  const fields=requestFields();fields.proposal=structuredClone(editingProposal);fields.files=await uploadFiles();fields.api_key='';
  const result=await runJob('/api/generate',fields);
  if(revision!==previewRevision){markEdited();return;}
  $('download').href=`/files/${encodeURIComponent(result.run_id)}/nimoteshot_${encodeURIComponent(result.run_id)}.zip`;$('download').classList.remove('hidden');
  $('export-path-label').textContent=ui('exportPath');$('export-path').textContent=result.output_path;$('export-location').classList.remove('hidden');
  $('open-export').textContent=ui('openExport');$('open-export').dataset.runId=result.run_id;$('open-export').classList.remove('hidden');
  $('result-summary').textContent=ui('exported',{screens:result.screens,targets:result.targets.length,locales:result.locales.length});
  renderPreviews(result);
}
$('open-export').addEventListener('click',async()=>{
  const button=$('open-export');button.disabled=true;
  try {const response=await fetch('/api/open-output',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({run_id:button.dataset.runId})});const result=await response.json();if(!response.ok)throw new Error(result.error);}
  catch(error){showError(error.message);}
  finally{button.disabled=false;}
});
function queueDesignPreview(indices = null) {
  clearTimeout(previewTimer);const revision=++previewRevision;previewController?.abort();
  if(!editingProposal)return;
  // Keep uncommitted screens across debounced edits, aborted requests and retries.
  (indices === null ? editingProposal.screens.map((_,index)=>index) : indices).forEach(index=>pendingPreviewIndices.add(index));
  const requestedIndices=Array.from(pendingPreviewIndices).filter(index=>index<editingProposal.screens.length).sort((a,b)=>a-b);
  if(!requestedIndices.length)return;
  const status=$('preview-status');if(status){status.textContent=ui('previewUpdating');status.dataset.state='loading';}
  $('retry-preview')?.classList.add('hidden');
  const images=Array.from(document.querySelectorAll('.design-rendered-preview'));
  requestedIndices.forEach(index=>images[index]?.classList.add('preview-stale'));
  previewTimer=setTimeout(async()=>{
    const controller=new AbortController();previewController=controller;
    try {
      const fields=requestFields();fields.proposal=structuredClone(editingProposal);fields.files=await uploadFiles();fields.preview_locale=Object.keys(localeCodes).find(locale=>localeCodes[locale]===editorLocale);fields.preview_target=editorTarget;fields.preview_indices=requestedIndices;fields.api_key='';
      if(revision!==previewRevision)return;
      const response=await fetch('/api/preview',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(fields),signal:controller.signal});
      const result=await response.json();if(!response.ok)throw new Error(result.error);
      if(revision!==previewRevision)return;
      if(JSON.stringify(result.indices)!==JSON.stringify(requestedIndices)||result.images.length!==requestedIndices.length)throw new Error('Invalid preview response');
      await Promise.all(result.images.map(async src=>{const decoded=new Image();decoded.src=src;await decoded.decode();}));
      if(revision!==previewRevision)return;
      result.images.forEach((src,offset)=>{
        const index=requestedIndices[offset],image=images[index];
        image.src=src;image.hidden=false;image.classList.remove('preview-stale');image.alt=`${ui('refine')}: ${editingProposal.screens[index].file} · ${result.locale} · ${words()[targetLabels[result.target]]||result.target}`;
      });
      pendingPreviewIndices.clear();
      if(status){status.textContent=ui('previewUpdated');status.dataset.state='ready';}
    }catch(error){if(error.name!=='AbortError'&&revision===previewRevision&&status){status.textContent=localizeFailure(error.message);status.dataset.state='error';$('retry-preview')?.classList.remove('hidden');}}
  },350);
}
document.addEventListener('change',event=>{
  if(!editingProposal)return;
  if(event.target.matches('input[name="design-style"], .export-targets input, #locale-list input'))showDesignEditor();
});

function localizeProgress(message='') {
  const exact={'Preparing captures':'preparing','Validating PNG/JPEG/WebP captures':'validating','Analyzing captures with AI':'analyzing','Reusing cached screenshot analysis':'cached','Revising copy from recorded visual evidence':'revisingCopy','Revising layout from recorded visual evidence':'revisingLayout','Archiving verified originals':'archiving','Packaging and validating ZIP':'packaging','Complete':'complete'};
  if(exact[message])return ui(exact[message]);
  const rendering=message.match(/^Rendering (.+) \/ (.+)$/);
  if(rendering)return ui('rendering',{locale:rendering[1],target:words()[targetLabels[rendering[2]]]||rendering[2]});
  return localizeFailure(message);
}
function localizeFailure(message='') {
  const rules=[[/No bundled font/i,'errorFont'],[/libraqm shaping/i,'errorShaping'],[/429|quota|rate limit/i,'errorRate'],[/timed out|timeout/i,'errorTimeout'],[/network|connect|fetch/i,'errorNetwork'],[/API.key|401|403|credential/i,'errorKey'],[/JSON|Invalid design|schema|mapping|omitted/i,'errorJson'],[/evidence|Analyze screenshots first/i,'errorEvidence'],[/fit|overflow|safe area|shorten/i,'errorCopy'],[/preview language|preview.*device/i,'errorPreview'],[/capture|image|base64|filename/i,'uploadInvalid']];
  return ui(rules.find(([pattern])=>pattern.test(message))?.[1]||'errorGeneric');
}
