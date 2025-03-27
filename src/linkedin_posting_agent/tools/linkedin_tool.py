import requests
import os
from dotenv import load_dotenv
from authlib.integrations.requests_client import OAuth2Session

load_dotenv(override=True)

class LinkedInOAuth:
    def __init__(self, client_id=None, client_secret=None, redirect_uri=None, scopes=None):
        self.client_id = client_id or os.getenv("LINKEDIN_CLIENT_ID")
        self.client_secret = client_secret or os.getenv("LINKEDIN_CLIENT_SECRET")
        self.redirect_uri = redirect_uri or "http://localhost:8000/callback"  # Default redirect URI
        self.scopes = scopes or ["w_member_social", "profile", "openid"]  # Default scopes
        self.authorization_base_url = "https://www.linkedin.com/oauth/v2/authorization"
        self.token_url = "https://www.linkedin.com/oauth/v2/accessToken"
        self.profile_url = "https://api.linkedin.com/v2/me"
        self.share_url = "https://api.linkedin.com/v2/ugcPosts"
        self.oauth = OAuth2Session(
            client_id=self.client_id, client_secret=self.client_secret, redirect_uri=self.redirect_uri, scope=self.scopes
        )

    def get_authorization_url(self):
        """Generates the LinkedIn authorization URL."""
        authorization_url, state = self.oauth.create_authorization_url(self.authorization_base_url)
        return authorization_url, state

    def fetch_token(self, authorization_response, state):
        """Fetches the access token from LinkedIn."""
        token = self.oauth.fetch_token(
            url=self.token_url,
            grant_type='authorization_code',
            client_secret=self.client_secret,
            authorization_response=authorization_response,
            state=state
        )
        return token

    def get_linkedin_profile(self, token):
        """Fetches the user's LinkedIn profile."""
        oauth = OAuth2Session(self.client_id, token=token)
        profile = oauth.get(self.profile_url).json()
        return profile

    def post_content(self, token, content):
        """Posts content to LinkedIn."""
        oauth = OAuth2Session(self.client_id, token=token)
        headers = {
            "X-Restli-Protocol-Version": "2.0.0",
            "Content-Type": "application/json"
        }
        payload = {
            "author": f"urn:li:person:{token['id']}",
            "lifecycleState": "PUBLISHED",
            "specificContent": {
                "com.linkedin.ugc.ShareContent": {
                    "shareCommentary": {
                        "text": content
                    },
                    "shareMediaCategory": "NONE"
                }
            },
            "visibility": {
                "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
            }
        }
        response = oauth.post(self.share_url, headers=headers, json=payload)
        if response.status_code == 201:
            return "Successfully posted to LinkedIn!"
        else:
            return f"Error posting to LinkedIn: {response.status_code} {response.text}"
