### Sovereign C2 Cockpit - Air-Gap Queue & Dispatch Schema

#### Staged Dispatch States
| Status Code | Operational Behavior | Air-Gap Safe |
| :--- | :--- | :--- |
| `PENDING_CEO_APPROVAL` | Ingested via IMAP SSL; awaiting executive review | Yes (Local Vault) |
| `QUEUED_SOVEREIGN_LOCAL` | Approved offline; network socket suppressed | Yes (Air-Gapped) |
| `DISPATCHED_SUCCESS` | Verified TLS 1.3 release with non-null cryptographic `dispatched_at` timestamp | Network Authenticated |
| `ARCHIVED_NOISE` | Suppressed bulk notifications / unsolicited marketing | Yes (Local Vault) |
| `DISMISSED_BY_CEO` | Executive override suppression | Yes (Local Vault) |

All outbound operations strictly adhere to OK Title 61 / HB 2992 statutory audit standards.
