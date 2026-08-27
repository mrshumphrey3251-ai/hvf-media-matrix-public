import requests, json, csv, time

# ----- CONFIG -----
candidates = ["TerraLoom", "FarmPulse", "AgriVerse", "CultivaX",
              "VerdantPlay", "EcoScapeMedia", "HarvestForge", "NexField"]
uspto_api = "https://developer.uspto.gov/ibd-api/v1/application/publications"
whois_api = "https://api.domainsdb.info/v1/domains/search"

def uspto_search(name):
    """Very lightweight search – returns count of exact matches."""
    params = {"searchText": f'"{name}"', "publicationFromDate": "2020-01-01"}
    r = requests.get(uspto_api, params=params, timeout=10)
    data = r.json()
    return data.get("response", {}).get("numFound", 0)

def whois_check(name):
    r = requests.get(whois_api, params={"domain": f"{name.lower()}.com"}, timeout=10)
    return r.json().get("domains", []) == []

results = []
for n in candidates:
    tm_hits = uspto_search(n)
    domain_free = whois_check(n)
    results.append([n, tm_hits, domain_free])
    time.sleep(0.2)  # polite rate‑limit

# Write CSV for quick review
with open("brand_check_results.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["Name", "USPTO ExactMatches", "ComDomainFree"])
    writer.writerows(results)

print("✅ Brand check complete – see brand_check_results.csv")