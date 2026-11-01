# SAM.GOV / LOGIN.GOV 24-HOUR MFA PHONE NUMBER RESET & ENTITY ROLE RE-LINKING PLAYBOOK

* **Entity:** Humphrey Virtual Farms LLC (`701 E Drew, Madill, OK 73446-2620`)
* **Statutory Identifiers:** `CAGE Code: 1AHA8` | `SAM.gov UEI: S1M4ENLHTDH5` (`100% Active -- Unaffected by Personal Login.gov MFA Reset`)
* **Entity Administrator:** Jeffery Humphrey, Founder, President & CEO (`humphreyvirtualfarm@gmail.com` | Updated Phone: `(572) 358-9978`)
* **Shared Core C2 Merkle Root (`640` C2 Modules):** `d65049efcf06298f84d41436131794fc3cc5607873a2a596b5ad355f6ee67ccb`
* **Timestamp (UTC):** `2026-11-01T15:18:00.000000+00:00`

---

## 1. WHY THE 24-HOUR LOGIN.GOV RESET IS SAFE FOR `CAGE: 1AHA8` & `UEI: S1M4ENLHTDH5`
* Deleting and recreating a personal `Login.gov` sign-in profile due to a disconnected phone number **only** resets the personal authentication credential at `idp.int.identitysandbox.gov` / `secure.login.gov`.
* It **never** deletes, suspends, or modifies your company's active `SAM.gov` entity record (`Humphrey Virtual Farms LLC | CAGE: 1AHA8 | UEI: S1M4ENLHTDH5`). All five federal agencies (`DoD CDAO Tradewinds`, `DIU`, `DEVCOM ARL`, `USACE ERDC`, and `DHS S&T`) verify your company by `CAGE: 1AHA8` and `UEI: S1M4ENLHTDH5`.

---

## 2. STEP-BY-STEP EXECUTION ONCE THE 24-HOUR LOGIN.GOV TIMER COMPLETES
1. **Recreate Login.gov Using the Exact Same Email (`humphreyvirtualfarm@gmail.com`):**
   * Open the Login.gov confirmation email once the 24-hour waiting period finishes.
   * Click **Create an account** on `https://sam.gov` / `https://secure.login.gov` using **`humphreyvirtualfarm@gmail.com`**.
2. **Register TWO MFA Methods Immediately (`Phone` + `Backup Codes`):**
   * **Primary MFA:** Phone SMS/Voice at **`(572) 358-9978`**.
   * **Secondary MFA:** Select **Backup codes** (10-character recovery codes) and save the downloaded file into `C:\hvf_c2\backups\` so a phone replacement can never lock out the account again.
3. **Sign Into `SAM.gov` Workspace & Verify Entity Administrator Role (`UEI: S1M4ENLHTDH5`):**
   * If SAM.gov automatically matches `humphreyvirtualfarm@gmail.com`, navigate to **Account Details -> Public API Key** to rotate your optional API key.
   * If SAM.gov prompts to re-link your new Login.gov UUID to `Humphrey Virtual Farms LLC (UEI: S1M4ENLHTDH5)`, click **Request Role -> Entity Administrator** for `S1M4ENLHTDH5` and contact the **Federal Service Desk (`FSD.gov` | `1-866-606-8220`)** referencing `UEI: S1M4ENLHTDH5` and `CAGE: 1AHA8`.
