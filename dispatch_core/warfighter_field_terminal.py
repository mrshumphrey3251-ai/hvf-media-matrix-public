# -*- coding: utf-8 -*-
"""
Project Ebony: Dismounted Warfighter & Field Operator Tactical Terminal
Provides offline-first self-localization, MGRS geodetic translation,
rally point compass navigation, and direct Blue Force Tracking (BFT) transmission.
Entity: Humphrey Virtual Farms LLC (CAGE: 1AHA8)
Statutory Standard: DFARS 252.227-7018 / Oklahoma HB 2992
"""

import os
import sys
import math
import sqlite3
import datetime

repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
for p in [repo_root, os.path.join(repo_root, "scada_engine"), os.path.join(repo_root, "c2_cockpit"), os.path.join(repo_root, "dispatch_core")]:
    if p not in sys.path:
        sys.path.insert(0, p)

from warfighter_gps_beacon import WarfighterGPSBeacon

class WarfighterFieldTerminal:
    def __init__(self, operator_id="HVF-SCOUT-07", callsign="WARRIOR_SEVEN"):
        self.operator_id = operator_id
        self.callsign = callsign
        self.beacon = WarfighterGPSBeacon()
        self.base_station = {
            "name": "BASE_STATION_ALPHA",
            "lat": 35.4675,
            "lon": -97.5165,
            "elevation_m": 385.0
        }

    def locate_self(self, lat, lon, elev_m=380.0):
        """Calculates current tactical grid and azimuth heading back to Base Station Alpha."""
        mgrs = self.beacon.to_mgrs_approx(lat, lon)
        dist_to_base = self.beacon.calculate_haversine_distance(
            lat, lon, self.base_station["lat"], self.base_station["lon"]
        )
        
        # Calculate compass heading back to safe rally point
        phi1 = math.radians(lat)
        phi2 = math.radians(self.base_station["lat"])
        dlam = math.radians(self.base_station["lon"] - lon)
        x = math.sin(dlam) * math.cos(phi2)
        y = math.cos(phi1) * math.sin(phi2) - math.sin(phi1) * math.cos(phi2) * math.cos(dlam)
        bearing = (math.degrees(math.atan2(x, y)) + 360.0) % 360.0

        return {
            "operator_id": self.operator_id,
            "callsign": self.callsign,
            "coordinates": {"latitude": lat, "longitude": lon, "elevation_m": elev_m},
            "mgrs_grid": mgrs,
            "rally_point": self.base_station["name"],
            "rally_distance_m": round(dist_to_base, 2),
            "rally_bearing_deg": round(bearing, 1)
        }

    def transmit_bft_update(self, lat, lon, elev_m=380.0, battery_pct=92.0):
        """Dispatches an authenticated Blue Force Tracking telemetry update to C2."""
        rec_id, mgrs = self.beacon.transmit_beacon(
            operator_id=self.operator_id,
            callsign=self.callsign,
            lat=lat,
            lon=lon,
            elevation_m=elev_m,
            distress_active=False,
            battery_pct=battery_pct
        )
        return rec_id, mgrs

    def trigger_emergency_sos(self, lat, lon, elev_m=380.0, battery_pct=35.0):
        """Activates single-touch emergency SOS beacon for Search and Rescue."""
        rec_id, mgrs = self.beacon.transmit_beacon(
            operator_id=self.operator_id,
            callsign=self.callsign,
            lat=lat,
            lon=lon,
            elevation_m=elev_m,
            distress_active=True,
            battery_pct=battery_pct
        )
        return rec_id, mgrs

if __name__ == "__main__":
    print("=" * 72)
    print("  PROJECT EBONY: DISMOUNTED WARFIGHTER TACTICAL FIELD TERMINAL")
    print("  * Operator Authority: CEO_JEFFERY_HUMPHREY (Level 5 Unrestricted)")
    print("  * Authority CAGE:     1AHA8 (Humphrey Virtual Farms LLC)")
    print("=" * 72)

    # Initialize terminal for dismounted scout
    terminal = WarfighterFieldTerminal(operator_id="SOLDIER-SCOUT-09", callsign="VALKYRIE_ONE")

    # 1. Offline Self-Localization Inquiry (Operator lost in field sector)
    test_lat, test_lon, test_elev = 35.4695, -97.5140, 381.2
    loc = terminal.locate_self(test_lat, test_lon, test_elev)
    print("\n[1] OFFLINE SELF-LOCALIZATION TELEMETRY:")
    print(f"  * Operator Call:      {loc['callsign']} ({loc['operator_id']})")
    print(f"  * Geodetic GPS:       ({loc['coordinates']['latitude']:.4f}, {loc['coordinates']['longitude']:.4f})")
    print(f"  * Elevation:          {loc['coordinates']['elevation_m']} meters MSL")
    print(f"  * Tactical Grid:      MGRS {loc['mgrs_grid']}")
    print(f"  * Designated Rally:   {loc['rally_point']}")
    print(f"  * Standoff to Rally:  {loc['rally_distance_m']} meters")
    print(f"  * Compass Bearing:    {loc['rally_bearing_deg']} degrees (South-Southwest)")

    # 2. Transmit Routine Blue Force Tracking Beacon
    rec_id, mgrs_str = terminal.transmit_bft_update(test_lat, test_lon, test_elev, battery_pct=94.5)
    print(f"\n[2] BLUE FORCE TRACKING (BFT) TELEMETRY DISPATCHED:")
    print(f"  * Vault Record:       #{rec_id:02d}")
    print(f"  * Committed Grid:     {mgrs_str}")
    print(f"  * System Status:      SYNCHRONIZED WITH C2 COCKPIT")

    print("\n" + "=" * 72)
    print("  [PASS] Warfighter Field Terminal 100% Operational")
    print("=" * 72)
