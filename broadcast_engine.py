import csv
import os

print("[HVF SYSTEM] Initializing API Broadcast Engine...")
os.makedirs('OUTBOX', exist_ok=True)

with open('FOR_IMMEDIATE_RELEASE_EBONY.md', 'r') as f:
    core_payload = f.read()

with open('tier1_targets.csv', 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        if row['Status'] == 'Pending':
            pub = row['Publication']
            desk = row['Journalist_Name']
            vector = row['Contact_Vector']
            
            email_content = f"To: {desk} <{vector}>\n"
            if pub == 'Wired':
                email_content += f"Subject: Op-Ed Pitch: The End of Cloud-Dependent Autonomous Machinery\n\n"
            else:
                email_content += f"Subject: FOR IMMEDIATE RELEASE: Project Ebony Declassification\n\n"
            
            email_content += f"Attention {pub} {desk},\n\n"
            email_content += core_payload
            
            filename = f"OUTBOX/{pub}_payload.txt"
            with open(filename, 'w') as out:
                out.write(email_content)
            print(f" -> Staged custom payload for {pub} [{vector}]")

print("[HVF SYSTEM] All Tier-1 payloads staged in OUTBOX.")
