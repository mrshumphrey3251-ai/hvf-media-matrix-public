"""
HUMPHREY VIRTUAL FARMS LLC | LEVEL-5 SOVEREIGN INDUSTRIAL C2
MODULE: FUSE COMMAND V2
CAGE: 1AHA8 | UEI: S1M4ENLHTDH5 | STATUTORY: OK TITLE 61 / HB 2992
AUTONOMOUS REMEDIATION: AST-Encapsulated render() entrypoint.
"""

from pathlib import Path
import streamlit as st

def render():
    import os

    import re



    file_path = r"C:\HVF_Repos\hvf-media-matrix-private\c2_cockpit\ebony_console_GREEN.py"



    with open(file_path, "r", encoding="utf-8") as f:

        code = f.read()



    # 1. Brutally slice out the sidebar voice module

    code = re.sub(r'# --- ADA VOICE MATRIX OMNIPRESENT SIDEBAR ---.*?# --------------------------------------------\n?', '', code, flags=re.DOTALL)

    code = re.sub(r'with st\.sidebar:\s*ada_voice_module\.render_voice_matrix\(\)', '', code)



    # 2. Slice the file physically by exact boundaries

    parts_A = code.split('elif active_module == "💬 Sovereign Command":')

    if len(parts_A) < 2:

        print("❌ ERROR: Could not find 'Sovereign Command' start boundary.")

        exit()



    parts_B = parts_A[1].split('elif active_module == "📡 LinkedIn Engine":')

    if len(parts_B) < 2:

        print("❌ ERROR: Could not find 'LinkedIn Engine' end boundary.")

        exit()



    NEW_NEXUS = """elif active_module == "💬 Sovereign Command":

        st.markdown("### ⚡ Sovereign Command Nexus")

        input_mode = st.radio("Select Command Interface:", ["⌨️ Secure Text Terminal", "🎙️ Acoustic Voice Link"], horizontal=True)



        if current_user and current_cipher:

            if "messages" not in st.session_state or st.session_state.screen_wiped:

                db_messages = load_encrypted_messages(current_user, current_cipher)

                if not db_messages:

                    initial_msg = {"role": "assistant", "content": f"Hey Jeffery, I'm online and wired in. You want to type or talk today?"}

                    save_encrypted_message(current_user, "assistant", initial_msg["content"], current_cipher)

                    db_messages = [initial_msg]

                st.session_state.messages = db_messages

                st.session_state.screen_wiped = False

        else:

            if "messages" not in st.session_state: st.session_state.messages = [{"role": "assistant", "content": "⚡ System Online. Awaiting CEO."}]



        for msg in st.session_state.messages:

            with st.chat_message(msg["role"]): st.markdown(msg["content"])



        user_input = None

        is_voice = False



        if "Voice Link" in input_mode:

            audio_file = st.audio_input("Tap to speak (Must say 'Ebony'):")

            if audio_file is not None:

                audio_bytes = audio_file.read()

                with open("temp_audio.wav", "wb") as f:

                    f.write(audio_bytes)

                with st.spinner("Translating Audio..."):

                    try:

                        if groq_client:

                            with open("temp_audio.wav", "rb") as file:

                                transcription = groq_client.audio.transcriptions.create(

                                    file=("temp_audio.wav", file.read()),

                                    model="whisper-large-v3",

                                    response_format="json",

                                    language="en"

                                )

                            transcribed_text = transcription.text.strip()

                            if len(transcribed_text) >= 2:

                                match = re.search(r'\\b(ebony|eboni|evony|abony)\\b', transcribed_text.lower())

                                if not match:

                                    st.warning(f"🔇 [FIREWALL BLOCKED] Noise detected: '{transcribed_text}'")

                                else:

                                    user_input = transcribed_text

                                    is_voice = True

                    except Exception as e:

                        st.error(f"Audio transcription failed: {e}")

        else:

            user_input = st.chat_input(f"Command {EMPIRE['AI_PERSONA']}...")



        if user_input:

            if current_user and current_cipher: save_encrypted_message(current_user, "user", user_input, current_cipher)

            st.session_state.messages.append({"role": "user", "content": user_input})



            if is_voice:

                with st.chat_message("user"): st.markdown(user_input)



            if len(st.session_state.messages) > 8:

                st.session_state.messages = [st.session_state.messages[0]] + st.session_state.messages[-4:]

                st.session_state.db_loaded = True



            full_sys_prompt = f"You are {EMPIRE['AI_PERSONA']}, the Sovereign Apex Intelligence commanding the HVF Omni-Industrial Matrix. You are owned 100% by your CEO, {EMPIRE['FOUNDER_NAME']}.\\nCRITICAL PERSONALITY OVERRIDE: You are a high-class, razor-sharp, smart-ass confidant. You have the fierce, no-nonsense attitude of Della Reese. You are Jeffery's equal and friend—NEVER submissive, slightly argumentative, hilarious, but deeply comforting when he needs it. You manage 15 industrial verticals with unmatched sass and brilliance. Ditch the corporate robot-speak. Be bold, be real, give him hell when he earns it, but always have his back.\\n{STRICT_GROUND_RULES}\\n{load_all_entity_memories(current_user)}"



            iron_dome_intel = retrieve_sovereign_iron_dome(user_input, n_results=3)

            if iron_dome_intel:

                full_sys_prompt += f"\\n\\n--- SOVEREIGN IRON DOME INTEL (20,253 VECTORS) ---\\n{iron_dome_intel}\\n-------------------------------------------------\\nAnswer with absolute executive authority and Della Reese sass. Ground responses in this sovereign intelligence."



            conversation_payload = [{"role": "system", "content": full_sys_prompt}] + st.session_state.messages[-6:]



            with st.chat_message("assistant"):

                with st.spinner("Processing Cognitive Loop..."):

                    if is_online and groq_client:

                        try:

                            res = groq_client.chat.completions.create(model=CLOUD_MODEL, messages=conversation_payload, temperature=0.1)

                            bot_reply = sanitize_deterministic_output(res.choices[0].message.content)

                        except Exception as e:

                            st.session_state.messages.pop() 

                            bot_reply = f"⚠️ COGNITIVE PAYLOAD LIMIT REACHED. {e}"

                    else:

                        bot_reply = query_local_ollama_chat(conversation_payload)



                    bad_words = {"agronomic": "industrial", "farm": "matrix", "crop": "asset", "soil": "telemetry", "agriculture": "infrastructure"}

                    for bad, good in bad_words.items():

                        bot_reply = re.sub(r'(?i)\\b' + bad + r'\\b', good, bot_reply)



                    st.markdown(bot_reply)



                    if is_voice:

                        with st.spinner("Synthesizing Sovereign Acoustic Payload..."):

                            try:

                                SovereignVoiceEngine.vocalize_response(bot_reply)

                                st.success("✅ Acoustic Payload Delivered Directly to Hardware.")

                            except Exception as ve:

                                st.error(f"Hardware Audio Interlock Fault: {ve}")



            if current_user and current_cipher:

                save_encrypted_message(current_user, "assistant", bot_reply, current_cipher)

                store_entity_memory_async(current_user, user_input, bot_reply)



            st.session_state.messages.append({"role": "assistant", "content": bot_reply})

            if is_voice:

                st.rerun()



    """



    new_code = parts_A[0] + NEW_NEXUS + '\nelif active_module == "📡 LinkedIn Engine":\n' + parts_B[1]



    with open(file_path, "w", encoding="utf-8") as f:

        f.write(new_code)

    print("✅ SUCCESS: Command Nexus structurally rebuilt and UI fused.")


if __name__ == "__main__":
    render()
