import urllib.request
import re

def execute_recon(target_url):
    print(f"[EBONY RECON]: Initiating tactical sweep on {target_url}...")
    try:
        # Masking the approach as an executive crawler
        req = urllib.request.Request(
            target_url, 
            data=None, 
            headers={'User-Agent': 'EbonyMatrix/1.0 (Executive Recon; +Corporate)'}
        )
        with urllib.request.urlopen(req, timeout=10) as response:
            html = response.read().decode('utf-8')
            
            # Brutal HTML stripping for raw data extraction
            raw_text = re.sub(r'<style.*?</style>', '', html, flags=re.DOTALL)
            raw_text = re.sub(r'<script.*?</script>', '', raw_text, flags=re.DOTALL)
            raw_text = re.sub(r'<[^>]+>', ' ', raw_text)
            
            # Compress and clean the payload
            clean_text = ' '.join(raw_text.split())
            print("[EBONY RECON]: Target acquired and neutralized into raw data.")
            
            # Snatch the first 15,000 characters to prevent memory overflow
            return clean_text[:15000] 
            
    except Exception as e:
        error_msg = f"[EBONY RECON]: Tactical sweep failed. Target defended or offline. Error: {e}"
        print(error_msg)
        return error_msg

if __name__ == "__main__":
    # Internal diagnostic test
    test_data = execute_recon("https://example.com")
    print(f"\n[EXTRACTION PREVIEW]:\n{test_data[:500]}...\n[STATUS]: Optic Nerve Online.")
