# hvf_linkedin_engine.py - HVF Tactical Broadcast Engine (Private)
# Engineered to execute executive messaging and network dominance.

import urllib.request
import urllib.error
import json
import logging
from hvf_config_vault import ConfigVault

class LinkedInEngine:
    def __init__(self):
        self.logger = logging.getLogger("HVF_LinkedIn")
        self.vault = ConfigVault()
        self.token = self.vault.get("LINKEDIN_ACCESS_TOKEN")
        self.logger.info("LinkedIn Tactical Engine initialized and armed with live credentials.")

    def _get_author_urn(self):
        url = "https://api.linkedin.com/v2/userinfo"
        req = urllib.request.Request(url, headers={'Authorization': f'Bearer {self.token}'})
        try:
            response = urllib.request.urlopen(req)
            data = json.loads(response.read().decode('utf-8'))
            return f"urn:li:person:{data['sub']}"
        except Exception as e:
            self.logger.error(f"Failed to retrieve Author URN. Perimeter blockade: {e}")
            return None

    def deploy_message(self, message):
        if not self.token or self.token == "NOT_SET":
            self.logger.error("Deployment aborted. Access token missing.")
            return False

        author_urn = self._get_author_urn()
        if not author_urn:
            return False

        self.logger.info(f"Target locked. Author URN secured. Preparing payload...")
        
        url = "https://api.linkedin.com/v2/ugcPosts"
        headers = {
            'Authorization': f'Bearer {self.token}',
            'X-Restli-Protocol-Version': '2.0.0',
            'Content-Type': 'application/json'
        }
        
        payload = {
            "author": author_urn,
            "lifecycleState": "PUBLISHED",
            "specificContent": {
                "com.linkedin.ugc.ShareContent": {
                    "shareCommentary": {"text": message},
                    "shareMediaCategory": "NONE"
                }
            },
            "visibility": {"com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"}
        }

        req = urllib.request.Request(url, data=json.dumps(payload).encode('utf-8'), headers=headers, method='POST')
        
        try:
            response = urllib.request.urlopen(req)
            if response.getcode() == 201:
                self.logger.info(f"TACTICAL STRIKE SUCCESSFUL. Message deployed to LinkedIn network.")
                return True
        except urllib.error.HTTPError as e:
            self.logger.error(f"API Error: {e.code} - {e.read().decode('utf-8')}")
        except Exception as e:
            self.logger.error(f"Critical execution failure: {str(e)}")
        
        return False

    def run(self, payload=None):
        """
        The mandatory execution method. Engineered for dynamic payload injection.
        """
        self.logger.info("Executing live LinkedIn broadcast sequence...")
        
        # DYNAMIC EXTRACTION: If a message is passed, use it. Otherwise, use the default.
        if payload and "message" in payload:
            executive_payload = payload["message"]
            self.logger.info("Dynamic executive payload intercepted and loaded.")
        else:
            executive_payload = "The HVF Media Matrix Sovereign Core is now online and fully armed."
            
        self.deploy_message(executive_payload)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    engine = LinkedInEngine()
    engine.run()