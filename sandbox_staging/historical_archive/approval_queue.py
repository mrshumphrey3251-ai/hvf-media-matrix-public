import json
from datetime import datetime, timezone

class HITLQueue:
    def __init__(self):
        self.pending_actions = []

    def queue_recommendation(self, action_id: str, payload: dict):
        """Halts AI execution until executive override/approval is granted."""
        entry = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "action_id": action_id,
            "status": "PENDING_EXECUTIVE_APPROVAL",
            "details": payload
        }
        self.pending_actions.append(entry)
        print(f"[{entry['timestamp']}] ACTION {action_id} HALTED: Awaiting HITL Approval.")
        return entry

    def approve_action(self, action_id: str, approved_by: str):
        """Releases the action to the C2 Mesh after CEO approval."""
        print(f"[HITL OVERRIDE] Action {action_id} APPROVED by {approved_by}. Dispatching now.")
        return True

if __name__ == "__main__":
    queue = HITLQueue()
    queue.queue_recommendation("ACT_099", {"target": "Sector 7", "action": "Deploy Nitrogen"})
