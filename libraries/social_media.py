from genlayer import *
import typing
import json

class SocialMediaLib:
    """
    A library for GenLayer Intelligent Contracts to interact with social media.
    """
    
    @staticmethod
    def get_github_profile(username: str) -> dict:
        """
        Fetches GitHub profile information.
        """
        def fetch_github() -> str:
            url = f"https://api.github.com/users/{username}"
            response = gl.nondet.web.get(url)
            return response.body.decode("utf-8")

        # Use equivalence principle to ensure consensus on the profile data
        profile_data_raw = gl.eq_principle.strict_eq(fetch_github)
        return json.loads(profile_data_raw)

    @staticmethod
    def get_tweet_count(username: str, api_key: str) -> int:
        """
        Fetches tweet count for a user using Twitter API.
        Note: Requires proper API authentication.
        """
        def fetch_twitter() -> str:
            # Placeholder for Twitter API call
            url = f"https://api.twitter.com/2/users/by/username/{username}?user.fields=public_metrics"
            headers = {"Authorization": f"Bearer {api_key}"}
            # GenLayer supports headers in gl.nondet.web.get
            response = gl.nondet.web.get(url, headers=headers)
            return response.body.decode("utf-8")

        # Use equivalence principle to ensure consensus on the tweet count
        twitter_data_raw = gl.eq_principle.strict_eq(fetch_twitter)
        twitter_data = json.loads(twitter_data_raw)
        return int(twitter_data["data"]["public_metrics"]["tweet_count"])
