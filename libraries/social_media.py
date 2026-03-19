from genlayer import *
import typing
import json

class SocialMediaLib:
    """
    A library for GenLayer Intelligent Contracts to interact with social media APIs.
    Supports GitHub and provides a placeholder for Twitter integration with robust error handling.
    """
    
    @staticmethod
    def _fetch_github_profile(username: str) -> typing.Optional[dict]:
        """
        Fetches GitHub profile information.
        """
        try:
            url = f"https://api.github.com/users/{username}"
            response = gl.nondet.web.get(url)
            if response.status_code == 200:
                return json.loads(response.body.decode("utf-8"))
            else:
                print(f"GitHub API error for {username}: {response.status_code} - {response.body.decode("utf-8")}")
                return None
        except Exception as e:
            print(f"Error fetching from GitHub for {username}: {e}")
            return None

    @staticmethod
    def _fetch_twitter_metrics(username: str, api_key: str) -> typing.Optional[dict]:
        """
        Fetches Twitter user metrics (e.g., tweet count) using the Twitter API v2.
        Requires a bearer token (api_key) for authentication.
        """
        try:
            url = f"https://api.twitter.com/2/users/by/username/{username}?user.fields=public_metrics"
            headers = {"Authorization": f"Bearer {api_key}"}
            response = gl.nondet.web.get(url, headers=headers)
            if response.status_code == 200:
                data = json.loads(response.body.decode("utf-8"))
                if "data" in data and "public_metrics" in data["data"]:
                    return data
                else:
                    print(f"Twitter API error for {username}: Invalid response format. {data}")
                    return None
            else:
                print(f"Twitter API error for {username}: {response.status_code} - {response.body.decode("utf-8")}")
                return None
        except Exception as e:
            print(f"Error fetching from Twitter for {username}: {e}")
            return None

    @staticmethod
    def get_github_profile(username: str) -> typing.Optional[dict]:
        """
        Fetches GitHub profile information for a given username.
        """
        profile_data = gl.eq_principle.strict_eq(lambda: SocialMediaLib._fetch_github_profile(username))
        return profile_data

    @staticmethod
    def get_tweet_count(username: str, twitter_bearer_token: str) -> typing.Optional[int]:
        """
        Fetches the tweet count for a given Twitter username.
        Requires a Twitter bearer token for authentication.
        """
        twitter_data = gl.eq_principle.strict_eq(lambda: SocialMediaLib._fetch_twitter_metrics(username, twitter_bearer_token))
        if twitter_data and "data" in twitter_data and "public_metrics" in twitter_data["data"] and "tweet_count" in twitter_data["data"]["public_metrics"]:
            return int(twitter_data["data"]["public_metrics"]["tweet_count"])
        return None
