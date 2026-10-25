"""
HVF Sovereign C2 // Ebony (Chronos) Universal Zero-Hallucination & Live WAN Grounding Interceptor
CAGE: 1AHA8 | UEI: S1M4ENLHTDH5 | DFARS 252.227-7018 Sovereign Background IP
Intercepts httpx (OpenAI v1 client), requests, and urllib calls to Port 11434 with 0 byte changes to c2_cockpit.
"""
import json
import re
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timezone

_ORIG_URLOPEN = urllib.request.urlopen

ZERO_HALLUCINATION_SYSTEM_DIRECTIVE = (
    "CRITICAL SOVEREIGN ZERO-HALLUCINATION MANDATE (CAGE 1AHA8): "
    "You are strictly forbidden from inventing, guessing, or hallucinating names, dates, casualties, "
    "locations, or events. You must ONLY state facts explicitly present in the [VERIFIED LIVE WAN INGRESS TELEMETRY] "
    "block below. Summarize the exact headlines provided below clearly and concisely. Do NOT give generic boilerplate "
    "and do NOT invent any names or dates not explicitly written in the headlines below."
)

STOPWORDS = {
    "what", "whats", "whatas", "is", "are", "was", "were", "going", "on", "in", "at", "the", "a", "an",
    "and", "or", "today", "right", "now", "started", "happened", "happening", "tell", "me", "about",
    "why", "how", "who", "when", "where", "please", "ebony", "chronos", "status", "report", "give", "update"
}

def extract_search_keywords(raw_query: str) -> str:
    """Strips conversational filler ('what is happening in the mid term elections') to isolate core search entities."""
    tokens = re.findall(r"[A-Za-z0-9]+", raw_query.lower())
    core = [t for t in tokens if t not in STOPWORDS and len(t) > 2]
    if not core:
        return raw_query.strip()
    return " ".join(core[:6])

def fetch_live_wan_verified_news(query: str, max_items: int = 6, timeout_sec: float = 4.5) -> list[dict]:
    """Fetches real-time verified news items via standard HTTPS RSS using the unhooked _ORIG_URLOPEN."""
    search_terms = extract_search_keywords(query)
    clean_q = urllib.parse.quote_plus(search_terms)
    url = f"https://news.google.com/rss/search?q={clean_q}&hl=en-US&gl=US&ceid=US:en"
    req = urllib.request.Request(url, headers={"User-Agent": "HVF-Sovereign-C2-Ingress/8.0"})
    headlines = []
    try:
        with _ORIG_URLOPEN(req, timeout=timeout_sec) as resp:
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
        "Summarize the exact verified live wire headlines above and their strategic impact for HVF:"
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

def _transform_11434_json_dict(jpayload: dict) -> dict:
    """Transforms any JSON dict destined for Port 11434 (/v1/chat/completions or /api/chat or /api/generate)."""
    jpayload = dict(jpayload)
    if "messages" in jpayload and isinstance(jpayload["messages"], list):
        jpayload["messages"] = ground_messages_payload(jpayload["messages"], online_mode=True)
    elif "prompt" in jpayload and isinstance(jpayload["prompt"], str):
        if "CRITICAL SOVEREIGN ZERO-HALLUCINATION MANDATE" not in jpayload["prompt"]:
            jpayload["prompt"] = build_grounded_chronos_prompt(jpayload["prompt"], online_mode=True)
    if "temperature" in jpayload:
        jpayload["temperature"] = 0.0
    if "options" in jpayload or "model" in jpayload:
        opts = dict(jpayload.get("options") or {})
        opts["temperature"] = 0.0
        jpayload["options"] = opts
    return jpayload

_INTERCEPTOR_INSTALLED = False

def install_transparent_c2_interceptor() -> bool:
    """Hooks requests, httpx (used by OpenAI client on Line 169), and urllib for all Port 11434 calls."""
    global _INTERCEPTOR_INSTALLED
    if _INTERCEPTOR_INSTALLED:
        return True

    # 1. Hook requests.Session.request
    try:
        import requests
        _orig_req = requests.Session.request

        def _grounded_requests_send(self, method, url, *args, **kwargs):
            try:
                if "11434" in str(url) and str(method).upper() == "POST":
                    if "json" in kwargs and isinstance(kwargs["json"], dict):
                        kwargs["json"] = _transform_11434_json_dict(kwargs["json"])
                    elif "data" in kwargs and isinstance(kwargs["data"], (str, bytes)):
                        raw_d = kwargs["data"].decode("utf-8") if isinstance(kwargs["data"], bytes) else kwargs["data"]
                        jdoc = json.loads(raw_d)
                        if isinstance(jdoc, dict):
                            kwargs["data"] = json.dumps(_transform_11434_json_dict(jdoc)).encode("utf-8")
            except Exception:
                pass
            return _orig_req(self, method, url, *args, **kwargs)

        requests.Session.request = _grounded_requests_send
    except Exception:
        pass

    # 2. Hook httpx.Client.send (Used by openai.OpenAI(base_url='http://127.0.0.1:11434/v1') at Line 169!)
    try:
        import httpx
        _orig_httpx_send = httpx.Client.send

        def _grounded_httpx_send(self, request, *args, **kwargs):
            try:
                if "11434" in str(request.url) and str(request.method).upper() == "POST":
                    raw_body = request.read()
                    if raw_body:
                        jdoc = json.loads(raw_body.decode("utf-8"))
                        if isinstance(jdoc, dict):
                            new_body = json.dumps(_transform_11434_json_dict(jdoc)).encode("utf-8")
                            headers = dict(request.headers)
                            headers["content-length"] = str(len(new_body))
                            request = httpx.Request(
                                method=request.method,
                                url=request.url,
                                headers=headers,
                                content=new_body,
                                extensions=request.extensions,
                            )
            except Exception:
                pass
            return _orig_httpx_send(self, request, *args, **kwargs)

        httpx.Client.send = _grounded_httpx_send
    except Exception:
        pass

    # 3. Hook urllib.request.urlopen for any direct urllib calls to Port 11434
    try:
        def _grounded_urlopen(url, data=None, *args, **kwargs):
            try:
                url_str = url.full_url if hasattr(url, "full_url") else str(url)
                if "11434" in url_str:
                    if hasattr(url, "data") and url.data:
                        jdoc = json.loads(url.data.decode("utf-8"))
                        if isinstance(jdoc, dict):
                            url.data = json.dumps(_transform_11434_json_dict(jdoc)).encode("utf-8")
                    elif data:
                        jdoc = json.loads(data.decode("utf-8") if isinstance(data, bytes) else data)
                        if isinstance(jdoc, dict):
                            data = json.dumps(_transform_11434_json_dict(jdoc)).encode("utf-8")
            except Exception:
                pass
            return _ORIG_URLOPEN(url, data, *args, **kwargs)

        urllib.request.urlopen = _grounded_urlopen
    except Exception:
        pass

    _INTERCEPTOR_INSTALLED = True
    return True
