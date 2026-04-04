#!/usr/bin/env python3
"""
Tool Code Generator - Generate Python tool scaffolding for role tools.

根据角色描述和 API 信息自动生成 Python 工具代码脚手架：
  - API 调用封装
  - 错误处理
  - 认证处理（API Key、Bearer Token、OAuth 等）
  - 输出到 roles/{slug}/tools/ 目录

Usage:
    python3 tool_generator.py --slug <role_slug> --name <tool_name> \
        --api-base <base_url> --description "<tool_description>" \
        --auth-type <api_key|bearer|oauth|none> [--base-dir <path>]

Example:
    python3 tool_generator.py --slug weather_bot --name weather_api \
        --api-base "https://api.openweathermap.org/data/2.5" \
        --description "Get weather information from OpenWeatherMap API" \
        --auth-type api_key --base-dir ./roles
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Optional, Dict, Any


# Code template for generated tool
TOOL_TEMPLATE = '''#!/usr/bin/env python3
"""
{tool_description}

{description}

Authentication: {auth_description}
Base URL: {api_base}

Usage:
    python3 {tool_name}.py --setup  # Configure authentication (one-time)
    python3 {tool_name}.py <command> [options]
"""

from __future__ import annotations

import json
import sys
import time
import argparse
from pathlib import Path
from typing import Optional, Dict, Any

try:
    import requests
except ImportError:
    print("Error: Please install requests first: pip install requests", file=sys.stderr)
    sys.exit(1)


# Configuration
CONFIG_PATH = Path.home() / ".{project_slug}" / "{tool_name}_config.json"
BASE_URL = "{api_base}"

# Token cache (for expiration handling)
_token_cache: Dict[str, Any] = {{}}


# ─── Configuration Management ─────────────────────────────────────────────────


def load_config() -> Dict[str, Any]:
    """Load configuration from file."""
    if not CONFIG_PATH.exists():
        print(f"Configuration not found. Please run: python3 {tool_name}.py --setup", file=sys.stderr)
        sys.exit(1)
    return json.loads(CONFIG_PATH.read_text(encoding="utf-8"))


def save_config(config: Dict[str, Any]) -> None:
    """Save configuration to file."""
    CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
    CONFIG_PATH.write_text(
        json.dumps(config, indent=2, ensure_ascii=False),
        encoding="utf-8"
    )


def setup_config() -> None:
    """Interactive configuration setup."""
    print(f"=== {tool_description} Configuration ===\\n")
{setup_prompts}

    save_config(config)
    print(f"\\n✅ Configuration saved to {CONFIG_PATH}")


# ─── Authentication ────────────────────────────────────────────────────────────
{auth_code}


# ─── API Helpers ───────────────────────────────────────────────────────────────


def api_get(
    path: str,
    params: Optional[Dict[str, Any]] = None,
    config: Optional[Dict[str, Any]] = None,
    timeout: int = 15
) -> Dict[str, Any]:
    """Make a GET request to the API."""
    if config is None:
        config = load_config()

    url = f"{BASE_URL}{path}"
    headers = get_auth_headers(config)

    try:
        resp = requests.get(
            url,
            params=params,
            headers=headers,
            timeout=timeout
        )
        resp.raise_for_status()
        return resp.json()
    except requests.exceptions.RequestException as e:
        print(f"API GET error on {path}: {e}", file=sys.stderr)
        if hasattr(e, "response") and e.response is not None:
            print(f"Response: {e.response.text[:500]}", file=sys.stderr)
        return {{}}


def api_post(
    path: str,
    body: Optional[Dict[str, Any]] = None,
    config: Optional[Dict[str, Any]] = None,
    timeout: int = 15
) -> Dict[str, Any]:
    """Make a POST request to the API."""
    if config is None:
        config = load_config()

    url = f"{BASE_URL}{path}"
    headers = get_auth_headers(config)

    try:
        resp = requests.post(
            url,
            json=body or {},
            headers=headers,
            timeout=timeout
        )
        resp.raise_for_status()
        return resp.json()
    except requests.exceptions.RequestException as e:
        print(f"API POST error on {path}: {e}", file=sys.stderr)
        if hasattr(e, "response") and e.response is not None:
            print(f"Response: {e.response.text[:500]}", file=sys.stderr)
        return {{}}


# ─── Tool-specific Functions ───────────────────────────────────────────────────
{example_functions}


# ─── Main CLI ──────────────────────────────────────────────────────────────────


def main() -> None:
    parser = argparse.ArgumentParser(description="{tool_description}")
    parser.add_argument("--setup", action="store_true", help="Initialize authentication configuration")
{cli_arguments}

    args = parser.parse_args()

    if args.setup:
        setup_config()
        return
{main_body}

    print("No command executed. Use --help for usage.")


if __name__ == "__main__":
    main()
'''


def get_auth_template(auth_type: str) -> dict:
    """Get authentication code template based on type."""
    templates = {
        "api_key": {
            "auth_description": "API Key (passed as query parameter or header)",
            "setup_prompts": '''    api_key = input("API Key: ").strip()
    config = {"api_key": api_key}
''',
            "auth_code": '''def get_auth_headers(config: Dict[str, Any]) -> Dict[str, str]:
    """Get authentication headers for API requests."""
    # For API Key in header:
    return {"Authorization": f"Bearer {config['api_key']}"}
    # For API Key as query param: add it to the request params instead
''',
            "cli_extra": ""
        },
        "bearer": {
            "auth_description": "Bearer Token",
            "setup_prompts": '''    token = input("Bearer Token: ").strip()
    config = {"access_token": token, "expires_at": ""}
''',
            "auth_code": '''def get_auth_headers(config: Dict[str, Any]) -> Dict[str, str]:
    """Get authentication headers for API requests."""
    return {"Authorization": f"Bearer {config['access_token']}"}
''',
            "cli_extra": ""
        },
        "oauth2": {
            "auth_description": "OAuth 2.0 Client Credentials flow",
            "setup_prompts": '''    client_id = input("Client ID: ").strip()
    client_secret = input("Client Secret: ").strip()
    token_url = input("Token URL: ").strip() or "{api_base}/token"
    config = {{
        "client_id": client_id,
        "client_secret": client_secret,
        "token_url": token_url,
        "access_token": "",
        "expires_at": 0
    }}
''',
            "auth_code": '''def get_valid_token(config: Dict[str, Any]) -> str:
    """Get a valid access token, refreshing if expired."""
    now = time.time()
    if config.get("access_token") and config.get("expires_at", 0) > now + 60:
        return config["access_token"]

    # Need to refresh
    print("Refreshing OAuth access token...", file=sys.stderr)
    data = {{
        "grant_type": "client_credentials",
        "client_id": config["client_id"],
        "client_secret": config["client_secret"],
    }}

    try:
        resp = requests.post(config["token_url"], data=data, timeout=10)
        resp.raise_for_status()
        token_data = resp.json()
        config["access_token"] = token_data["access_token"]
        expires_in = token_data.get("expires_in", 3600)
        config["expires_at"] = int(now + expires_in)
        save_config(config)
        return config["access_token"]
    except Exception as e:
        print(f"Failed to refresh OAuth token: {e}", file=sys.stderr)
        sys.exit(1)


def get_auth_headers(config: Dict[str, Any]) -> Dict[str, str]:
    """Get authentication headers with a valid token."""
    token = get_valid_token(config)
    return {"Authorization": f"Bearer {token}"}
''',
            "cli_extra": ""
        },
        "basic": {
            "auth_description": "Basic Authentication (username/password)",
            "setup_prompts": '''    username = input("Username: ").strip()
    password = input("Password: ").strip()
    config = {"username": username, "password": password}
''',
            "auth_code": '''import base64

def get_auth_headers(config: Dict[str, Any]) -> Dict[str, str]:
    """Get Basic Authentication headers."""
    credentials = f"{config['username']}:{config['password']}"
    encoded = base64.b64encode(credentials.encode()).decode()
    return {"Authorization": f"Basic {encoded}"}
''',
            "cli_extra": ""
        },
        "none": {
            "auth_description": "No authentication required",
            "setup_prompts": '''    config = {}
    print("This API does not require authentication.")
''',
            "auth_code": '''def get_auth_headers(config: Dict[str, Any]) -> Dict[str, str]:
    """No authentication required."""
    return {}
''',
            "cli_extra": ""
        }
    }
    # Default to api_key if not found
    return templates.get(auth_type, templates["api_key"])


def generate_example_functions(tool_name: str, description: str) -> str:
    """Generate example function stubs based on common API patterns."""
    return f'''# Example functions - replace these with your actual API endpoints

def get_resource(resource_id: str, config: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Get a specific resource by ID."""
    return api_get(f"/resources/{{resource_id}}", config=config)


