"""
E.B.O.N.Y. State Contractor Registry Management & Extension Engine
Entity: Humphrey Virtual Farms LLC | CAGE: 1AHA8 | UEI: S1M4ENLHTDH5
Statutory Authority: Oklahoma Title 61 & Title 74
"""
import json
from datetime import datetime, timezone
from pathlib import Path

REGISTRY_FILE = Path(r"C:\hvf_c2\hvf-media-matrix-private\c2_cockpit\state_contractor_registry.json")

def load_contractor_registry() -> dict:
    if not REGISTRY_FILE.exists():
        return {}
    return json.loads(REGISTRY_FILE.read_text(encoding="utf-8"))

def save_contractor_registry(data: dict) -> bool:
    try:
        data["last_updated_utc"] = datetime.now(timezone.utc).isoformat()
        REGISTRY_FILE.write_text(json.dumps(data, indent=2), encoding="utf-8")
        return True
    except Exception as e:
        print(f"[!] Registry write error: {e}")
        return False

def add_unspsc_code(code: str, title: str, division: str, target_capability: str) -> bool:
    """Safely appends a new commodity code without modifying or rewriting existing architecture."""
    data = load_contractor_registry()
    if not data:
        return False
        
    codes = data.get("unspsc_commodity_codes", [])
    # Check duplicate
    for c in codes:
        if c.get("code") == code:
            print(f"[*] UNSPSC Code {code} already registered.")
            return True
            
    codes.append({
        "code": code,
        "title": title,
        "division": division,
        "target_capability": target_capability,
        "status": "ACTIVE_REGISTERED"
    })
    data["unspsc_commodity_codes"] = codes
    return save_contractor_registry(data)

def search_codes(query: str) -> list:
    """Searches across all UNSPSC and NAICS codes for matching capabilities."""
    data = load_contractor_registry()
    q = query.lower()
    matches = []
    for c in data.get("unspsc_commodity_codes", []):
        if q in c.get("code", "") or q in c.get("title", "").lower() or q in c.get("target_capability", "").lower():
            matches.append(("UNSPSC", c.get("code"), c.get("title")))
    for n in data.get("naics_crosswalk_codes", []):
        if q in n.get("code", "") or q in n.get("title", "").lower():
            matches.append(("NAICS", n.get("code"), n.get("title")))
    return matches

if __name__ == "__main__":
    reg = load_contractor_registry()
    print("=" * 86)
    print("     E.B.O.N.Y. STATE CONTRACTOR REGISTRY VERIFICATION AUDIT     ")
    print(f"     ENTITY: {reg['corporate_identity']['legal_entity_name']} | CAGE: {reg['corporate_identity']['cage_code']}")
    print("=" * 86)
    print(f"[+] Total Active UNSPSC Codes: {len(reg.get('unspsc_commodity_codes', []))}")
    for item in reg.get("unspsc_commodity_codes", []):
        print(f"  • {item['code']} | {item['title'][:45]:<45} | {item['division']}")
    print(f"\n[+] Total NAICS Industry Crosswalk Codes: {len(reg.get('naics_crosswalk_codes', []))}")
    for item in reg.get("naics_crosswalk_codes", []):
        print(f"  • {item['code']} | {item['title']}")
    
    # Test safe extensibility append
    test_append = add_unspsc_code(
        code="99999999",
        title="Test Dynamic Extension Capability",
        division="OMES Title 61 Test",
        target_capability="Dynamic addition verification without codebase rewrite"
    )
    assert test_append == True, "Failed dynamic code append test!"
    
    # Clean up test entry
    data = load_contractor_registry()
    data["unspsc_commodity_codes"] = [c for c in data["unspsc_commodity_codes"] if c.get("code") != "99999999"]
    save_contractor_registry(data)
    print("\n[SUCCESS] Extensible architecture verified: New codes dynamically supported with zero syntax breakage.")
    print("=" * 86)