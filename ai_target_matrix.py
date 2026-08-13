import os

print("[HVF AI MATRIX] Initializing Strategic Target Scoring...")

# High-value enterprise triggers
TIER_1_KEYWORDS = ['defense', 'aerospace', 'robotics', 'automation', 'space', 'military']
TIER_2_KEYWORDS = ['contract', 'funding', 'billion', 'million', 'acquisition', 'ceo', 'founder']

input_log = "/home/mrshumphrey3251/HVF_INTEL_SCRAPER/osint_targets.log"
output_log = "/home/mrshumphrey3251/HVF_INTEL_SCRAPER/scored_targets.log"

if not os.path.exists(input_log):
    print("[!] Target log empty or offline. Standing by.")
    exit(0)

scored_data = []
with open(input_log, "r") as f:
    lines = f.readlines()

current_target = ""
for line in lines:
    if line.startswith("[TARGET ACQUIRED]"):
        current_target = line
    elif line.startswith("URL:"):
        url = line
        score = 50 # Base operational score
        text_to_analyze = current_target.lower()
        
        for kw in TIER_1_KEYWORDS:
            if kw in text_to_analyze: score += 15
        for kw in TIER_2_KEYWORDS:
            if kw in text_to_analyze: score += 10
        
        score = min(score, 99) # Maximum score limit
        
        if score >= 80:
            classification = "[CLASS A - IMMEDIATE ENGAGEMENT]"
        elif score >= 65:
            classification = "[CLASS B - HIGH VALUE]"
        else:
            classification = "[CLASS C - MONITOR]"
            
        scored_data.append(f"STRATEGIC VALUE: {score}/99 {classification}\n{current_target}{url}\n")
        current_target = ""

with open(output_log, "w") as f:
    f.writelines(scored_data)

print(f"[HVF AI MATRIX] Targets successfully evaluated and locked in: {output_log}")