def list_resources(limit: int = 20, offset: int = 0, config: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """List resources with pagination."""
    params = {{"limit": limit, "offset": offset}}
    return api_get("/resources", params=params, config=config)


def create_resource(data: Dict[str, Any], config: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Create a new resource."""
    return api_post("/resources", body=data, config=config)
'''


def generate_cli_arguments(auth_type: str) -> str:
    """Generate CLI argument definitions."""
    base = '''\
    parser.add_argument("--resource-id", help="Get resource by ID")
    parser.add_argument("--list", action="store_true", help="List resources")
    parser.add_argument("--limit", type=int, default=20, help="Number of items to list")
'''
    return base


def generate_main_body(tool_name: str) -> str:
    """Generate main CLI body."""
    return '''
    config = load_config()

    if args.resource_id:
        result = get_resource(args.resource_id, config)
        if result:
            print(json.dumps(result, indent=2, ensure_ascii=False))
        else:
            sys.exit(1)
    elif args.list:
        result = list_resources(limit=args.limit, config=config)
        if result:
            print(json.dumps(result, indent=2, ensure_ascii=False))
        else:
            sys.exit(1)
'''


def generate_tool_code(
    tool_name: str,
    tool_description: str,
    api_base: str,
    auth_type: str,
    project_slug: str,
) -> str:
    """Generate the complete tool code."""
    auth_tpl = get_auth_template(auth_type)

    # Fill in the template
    code = TOOL_TEMPLATE.format(
        tool_name=tool_name,
        tool_description=tool_description,
        description=tool_description,
        api_base=api_base,
        project_slug=project_slug,
        auth_description=auth_tpl["auth_description"],
        setup_prompts=auth_tpl["setup_prompts"],
        auth_code=auth_tpl["auth_code"],
        example_functions=generate_example_functions(tool_name, tool_description),
        cli_arguments=generate_cli_arguments(auth_type),
        main_body=generate_main_body(tool_name),
    )
    return code


def generate_tool(
    base_dir: Path,
    role_slug: str,
    tool_name: str,
    tool_description: str,
    api_base: str,
    auth_type: str,
) -> Path:
    """Generate a tool file and return the path."""
    # Ensure output directory exists
    output_dir = base_dir / role_slug / "tools"
    output_dir.mkdir(parents=True, exist_ok=True)

    # Generate the code
    code = generate_tool_code(
        tool_name=tool_name,
        tool_description=tool_description,
        api_base=api_base,
        auth_type=auth_type,
        project_slug=f"{role_slug}_tools",
    )

    # Write to file
    output_path = output_dir / f"{tool_name}.py"
    output_path.write_text(code, encoding="utf-8")

    # Make executable
    output_path.chmod(0o755)

    return output_path


def generate_tools_from_spec(
    base_dir: Path,
    role_slug: str,
    tools_spec: list[dict],
) -> list[Path]:
    """Generate multiple tools from a specification list."""
    generated = []
    for spec in tools_spec:
        path = generate_tool(
            base_dir=base_dir,
            role_slug=role_slug,
            tool_name=spec.get("name", "api_client"),
            tool_description=spec.get("description", "API client"),
            api_base=spec.get("api_base", "https://api.example.com"),
            auth_type=spec.get("auth_type", "api_key"),
        )
        generated.append(path)
    return generated


def main():
    parser = argparse.ArgumentParser(description="Generate Python tool scaffolding")
    parser.add_argument("--slug", required=True, help="Role slug (directory name)")
    parser.add_argument("--name", required=True, help="Tool name (filename without .py)")
    parser.add_argument("--description", default="", help="Tool description")
    parser.add_argument("--api-base", required=True, help="API base URL")
    parser.add_argument("--auth-type", default="api_key",
                        choices=["api_key", "bearer", "oauth2", "basic", "none"],
                        help="Authentication type")
    parser.add_argument("--spec", help="JSON spec file with multiple tools")
    parser.add_argument("--base-dir", default="./roles",
                        help="Base directory for roles (default: ./roles)")

    args = parser.parse_args()
    base_dir = Path(args.base_dir).expanduser()

    if args.spec:
        # Generate multiple tools from spec
        spec = json.loads(Path(args.spec).read_text(encoding="utf-8"))
        generated = generate_tools_from_spec(
            base_dir=base_dir,
            role_slug=args.slug,
            tools_spec=spec if isinstance(spec, list) else spec.get("tools", []),
        )
        print(f"✅ Generated {len(generated)} tools:")
        for path in generated:
            print(f"   {path}")
    else:
        # Generate single tool
        output_path = generate_tool(
            base_dir=base_dir,
            role_slug=args.slug,
            tool_name=args.name,
            tool_description=args.description,
            api_base=args.api_base,
            auth_type=args.auth_type,
        )
        print(f"✅ Generated tool: {output_path}")


if __name__ == "__main__":
    main()
