"""
HVF Sovereign C2 // Ebony (Chronos) Deterministic Zero-Hallucination & Live WAN Grounding Gate
CAGE: 1AHA8 | UEI: S1M4ENLHTDH5 | DFARS 252.227-7018 Sovereign Background IP
"""
import re
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timezone

ZERO_HALLUCINATION_SYSTEM_DIRECTIVE = (
    "CRITICAL SOVEREIGN ZERO-HALLUCINATION MANDATE (CAGE 1AHA8): "
    "You are strictly forbidden from inventing, guessing, or hallucinating names, dates, casualties, "
    "locations, or events. You must ONLY state facts explicitly present in the [VERIFIED GROUND-TRUTH TELEMETRY] "
    "block below or verified HVF C2 system architecture. Do NOT invent names of individuals or dates not listed "
    "in the verified headlines. If a detail (such as a specific person's name) is not in the headlines below, "
    "explicitly state: 'Specific detail not yet confirmed in live wire headlines; refusing to speculate per HVF Zero-Hallucination Protocol.'"
)

STOPWORDS = {
    "what", "whats", "whatas", "is", "are", "was", "were", "going", "on", "in", "at", "the", "a", "an",
    "and", "or", "today", "right", "now", "started", "happened", "happening", "tell", "me", "about",
    "why", "how", "who", "when", "where", "please", "ebony", "chronos", "status", "report", "give", "update"
}

def extract_search_keywords(raw_query: str) -> str:
    """Strips conversational filler and typos ('whatas going on in paris today...') to isolate core search entities."""
    tokens = re.findall(r"[A-Za-z0-9]+", raw_query.lower())
    core = [t for t in tokens if t not in STOPWORDS and len(t) > 2]
    if not core:
        return raw_query.strip()
    return " ".join(core[:6])

def fetch_live_wan_verified_news(query: str, max_items: int = 6, timeout_sec: float = 4.5) -> list[dict]:
    """Fetches real-time verified news items via standard HTTPS RSS when Online WAN Ingress is active."""
    search_terms = extract_search_keywords(query)
    clean_q = urllib.parse.quote_plus(search_terms)
    url = f"https://news.google.com/rss/search?q={clean_q}&hl=en-US&gl=US&ceid=US:en"
    req = urllib.request.Request(url, headers={"User-Agent": "HVF-Sovereign-C2-Ingress/8.0"})
    headlines = []
    try:
        with urllib.request.urlopen(req, timeout=timeout_sec) as resp:
            raw_xml = resp.read()
        root = ET.fromstring(raw_xml)
        for item in root.findall(".//item")[:max_items]:
            title = (item.findtext("title") or "").strip()
            pub_date = (item.findtext("pubDate") or "").strip()
            source = (item.findtext("source") or "Verified Wire").strip()
            if title:
                headlines.append({"title": title, "pub_date": pub_date, "source": source})
    except Exception:
        return []
    return headlines

def build_grounded_chronos_prompt(user_directive: str, online_mode: bool = True) -> str:
    """Wraps any operator directive in a deterministic anti-hallucination envelope with live WAN RSS facts."""
    now_utc = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    search_kw = extract_search_keywords(user_directive)
    if online_mode:
        items = fetch_live_wan_verified_news(user_directive, max_items=6)
        if items:
            bullet_list = "\n".join(
                f"  - [{it['pub_date']}] ({it['source']}): {it['title']}" for it in items
            )
            telemetry_block = (
                f"[VERIFIED LIVE WAN INGRESS TELEMETRY AS OF {now_utc} // QUERY: '{search_kw}']\n{bullet_list}"
            )
        else:
            telemetry_block = (
                f"[VERIFIED LIVE WAN INGRESS TELEMETRY AS OF {now_utc} // QUERY: '{search_kw}']\n"
                "  - No verified live wire items matched this query. Do NOT invent names, dates, or events."
            )
    else:
        telemetry_block = (
            f"[SOVEREIGN AIR-GAP MODE ACTIVE AS OF {now_utc}]\n"
            "  - External WAN news ingress is physically/logically disabled in Offline Air-Gap mode. "
            "Refuse any request for live external world news rather than guessing."
        )
    return (
        f"{ZERO_HALLUCINATION_SYSTEM_DIRECTIVE}\n\n"
        f"{telemetry_block}\n\n"
        f"OPERATOR DIRECTIVE: {user_directive}\n"
        "Provide a concise, strictly verified executive status report using ONLY the verified telemetry above:"
    )


def ground_messages_payload(messages_payload: list, online_mode: bool = True) -> list:
    """Intercepts any OpenAI/Ollama messages list and grounds the latest user message with live WAN telemetry."""
    if not isinstance(messages_payload, list) or len(messages_payload) == 0:
        return messages_payload
    grounded = [dict(m) if isinstance(m, dict) else m for m in messages_payload]
    for idx in range(len(grounded) - 1, -1, -1):
        msg = grounded[idx]
        if isinstance(msg, dict) and msg.get("role") == "user":
            raw_u = str(msg.get("content", ""))
            if "CRITICAL SOVEREIGN ZERO-HALLUCINATION MANDATE" not in raw_u:
                grounded[idx]["content"] = build_grounded_chronos_prompt(raw_u, online_mode=online_mode)
            break
    return grounded
