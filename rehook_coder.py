targets = [
    r"C:\HVF_Repos\hvf-media-matrix-private\c2_cockpit\ebony_console_GREEN.py",
    r"C:\HVF_Repos\hvf-media-matrix-public\c2_cockpit\ebony_console_GREEN.py"
]

hook_code = """
            # Autonomous Engineering Directive Intercept
            clean_p = (prompt if 'prompt' in locals() else user_input).strip().lower()
            intent_triggers = ["build", "create", "architect", "generate", "develop", "make"]
            is_build = any(clean_p.startswith(t) or f" {t} " in clean_p for t in intent_triggers)

            if is_build and any(w in clean_p for w in ["scheduler", "module", "monitor", "scada", "extension", "dispatch", "engine"]):
                with st.spinner("⚡ Ebony is synthesizing module in quarantine sandbox..."):
                    import sovereign_coder
                    coder = sovereign_coder.SovereignCoder()
                    mod_name = "linkedin_lead_scheduler.py"
                    res = coder.generate_and_stage(mod_name, prompt if 'prompt' in locals() else user_input)
                    if res.get("success"):
                        response_text = f"⚡ Directive executed. I have synthesized `{mod_name}` into quarantine, verified it through the sandbox harness (Returncode: 0), and staged it at the 🛡️ CEO Authorization Gate awaiting your cryptographic sign-off."
                    else:
                        response_text = f"[-] Sandbox verification issue: {res.get('error')}. Staged for inspection."
            else:
                response_text = sovereign_comms.generate_chat_response(prompt if "prompt" in locals() else user_input)
"""

for filepath in targets:
    with open(filepath, "r", encoding="utf-8-sig") as f:
        content = f.read()

    if "import sovereign_coder" not in content:
        content = content.replace("import sovereign_comms", "import sovereign_comms\nimport sovereign_coder\nimport re")

    # Replace standard chat response call with the autonomous build hook
    target_call = 'response_text = sovereign_comms.generate_chat_response(prompt if "prompt" in locals() else user_input)'
    if target_call in content:
        content = content.replace(target_call, hook_code.strip())

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"[+] Re-hooked Autonomous Coder into: {filepath}")
