$ErrorActionPreference = 'Stop'
Set-Location $PSScriptRoot
if (Get-Command py -ErrorAction SilentlyContinue) { $python = 'py'; $pythonArgs = @('-3') }
elseif (Get-Command python -ErrorAction SilentlyContinue) { $python = 'python'; $pythonArgs = @() }
else { throw 'Python 3.11 or newer is required. Install it from python.org.' }
& $python @pythonArgs -c "import sys; assert sys.version_info >= (3,11), 'Python 3.11 or newer is required'"
if ($LASTEXITCODE -ne 0) { throw 'Python 3.11 or newer is required.' }
if (-not (Test-Path '.venv\Scripts\python.exe')) { & $python @pythonArgs -m venv .venv }
if ($LASTEXITCODE -ne 0) { throw 'Could not create virtual environment.' }
& '.venv\Scripts\python.exe' -c "import sys; assert sys.version_info >= (3,11), 'Recreate .venv with Python 3.11 or newer'"
if ($LASTEXITCODE -ne 0) { throw 'Recreate .venv with Python 3.11 or newer.' }
& '.venv\Scripts\python.exe' -m pip install -r store_screenshots/requirements.txt
if ($LASTEXITCODE -ne 0) { throw 'Dependency installation failed.' }
& '.venv\Scripts\python.exe' scripts/nimoteshot.py web @args
