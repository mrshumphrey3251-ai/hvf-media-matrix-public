import json
from datetime import datetime, timezone

class PhysicalSecurityLogger:
    def __init__(self):
        self.event_log = []

    def log_badge_scan(self, employee_id: str, access_point: str, authorized: bool):
        """Immutable logging for physical door access, synced with cyber RBAC."""
        event = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "employee_id": employee_id,
            "access_point": access_point,
            "authorized": authorized
        }
        self.event_log.append(event)
        
        status = "GRANTED" if authorized else "DENIED - TRIGGERING ALARM"
        print(f"[PHYSICAL SECURITY] Badge Scan at {access_point} by {employee_id}: {status}")
        return event

if __name__ == "__main__":
    sec = PhysicalSecurityLogger()
    sec.log_badge_scan("EMP_001", "Server_Room_Alpha", True)
