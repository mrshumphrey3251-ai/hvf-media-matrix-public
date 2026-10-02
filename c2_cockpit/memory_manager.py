import streamlit as st

class ContextManager:
    def __init__(self, token_limit=7500):
        # Set safely below the 8000 limit to prevent 413 Cloud Faults
        self.token_limit = token_limit

    def approximate_tokens(self, text: str) -> int:
        """Industry standard approximation: 1 token is roughly 4 characters."""
        return len(text) // 4

    def prune_history(self, messages: list):
        """Automatically drops the oldest messages when approaching the limit."""
        current_tokens = sum(self.approximate_tokens(str(m)) for m in messages)
        
        # Keep pruning until we are under the safety threshold, always preserving the system prompt
        while current_tokens > self.token_limit and len(messages) > 2:
            messages.pop(1) 
            current_tokens = sum(self.approximate_tokens(str(m)) for m in messages)
            
        return messages

    def render_purge_button(self):
        """Renders the executive override button to manually clear the screen and reset tokens."""
        if st.sidebar.button("⚠️ Purge AI Memory (Reset Tokens)"):
            if "messages" in st.session_state:
                st.session_state.messages = []
            st.sidebar.success("Matrix Memory Purged. Token limit reset to zero.")
            st.rerun()

if __name__ == "__main__":
    print("HVF Token Optimization Engine Initialized. Circuit breakers active.")
