import requests
import os
from dotenv import load_dotenv
from crewai_tools import BaseTool

class LinkedInPostingTool(BaseTool):
    name = "linkedin_poster"
    description = "Posts content to LinkedIn using a developer app. Input should be the text content to post."
    
    def __init__(self):
        super().__init__()
        load_dotenv()
        # Expect these in your .env file:
        # LINKEDIN_ACCESS_TOKEN: your OAuth access token
        # LINKEDIN_AUTHOR_URN: your LinkedIn author URN (e.g. "urn:li:person:xxxxxxxx")
        self.access_token = os.getenv("LINKEDIN_ACCESS_TOKEN")
        self.author_urn = os.getenv("LINKEDIN_AUTHOR_URN")
        
        if not self.access_token or not self.author_urn:
            raise ValueError("LinkedIn credentials not found in .env file. Please set LINKEDIN_ACCESS_TOKEN and LINKEDIN_AUTHOR_URN.")
        
    def _run(self, post_content: str) -> str:
        """
        Posts content to LinkedIn using the official LinkedIn API.
        
        Args:
            post_content (str): The content to post on LinkedIn.
            
        Returns:
            str: Success or error message.
        """
        url = "https://api.linkedin.com/v2/ugcPosts"
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "X-Restli-Protocol-Version": "2.0.0",
            "Content-Type": "application/json"
        }
        payload = {
            "author": self.author_urn,
            "lifecycleState": "PUBLISHED",
            "specificContent": {
                "com.linkedin.ugc.ShareContent": {
                    "shareCommentary": {
                        "text": post_content
                    },
                    "shareMediaCategory": "NONE"
                }
            },
            "visibility": {
                "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
            }
        }
        
        try:
            response = requests.post(url, headers=headers, json=payload)
            if response.status_code == 201:
                return "Successfully posted to LinkedIn!"
            else:
                return f"Error posting to LinkedIn: {response.status_code} {response.text}"
        except Exception as e:
            return f"Error posting to LinkedIn: {str(e)}"
    
    def _arun(self, post_content: str) -> str:
        """
        Async version of the LinkedIn posting tool.
        """
        raise NotImplementedError("Async version not implemented")
