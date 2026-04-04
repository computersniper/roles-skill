#!/usr/bin/env python3
"""
Data analysis and statistical processing toolkit

Data analysis and statistical processing toolkit

Authentication: No authentication required
Base URL: local

Usage:
    python3 data_analyzer.py --setup  # Initialize working directory
    python3 data_analyzer.py <command> [options]
"""

from __future__ import annotations

import json
import sys
import time
import argparse
from pathlib import Path
from typing import Optional, Dict, Any, List, Union

try:
    import pandas as pd
    import numpy as np
    from scipy import stats
except ImportError:
    print("Error: Please install required packages first:", file=sys.stderr)
    print("   pip install pandas numpy scipy", file=sys.stderr)
    sys.exit(1)


# Configuration
CONFIG_PATH = Path.home() / ".data_scientist_tools" / "data_analyzer_config.json"
WORKSPACE_DEFAULT = Path.home() / "ds_workspace"

# Token cache (for expiration handling)
_token_cache: Dict[str, Any] = {}


# ─── Configuration Management ─────────────────────────────────────────────────


def load_config() -> Dict[str, Any]:
    """Load configuration from file."""
    if not CONFIG_PATH.exists():
        print(f"Configuration not found. Please run: python3 data_analyzer.py --setup", file=sys.stderr)
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
    print(f"=== Data analysis and statistical processing toolkit ===\n")
    workspace = input(f"Workspace directory [{WORKSPACE_DEFAULT}]: ").strip() or str(WORKSPACE_DEFAULT)
    config = {"workspace": workspace}

    save_config(config)
    Path(workspace).mkdir(parents=True, exist_ok=True)
    print(f"\n✅ Configuration saved to {CONFIG_PATH}")
    print(f"✅ Workspace directory created at {workspace}")


# ─── Authentication ────────────────────────────────────────────────────────────
def get_auth_headers(config: Dict[str, Any]) -> Dict[str, str]:
    """No authentication required."""
    return {}


# ─── Data Analysis Functions ───────────────────────────────────────────────────

def load_csv(file_path: str, **kwargs) -> pd.DataFrame:
    """Load CSV file into pandas DataFrame."""
    return pd.read_csv(file_path, **kwargs)


def descriptive_stats(df: pd.DataFrame) -> Dict[str, Any]:
    """Calculate descriptive statistics for DataFrame."""
    result = {
        "summary": df.describe().to_dict(),
        "missing_values": df.isnull().sum().to_dict(),
        "correlation": df.corr(numeric_only=True).to_dict() if len(df.select_dtypes(include=[np.number]).columns) > 0 else {}
    }
    return result


def hypothesis_test(
    df: pd.DataFrame,
    column: str,
    test_type: str = "ttest",
    compare_value: float = 0,
    group_col: Optional[str] = None
) -> Dict[str, Any]:
    """Perform common statistical hypothesis tests."""
    result = {"test_type": test_type, "column": column}

    if test_type == "ttest":
        if group_col and group_col in df.columns:
            groups = df[group_col].unique()
            if len(groups) == 2:
                group1 = df[df[group_col] == groups[0]][column].dropna()
                group2 = df[df[group_col] == groups[1]][column].dropna()
                stat, pval = stats.ttest_ind(group1, group2, equal_var=False)
                result = {
                    "test_type": "independent_ttest",
                    "statistic": float(stat),
                    "p_value": float(pval),
                    "groups": [str(groups[0]), str(groups[1])],
                    "significant": pval < 0.05
                }
        else:
            stat, pval = stats.ttest_1samp(df[column].dropna(), popmean=compare_value)
            result = {
                "test_type": "one_sample_ttest",
                "compare_value": compare_value,
                "statistic": float(stat),
                "p_value": float(pval),
                "significant": pval < 0.05
            }
    elif test_type == "chi_square":
        # Chi-square test for independence
        if group_col and group_col in df.columns:
            contingency = pd.crosstab(df[column], df[group_col])
            chi2, pval, dof, expected = stats.chi2_contingency(contingency)
            result = {
                "test_type": "chi_square",
                "chi2_statistic": float(chi2),
                "p_value": float(pval),
                "degrees_of_freedom": dof,
                "significant": pval < 0.05
            }

    return result


def linear_regression(
    df: pd.DataFrame,
    x_cols: List[str],
    y_col: str
) -> Dict[str, Any]:
    """Simple linear regression using numpy."""
    X = df[x_cols].values
    y = df[y_col].values

    # Add intercept
    X = np.hstack([np.ones((X.shape[0], 1)), X])

    # Normal equation: (X'X)^-1 X'y
    try:
        beta = np.linalg.inv(X.T @ X) @ X.T @ y
    except np.linalg.LinAlgError:
        return {"error": "Singular matrix, cannot compute regression"}

    y_pred = X @ beta
    residuals = y - y_pred
    mse = np.mean(residuals ** 2)
    r_squared = 1 - (np.sum(residuals ** 2) / np.sum((y - np.mean(y)) ** 2))

    result = {
        "intercept": float(beta[0]),
        "coefficients": {name: float(beta[i+1]) for i, name in enumerate(x_cols)},
        "r_squared": float(r_squared),
        "mse": float(mse),
        "n_samples": len(y)
    }

    return result


# ─── Main CLI ──────────────────────────────────────────────────────────────────


def main() -> None:
    parser = argparse.ArgumentParser(description="Data analysis and statistical processing toolkit")
    parser.add_argument("--setup", action="store_true", help="Initialize working directory configuration")
    parser.add_argument("--describe", help="Calculate descriptive statistics for CSV file")
    parser.add_argument("--ttest", help="Perform t-test on column")
    parser.add_argument("--group", help="Group column for two-sample test")
    parser.add_argument("--compare", type=float, default=0, help="Comparison value for one-sample t-test")
    parser.add_argument("--regress", help="Linear regression, target Y column")
    parser.add_argument("--x-vars", help="Comma-separated list of X variables")
    parser.add_argument("--output", help="Output JSON results to file")

    args = parser.parse_args()

    if args.setup:
        setup_config()
        return

    config = load_config()

    if args.describe:
        df = load_csv(args.describe)
        result = descriptive_stats(df)
        print(json.dumps(result, indent=2, ensure_ascii=False))

    elif args.ttest:
        if not args.group:
            print("Error: --group is required for two-sample t-test", file=sys.stderr)
            sys.exit(1)
        df = load_csv(args.ttest.split(':')[0])
        column = args.ttest.split(':')[1] if ':' in args.ttest else args.ttest
        result = hypothesis_test(df, column, test_type="ttest", group_col=args.group)
        print(json.dumps(result, indent=2, ensure_ascii=False))

    elif args.regress:
        if not args.x_vars:
            print("Error: --x-vars is required for regression", file=sys.stderr)
            sys.exit(1)
        df = load_csv(args.regress.split(':')[0])
        y_col = args.regress.split(':')[1] if ':' in args.regress else args.regress
        x_cols = args.x_vars.split(',')
        result = linear_regression(df, x_cols, y_col)
        print(json.dumps(result, indent=2, ensure_ascii=False))

    else:
        print("No command executed. Use --help for usage.")


if __name__ == "__main__":
    main()
