import csv
import os
import glob

# Clear previous payloads
for f in glob.glob("OUTBOX/*_payload.txt"):
    os.remove(f)

location = os.environ.get("HVF_LOCATION", "United States")
github_link = "https://github.com/mrshumphrey3251-ai/hvf-media-matrix-public"

with open('tier1_targets.csv', 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        contact = row['Contact_Vector']
        pub = row['Publication']
        
        # Only target valid emails, ignore redacted public vectors
        if "@" not in contact:
            continue
            
        body = f"To: <{contact}>\nSubject: Technical Addendum: Project Ebony Open-Source Repository & HQ Coordinates\n\n"
        body += f"To the Editorial Desk at {pub},\n\n"
        body += "Following our prior transmission regarding Project Ebony, we are formally appending our physical operational coordinates and the public GitHub repository containing the redacted architectural blueprints of this broadcast engine.\n\n"
        body += f"Public Repository: {github_link}\n"
        body += f"Operational Location: {location}\n\n"
        body += "Jeffery Humphrey\nChief Architect, Project Ebony\n"
        
        with open(f"OUTBOX/{pub}_payload.txt", 'w') as out_f:
            out_f.write(body)

print("[HVF SYSTEM] Addendum payloads successfully staged in OUTBOX.")
