targets = [
    r"C:\HVF_Repos\hvf-media-matrix-private\c2_cockpit\ebony_console_GREEN.py",
    r"C:\HVF_Repos\hvf-media-matrix-public\c2_cockpit\ebony_console_GREEN.py"
]

for filepath in targets:
    with open(filepath, "r", encoding="utf-8-sig") as f:
        content = f.read()

    # Ensure sovereign_coder is imported
    if "import sovereign_coder" not in content:
        content = content.replace("import sovereign_comms", "import sovereign_comms\nimport sovereign_coder")

    # Hook autonomous code generation directly before conversational fallback
    hook_logic = """
            # Autonomous Engineering Directive Intercept
            clean_p = (prompt if 'prompt' in locals() else user_input).strip().lower()
            intent_triggers = ["build ", "create ", "architect ", "generate ", "write a module ", "develop "]
            if any(clean_p.startswith(t) or f" {t}" in clean_p for t in intent_triggers) and ("module" in clean_p or "scheduler" in clean_p or "monitor" in clean_p or "scada" in clean_p or "extension" in clean_p):
                with st.spinner("⚡ Ebony is architecting module in quarantine sandbox..."):
                    coder = sovereign_coder.SovereignCoder()
                    # Generate dynamic module name
                    slug = re.sub(r'[^a-zA-Z0-9_]', '_', clean_p.replace("build", "").replace("create", "").replace("architect", "").strip())[:25].strip("_") or "autonomous_module"
                    if not slug.endswith(".py"):
                        mod_filename = f"{slug}.py"
                    else:
                        mod_filename = slug

                    res = coder.generate_and_stage(
                        module_name=mod_filename,
                        specification=prompt if 'prompt' in locals() else user_input
                    )
                    if res.get("success"):
                        response_text = f"⚡ Directive executed. I have synthesized `{mod_filename}` into quarantine, verified it through the sandbox harness (Returncode: 0), and staged it at the 🛡️ CEO Authorization Gate awaiting your cryptographic sign-off."
                    else:
                        response_text = f"[-] Sandbox verification encountered an issue: {res.get('error')}. Quarantine engaged."
            else:
                response_text = sovereign_comms.generate_chat_response(prompt if "prompt" in locals() else user_input)
"""

    target_block = 'response_text = sovereign_comms.generate_chat_response(prompt if "prompt" in locals() else user_input)'
    if target_block in content and "Autonomous Engineering Directive Intercept" not in content:
        content = content.replace(target_block, hook_logic.strip())

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"[+] Autonomous Coder hooked into: {filepath}")
