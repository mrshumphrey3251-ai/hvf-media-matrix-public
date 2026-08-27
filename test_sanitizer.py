import re

OFFICIAL_EMAIL = "humphreyvirtualfarm@gmail.com"
OFFICIAL_FOUNDER = "Jeffery Humphrey"

def sanitize_deterministic_output(raw_text: str) -> str:
    if not raw_text:
        return raw_text
    text = raw_text
    name_patterns = [
        r"(?i)\bHumphrey\s+[A-Z]\.?\s+Miller\b",
        r"(?i)\bHumphrey\s+Miller\b",
        r"(?i)\bMr\.?\s+Miller\b",
        r"(?i)\bJeffrey\s+Humphrey\b",
        r"(?i)\bJeff\s+Humphrey\b"
    ]
    for pattern in name_patterns:
        text = re.sub(pattern, OFFICIAL_FOUNDER, text)
    email_patterns = [
        r"(?i)[a-zA-Z0-9_.+-]+@hvf\.io",
        r"(?i)[a-zA-Z0-9_.+-]+@humphreyvirtualfarm\.io",
        r"(?i)[a-zA-Z0-9_.+-]+@humphreyvirtualfarms\.com"
    ]
    for pattern in email_patterns:
        text = re.sub(pattern, OFFICIAL_EMAIL, text)
    vc_patterns = [
        r"(?i)\$?\d+(\.\d+)?\s*(M|million|B|billion)\s*(in\s+)?(seed\s*(&|and)\s*)?(series[\s-]?[a-z]|venture\s+capital|funding|investment\s+round)",
        r"(?i)secured\s+\$?\d+[\d,]*\s*(million|M)\s+in\s+funding"
    ]
    for pattern in vc_patterns:
        text = re.sub(pattern, "sovereign, self-funded agricultural architecture", text)
    return text

# Test corrupted input
hallucinated_sample = (
    "Article by Humphrey J. Miller, Founder & CEO. "
    "Contact him at humphrey.miller@hvf.io. "
    "We have secured $14M in seed & series-A funding."
)

clean_result = sanitize_deterministic_output(hallucinated_sample)
print("\n--- SANITIZER VERIFICATION TEST ---")
print(f"INPUT : {hallucinated_sample}")
print(f"OUTPUT: {clean_result}")

assert "Humphrey J. Miller" not in clean_result, "Failed: Name hallucination remained"
assert "humphrey.miller@hvf.io" not in clean_result, "Failed: Fake email remained"
assert "$14M" not in clean_result, "Failed: Fake funding remained"
assert "Jeffery Humphrey" in clean_result, "Failed: Founder name missing"
assert "humphreyvirtualfarm@gmail.com" in clean_result, "Failed: Official email missing"
print("✅ [UNIT TEST PASSED]: Anti-hallucination filter is 100% deterministic!\n")