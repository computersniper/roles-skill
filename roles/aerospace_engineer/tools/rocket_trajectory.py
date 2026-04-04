#!/usr/bin/env python3
"""
Rocket trajectory simulation and orbital mechanics calculator

Rocket trajectory simulation and orbital mechanics calculator

Authentication: No authentication required
Base URL: local

Usage:
    python3 rocket_trajectory.py --setup  # Initialize workspace
    python3 rocket_trajectory.py <command> [options]
"""

from __future__ import annotations

import json
import math
import sys
import argparse
from pathlib import Path
from typing import Optional, Dict, Any, List, Tuple

try:
    import numpy as np
except ImportError:
    print("Error: Please install numpy first: pip install numpy", file=sys.stderr)
    sys.exit(1)


# Configuration
CONFIG_PATH = Path.home() / ".aerospace_engineer_tools" / "rocket_trajectory_config.json"
GRAVITATIONAL_CONSTANT = 6.67430e-11  # m^3 kg^-1 s^-2
EARTH_MASS = 5.972e24  # kg
EARTH_RADIUS = 6371000  # meters

# Constants
MU = GRAVITATIONAL_CONSTANT * EARTH_MASS  # Standard gravitational parameter for Earth


# ─── Configuration Management ─────────────────────────────────────────────────


def load_config() -> Dict[str, Any]:
    """Load configuration from file."""
    if not CONFIG_PATH.exists():
        print(f"Configuration not found. Please run: python3 rocket_trajectory.py --setup", file=sys.stderr)
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
    print(f"=== Rocket trajectory simulation and orbital mechanics calculator ===\n")
    print("No additional configuration required.")
    config = {}

    save_config(config)
    print(f"\n✅ Configuration saved to {CONFIG_PATH}")


# ─── Authentication ────────────────────────────────────────────────────────────
def get_auth_headers(config: Dict[str, Any]) -> Dict[str, str]:
    """No authentication required."""
    return {}


# ─── Orbital Mechanics Calculations ─────────────────────────────────────────────

def circular_orbit_velocity(altitude: float) -> float:
    """Calculate required circular orbit velocity at given altitude.

    Args:
        altitude: Altitude above Earth surface in kilometers

    Returns:
        Velocity in m/s
    """
    radius = (altitude * 1000) + EARTH_RADIUS
    velocity = math.sqrt(MU / radius)
    return velocity


def orbital_period(altitude: float) -> float:
    """Calculate orbital period for circular orbit at given altitude.

    Args:
        altitude: Altitude above Earth surface in kilometers

    Returns:
        Period in minutes
    """
    radius = (altitude * 1000) + EARTH_RADIUS
    period = 2 * math.pi * math.sqrt(radius**3 / MU)
    return period / 60.0


def delta_v_hohmann(altitude1: float, altitude2: float) -> float:
    """Calculate total delta-V required for Hohmann transfer between two circular orbits.

    Args:
        altitude1: Initial orbit altitude in km
        altitude2: Final orbit altitude in km

    Returns:
        Total delta-V required in m/s
    """
    r1 = (altitude1 * 1000) + EARTH_RADIUS
    r2 = (altitude2 * 1000) + EARTH_RADIUS

    v1 = math.sqrt(MU / r1)
    v2 = math.sqrt(MU / r2)

    # Semi-major axis of transfer ellipse
    a_transfer = (r1 + r2) / 2

    # Velocity at departure
    v_departure = math.sqrt(MU * (2 / r1 - 1 / a_transfer))
    delta_v1 = v_departure - v1

    # Velocity at arrival
    v_arrival = math.sqrt(MU * (2 / r2 - 1 / a_transfer))
    delta_v2 = v2 - v_arrival

    return delta_v1 + delta_v2


def escape_velocity(altitude: float) -> float:
    """Calculate escape velocity from Earth at given altitude.

    Args:
        altitude: Altitude above Earth surface in kilometers

    Returns:
        Escape velocity in m/s
    """
    radius = (altitude * 1000) + EARTH_RADIUS
    return math.sqrt(2 * MU / radius)


