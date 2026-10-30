#!/usr/bin/env python3
"""NimoteShot: local web UI and one-command AI generation."""
import argparse
import getpass
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from nimoteshot.pipeline import MODELS, STYLES, generate
from nimoteshot.providers import check_connection
from nimoteshot.server import serve
from nimoteshot.settings import config_path, describe, save


def main():
    parser = argparse.ArgumentParser(description="NimoteShot screenshot studio")
    sub = parser.add_subparsers(dest="command", required=True)
    web = sub.add_parser("web", help="Open the local web UI")
    web.add_argument("--port", type=int, default=8765,
                     help="Preferred port; restart a verified idle studio or select a free port if occupied")
    web.add_argument("--no-browser", action="store_true")
    doctor = sub.add_parser("doctor", help="Check the selected provider before uploading captures")
    doctor.add_argument("--provider", choices=[item["id"] for item in MODELS["providers"]], default=MODELS["default_provider"])
    doctor.add_argument("--model", default="")
    doctor.add_argument("--base-url", default="")
    configure = sub.add_parser("configure", help="Save a provider profile in your user config directory")
    configure.add_argument("--provider", choices=[item["id"] for item in MODELS["providers"]])
    configure.add_argument("--model", default="")
    configure.add_argument("--base-url", default="")
    configure.add_argument("--api-key", default="", help="Avoid shell history: prefer --prompt-api-key")
    configure.add_argument("--api-key-stdin", action="store_true", help="Read one API key line from standard input")
    configure.add_argument("--prompt-api-key", action="store_true", help="Prompt for an API key without echoing it")
    configure.add_argument("--clear-key", action="store_true")
    configure.add_argument("--verify", action="store_true", help="Verify the provider before saving this profile")
    configure.add_argument("--show", action="store_true", help="Show configured providers without secrets")
    run = sub.add_parser("generate", help="Generate all languages and sizes with AI")
    run.add_argument("--input", default="screens", help="Folder of original PNG captures")
    run.add_argument("--brand", required=True, help="App name shown on artwork")
    run.add_argument("--description", default="", help="What the app does and its main features")
    run.add_argument("--website", default="", help="Optional public HTTPS product website")
    run.add_argument("--style", choices=[item["id"] for item in STYLES["styles"]], default=STYLES["default"])
    run.add_argument("--provider", choices=[item["id"] for item in MODELS["providers"]], default=MODELS["default_provider"])
    run.add_argument("--model", default="", help="Optional model override")
    run.add_argument("--base-url", default="", help="Only needed for another compatible API")
    run.add_argument("--design-prompt", default="", help="Optional layout or art-direction guidance for the model")
    run.add_argument("--locales", default="zh-CN", help="Comma-separated output locales: zh-CN,ja-JP,ko-KR,es-ES")
    args = parser.parse_args()
    if args.command == "web":
        serve(port=args.port, open_browser=not args.no_browser)
    elif args.command == "configure":
        if args.show:
            print("Config:", config_path())
            for provider, item in describe().items():
                print(f"{provider}: model={item['model'] or '(default)'} key={'saved' if item['has_api_key'] else 'not saved'}")
            return
        if not args.provider:
            parser.error("configure requires --provider unless --show is used")
        if sum(bool(value) for value in (args.api_key, args.api_key_stdin, args.prompt_api_key)) > 1:
            parser.error("use only one API key input method")
        api_key = getpass.getpass("API key: ") if args.prompt_api_key else (sys.stdin.readline().rstrip("\r\n") if args.api_key_stdin else args.api_key)
        if args.verify:
            status = check_connection(args.provider, args.model, args.base_url, api_key)
            print(status["message"])
        path = save(args.provider, args.model, args.base_url, api_key, args.clear_key)
        print("Saved provider profile:", path)
    elif args.command == "doctor":
        print(check_connection(args.provider, args.model, args.base_url)["message"])
    else:
        result = generate(ROOT / args.input, args.brand, args.description, args.website,
                          args.style, args.provider, model=args.model, base_url=args.base_url,
                          progress=print, design_prompt=args.design_prompt,
                          locales=tuple(item.strip() for item in args.locales.split(",") if item.strip()))
        print("ZIP:", ROOT / result["archive"])


if __name__ == "__main__":
    try:
        main()
    except (ValueError, RuntimeError, FileExistsError) as error:
        print(f"NimoteShot: {error}", file=sys.stderr)
        raise SystemExit(2) from error
