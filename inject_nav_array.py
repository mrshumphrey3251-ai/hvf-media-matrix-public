import sys

file_path = "ebony_console_GREEN.py"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# Locate the start of the navigation array dynamically
start_str = 'st.radio("Navigation", ['
start_idx = content.find(start_str)

if start_idx != -1:
    # Find the closing bracket of the array
    end_idx = content.find(']', start_idx)
    if end_idx != -1:
        nav_block = content[start_idx:end_idx]
        
        if "Sovereign Comms Deck" not in nav_block:
            # Strip trailing whitespace from the current list
            new_nav_block = nav_block.rstrip()
            
            # Ensure the last item has a comma before we append ours
            if not new_nav_block.endswith(','):
                new_nav_block += ','
                
            # Append the Comms Deck module
            new_nav_block += '\n        "📡 Sovereign Comms Deck"\n    '
            
            # Rebuild the file content
            content = content[:start_idx] + new_nav_block + content[end_idx:]
            print("[SUCCESS] Comms Deck dynamically injected into the navigation array.")
        else:
            print("[NOTICE] Comms Deck is already present in the navigation array.")
    else:
        print("[ERROR] Could not find closing bracket of navigation array.")
else:
    print("[ERROR] Could not locate 'st.radio(\"Navigation\", [' in the file.")

# Write the updated content back cleanly
with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)
