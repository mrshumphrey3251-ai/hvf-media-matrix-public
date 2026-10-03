import os
import sys
import email_triage_core
import importlib
importlib.reload(email_triage_core)

# ==============================================================================
# HVF Omni-Industrial Matrix | SOVEREIGN INGESTION DISPATCH TRIGGER
# Authority: Jeffery Humphrey, Founder & CEO (CAGE: 1AHA8, UEI: S1M4ENLHTDH5)
# System: Live Polling Cycle across Authenticated Inboxes
# ==============================================================================

print("=" * 80)
print("STARTING LIVE INGESTION CYCLE ACROSS CONFIGURED INBOXES")
print("=" * 80)

email_triage_core.run_multi_account_cycle()

print("\n" + "=" * 80)
print("LIVE INGESTION CYCLE COMPLETE: PROCEED TO SOVEREIGN DISPATCH DECK FOR REVIEW")
print("=" * 80)
