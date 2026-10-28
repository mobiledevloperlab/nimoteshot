<p align="center">
  <img src="web/assets/nimoteshot-logo.svg" alt="NimoteShot" width="392">
</p>

<p align="center"><strong>Estudio de capturas para App Store</strong></p>

<p align="center">
  <a href="README.md">English</a> · <a href="README.zh-CN.md">简体中文</a> · <a href="README.ja.md">日本語</a> · <a href="README.ko.md">한국어</a> · Español
</p>

NimoteShot convierte capturas reales de producto en imágenes claras y localizadas para App Store y Google Play. Analiza capturas PNG, JPEG o WebP con un modelo de visión para preparar textos de tienda; la composición y la exportación se realizan en tu equipo.

## Vista previa

<table><tr>
<td width="56%" valign="top"><img src="web/assets/ui.png" alt="Página de inicio y ejemplo generado de NimoteShot" width="100%"><p align="center"><sub>Inicio y ejemplo de imágenes de tienda generadas</sub></p></td>
<td width="44%" valign="top"><img src="web/assets/snapshot.png" alt="Flujo de creación en cuatro pasos" width="100%"><p align="center"><sub>Flujo de creación local en cuatro pasos</sub></p></td>
</tr></table>

### Capturas reales → material para la tienda

<table><tr>
<td width="33.33%" align="center" valign="top"><strong>Editor de código móvil</strong><br><br><img src="demo/nimotecode/originals/code-editor.png" alt="Captura original del editor de código" width="47%"> <img src="demo/nimotecode/previews/01_feature.png" alt="Material generado para IDE móvil" width="47%"><br><sub>Captura original → material funcional generado</sub></td>
<td width="33.33%" align="center" valign="top"><strong>Espacio de trabajo SSH</strong><br><br><img src="demo/nimotecode/originals/ssh-workspace.png" alt="Captura original del espacio de trabajo SSH" width="47%"> <img src="demo/nimotecode/previews/03_feature.png" alt="Material generado para espacio de trabajo SSH" width="47%"><br><sub>Captura original → material funcional generado</sub></td>
<td width="33.33%" align="center" valign="top"><strong>Asistente de programación con IA</strong><br><br><img src="demo/nimotecode/originals/ai-assistant.png" alt="Captura original del asistente de IA" width="47%"> <img src="demo/nimotecode/previews/02_feature.png" alt="Material generado para asistente de IA" width="47%"><br><sub>Captura original → material funcional generado</sub></td>
</tr></table>

## Características

- Convierte entre 1 y 40 capturas reales PNG, JPEG o WebP en material de tienda localizado.
- Genera textos en inglés y, opcionalmente, chino, japonés, coreano y español.
- Admite tamaños de destino para iPhone, Android y iPad, en vertical y horizontal.
- Incluye cuatro estilos visuales, 28 paletas por categoría y sugerencias de diseño opcionales.
- Funciona como aplicación web local o herramienta de línea de comandos; el renderizado y la exportación permanecen en el equipo.

## Inicio rápido

### Linux y macOS

```bash
git clone <your-repository-url> nimoteshot
cd nimoteshot
./install.sh
```

### Windows PowerShell

```powershell
git clone <your-repository-url> nimoteshot
Set-Location nimoteshot
powershell -ExecutionPolicy Bypass -File .\install.ps1
```

El instalador comprueba Python 3.11 o posterior, crea `.venv`, instala las dependencias y abre el estudio. Para iniciarlo sin abrir el navegador, usa `./install.sh --no-browser`. Abre la dirección `http://127.0.0.1:8765` que se muestre; el servidor escucha solo en el bucle local.

## Uso del estudio

1. Introduce el nombre de la aplicación y una breve descripción del producto o una página HTTPS pública y fiable.
2. Sube entre 1 y 40 capturas PNG, JPEG o WebP reales sobre las que tengas derecho de uso.
3. Elige idiomas de salida, estilo, paleta y, si quieres, una indicación de diseño.
4. Selecciona un proveedor de visión y ejecuta **Check setup** antes de generar.
5. Haz clic en **Analyze and plan** para previsualizar y editar el texto de cada idioma.
6. Haz clic en **Export PNG / ZIP** para descargar imágenes validadas. Sin clave API, elige **Manual design** y escribe el texto manualmente.

Cada tarea se guarda en `store_screenshots/runs/<task-id>/` e incluye originales, `source_manifest.json`, un `config.json` editable, vistas previas, PNG y un ZIP. Antes de publicar, revisa las [especificaciones de capturas de Apple](https://developer.apple.com/help/app-store-connect/reference/app-information/screenshot-specifications/) y los [requisitos de imágenes de Google Play](https://support.google.com/googleplay/android-developer/answer/9866151).

## CLI

Coloca capturas PNG/JPEG/WebP en `screens/`, configura un proveedor y ejecuta:

```bash
.venv/bin/python scripts/nimoteshot.py generate \
  --brand "My App" \
  --description "Un editor móvil con herramientas SSH, Git y terminal" \
  --style editorial --provider qwen --locales es-ES
```

En Windows, sustituye `.venv/bin/python` por `.venv\Scripts\python.exe`. Consulta todas las opciones con `python scripts/nimoteshot.py --help`.

## Privacidad y seguridad

- El renderizado, empaquetado y exportación se realizan localmente. Las capturas y la descripción se envían al modelo elegido para su análisis.
- Las tareas generadas contienen capturas y texto de origen: trátalas como datos privados y elimínalas cuando ya no sean necesarias.
- La salida del modelo no es fiable. Revisa todos los textos, afirmaciones, traducciones y asignaciones de dispositivos antes de publicar.
- No subas claves API, perfiles locales, capturas privadas, tareas generadas ni archivos a tu repositorio.

Para desarrollo, resolución de problemas, requisitos de proveedores y la referencia técnica completa, consulta el [README en inglés](README.md).
