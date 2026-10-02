import os
from dotenv import load_dotenv

# Force load and override to bypass cache
load_dotenv(override=True)

groq = os.getenv("GROQ_API_KEY")
li_token = os.getenv("LINKEDIN_ACCESS_TOKEN")
li_urn = os.getenv("LINKEDIN_AUTHOR_URN")

print("\n--- [EBONY MATRIX: AMMUNITION CHECK] ---")
print(f"GROQ_API_KEY          : {'[LOADED]' if groq else '[MISSING]'}")
print(f"LINKEDIN_ACCESS_TOKEN : {'[LOADED]' if li_token else '[MISSING]'}")
print(f"LINKEDIN_AUTHOR_URN   : {'[LOADED]' if li_urn else '[MISSING]'}")
print("----------------------------------------")

if li_urn and not li_urn.startswith("urn:li:person:"):
    print("[WARNING]: Your LINKEDIN_AUTHOR_URN is improperly formatted. It must start exactly with 'urn:li:person:'")
elif li_urn and li_token:
    print("[SYSTEM]: Chamber is fully loaded. Ready to fire.")
else:
    print("[SYSTEM]: Chamber is empty. Matrix is blind to the keys.")
print("\n")
