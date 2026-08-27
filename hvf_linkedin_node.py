import logging
import os
import requests
from dotenv import load_dotenv

# HVF Media Matrix - LinkedIn API Node (Private/Unredacted)
# Engineered for secure REST API outbound transmission

class HVFLinkedInNode:
    def __init__(self):
        self.logger = logging.getLogger("HVF_LinkedIn_Node")
        load_dotenv()
        self.access_token = os.getenv("LINKEDIN_API_KEY")

    def dispatch(self, payload):
        self.logger.info("Initializing live LinkedIn API vector...")
        
        if not self.access_token or self.access_token == "PLACEHOLDER_AWAITING_LIVE_KEY":
            self.logger.warning("LinkedIn Aborted: Live transmission keys not detected in vault.")
            return False

        try:
            headers = {
                'Authorization': f'Bearer {self.access_token}',
                'X-Restli-Protocol-Version': '2.0.0',
                'Content-Type': 'application/json'
            }

            self.logger.info("Authenticating token and extracting author URN...")
            profile_response = requests.get('https://api.linkedin.com/v2/userinfo', headers=headers)
            
            if profile_response.status_code != 200:
                self.logger.error(f"LinkedIn Authentication Failed: {profile_response.text}")
                return False
                
            author_urn = f"urn:li:person:{profile_response.json().get('sub')}"
            
            post_data = {
                "author": author_urn,
                "lifecycleState": "PUBLISHED",
                "specificContent": {
                    "com.linkedin.ugc.ShareContent": {
                        "shareCommentary": {"text": payload},
                        "shareMediaCategory": "NONE"
                    }
                },
                "visibility": {"com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"}
            }

            self.logger.info("Syndicating intel payload to LinkedIn feed...")
            post_response = requests.post('https://api.linkedin.com/v2/ugcPosts', headers=headers, json=post_data)
            
            if post_response.status_code == 201:
                self.logger.info("Payload successfully syndicated to professional network.")
                return True
            else:
                self.logger.error(f"LinkedIn Transmission Failed: {post_response.text}")
                return False

        except Exception as e:
            self.logger.error(f"LinkedIn API Error: {e}")
            return False