def thrust_to_weight(thrust: float, mass: float) -> float:
    """Calculate thrust-to-weight ratio.

    Args:
        thrust: Engine thrust in Newtons
        mass: Vehicle mass in kg

    Returns:
        Thrust-to-weight ratio (>1 means can lift off)
    """
    weight = mass * 9.81  # m/s^2 at sea level
    return thrust / weight


def apogee_perigee_from_altitudes(perigee_alt: float, apogee_alt: float) -> Tuple[float, float]:
    """Convert altitudes to radii and calculate semi-major axis and eccentricity.

    Returns:
        (semi_major_axis, eccentricity)
    """
    rp = (perigee_alt * 1000) + EARTH_RADIUS
    ra = (apogee_alt * 1000) + EARTH_RADIUS
    a = (rp + ra) / 2
    e = (ra - rp) / (ra + rp)
    return a, e


def delta_v_to_leo(lift_off_mass: float, dry_mass: float, isp: float) -> float:
    """Calculate total delta-V available using Tsiolkovsky rocket equation.

    Args:
        lift_off_mass: Initial mass at lift-off in kg
        dry_mass: Dry mass after fuel burn in kg
        isp: Specific impulse in seconds

    Returns:
        Total delta-V in m/s
    """
    ve = isp * 9.81
    mass_ratio = lift_off_mass / dry_mass
    return ve * math.log(mass_ratio)


# ─── Main CLI ──────────────────────────────────────────────────────────────────


def main() -> None:
    parser = argparse.ArgumentParser(description="Rocket trajectory simulation and orbital mechanics calculator")
    parser.add_argument("--setup", action="store_true", help="Initialize configuration")
    parser.add_argument("--velocity", type=float, help="Calculate circular orbit velocity at altitude (km)")
    parser.add_argument("--period", type=float, help="Calculate orbital period at altitude (km)")
    parser.add_argument("--hohmann", nargs=2, type=float, metavar=("ALT1", "ALT2"), help="Hohmann transfer between two altitudes (km)")
    parser.add_argument("--escape", type=float, help="Calculate escape velocity at altitude (km)")
    parser.add_argument("--tsiolkovsky", nargs=3, type=float, metavar=("MASS_INIT", "MASS_FINAL", "ISP"), help="Delta-V from rocket equation")

    args = parser.parse_args()

    if args.setup:
        setup_config()
        return

    result: Dict[str, Any] = {}

    if args.velocity is not None:
        vel = circular_orbit_velocity(args.velocity)
        result = {
            "altitude_km": args.velocity,
            "circular_orbit_velocity_mps": vel,
            "circular_orbit_velocity_kmh": vel * 3.6
        }

    elif args.period is not None:
        period_min = orbital_period(args.period)
        result = {
            "altitude_km": args.period,
            "orbital_period_minutes": period_min,
            "orbital_period_hours": period_min / 60
        }

    elif args.hohmann:
        alt1, alt2 = args.hohmann
        total_dv = delta_v_hohmann(alt1, alt2)
        result = {
            "initial_altitude_km": alt1,
            "final_altitude_km": alt2,
            "total_deltav_mps": total_dv
        }

    elif args.escape is not None:
        v_esc = escape_velocity(args.escape)
        result = {
            "altitude_km": args.escape,
            "escape_velocity_mps": v_esc,
            "escape_velocity_kmh": v_esc * 3.6
        }

    elif args.tsiolkovsky:
        m_init, m_final, isp = args.tsiolkovsky
        dv = delta_v_to_leo(m_init, m_final, isp)
        result = {
            "initial_mass_kg": m_init,
            "final_mass_kg": m_final,
            "isp_seconds": isp,
            "mass_ratio": m_init / m_final,
            "total_deltav_mps": dv
        }

    else:
        print("No command executed. Use --help for usage.")
        sys.exit(1)

    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
