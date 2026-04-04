#!/usr/bin/env python3
"""
Get climate change data and projections from open climate APIs

Get climate change data and projections from open climate APIs

Authentication: No authentication required
Base URL: https://api.climatedata.org

Usage:
    python3 climate_data_api.py --setup  # Configure authentication (one-time)
    python3 climate_data_api.py <command> [options]
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
CONFIG_PATH = Path.home() / ".climate_scientist_tools" / "climate_data_api_config.json"
BASE_URL = "https://api.climatedata.org"

# Token cache (for expiration handling)
_token_cache: Dict[str, Any] = {}


# ─── Configuration Management ─────────────────────────────────────────────────


def load_config() -> Dict[str, Any]:
    """Load configuration from file."""
    if not CONFIG_PATH.exists():
        print(f"Configuration not found. Please run: python3 climate_data_api.py --setup", file=sys.stderr)
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
    print(f"=== Get climate change data and projections from open climate APIs ===\n")
    config = {}
    print("This API does not require authentication.")

    save_config(config)
    print(f"\n✅ Configuration saved to {CONFIG_PATH}")


# ─── Authentication ────────────────────────────────────────────────────────────
def get_auth_headers(config: Dict[str, Any]) -> Dict[str, str]:
    """No authentication required."""
    return {}


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
        return {}


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
        return {}


# ─── Tool-specific Functions ───────────────────────────────────────────────────
# Example functions - replace these with your actual API endpoints

def get_global_temp(config: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Get global temperature anomaly data."""
    return api_get("/temperature/anomaly", config=config)


def get_co2_concentration(limit: int = 100, config: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Get recent CO2 concentration data."""
    params = {"limit": limit}
    return api_get("/co2/concentration", params=params, config=config)


def get_sea_level_rise(start_year: int, end_year: int, config: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Get sea level rise data for a time range."""
    params = {"start_year": start_year, "end_year": end_year}
    return api_get("/sea-level/rise", params=params, config=config)


def project_future_temperature(scenario: str = "ssp585", config: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Project future temperature under different emission scenarios."""
    return api_get(f"/projections/temperature/{scenario}", config=config)


# ─── Main CLI ──────────────────────────────────────────────────────────────────


def main() -> None:
    parser = argparse.ArgumentParser(description="Get climate change data and projections from open climate APIs")
    parser.add_argument("--setup", action="store_true", help="Initialize authentication configuration")
    parser.add_argument("--global-temp", action="store_true", help="Get global temperature anomaly data")
    parser.add_argument("--co2", action="store_true", help="Get CO2 concentration data")
    parser.add_argument("--limit", type=int, default=100, help="Number of data points to return")
    parser.add_argument("--sea-level", action="store_true", help="Get sea level rise data")
    parser.add_argument("--start-year", type=int, default=1900, help="Start year for sea level data")
    parser.add_argument("--end-year", type=int, default=2024, help="End year for sea level data")
    parser.add_argument("--project", help="Project future temperature scenario (ssp126, ssp245, ssp585)")

    args = parser.parse_args()

    if args.setup:
        setup_config()
        return

    config = load_config()

    if args.global_temp:
        result = get_global_temp(config)
        if result:
            print(json.dumps(result, indent=2, ensure_ascii=False))
        else:
            sys.exit(1)
    elif args.co2:
        result = get_co2_concentration(limit=args.limit, config=config)
        if result:
            print(json.dumps(result, indent=2, ensure_ascii=False))
        else:
            sys.exit(1)
    elif args.sea_level:
        result = get_sea_level_rise(args.start_year, args.end_year, config)
        if result:
            print(json.dumps(result, indent=2, ensure_ascii=False))
        else:
            sys.exit(1)
    elif args.project:
        result = project_future_temperature(scenario=args.project, config=config)
        if result:
            print(json.dumps(result, indent=2, ensure_ascii=False))
        else:
            sys.exit(1)

    print("No command executed. Use --help for usage.")


if __name__ == "__main__":
    main()
