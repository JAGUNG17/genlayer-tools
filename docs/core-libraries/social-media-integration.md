# Social Media Integration

## Overview

The `SocialMediaLib` provides functionalities for GenLayer Intelligent Contracts to interact with social media platforms, enabling contracts to fetch public profile information and metrics. Currently, it supports GitHub profile retrieval and includes a framework for Twitter (X) integration, allowing contracts to react to or utilize data from these platforms.

## Features

- **GitHub Profile Data**: Easily fetch public profile information for any GitHub user.
- **Twitter (X) Metrics**: Framework for retrieving user metrics like tweet counts (requires API key/bearer token).
- **Error Handling**: Includes mechanisms to handle API errors and invalid responses gracefully.
- **Equivalence Principle**: Ensures consistent data retrieval across validators for social media data.

## Usage

To use the `SocialMediaLib`, import it into your Intelligent Contract and call the relevant static methods. Ensure your contract declares the `py-genlayer` dependency.

### Example: Fetching GitHub Profile Information

This example demonstrates how to fetch public profile data for a GitHub user.

```python
# { "Depends": "py-genlayer:YOUR_GENLAYER_SDK_VERSION" }
from genlayer import *
from libraries.social_media import SocialMediaLib
from services.studio_ux_utils import StudioUXUtils

class GitHubProfileContract(gl.Contract):
    github_username: str
    profile_data: typing.Optional[dict]
    last_updated: int

    def __init__(self):
        self.github_username = ""
        self.profile_data = None
        self.last_updated = 0

    @gl.public.write
    def update_github_profile(self, username: str):
        """
        Fetches GitHub profile information for a given username and updates the contract state.
        """
        try:
            profile = SocialMediaLib.get_github_profile(username)
            if profile is not None:
                self.github_username = username
                self.profile_data = profile
                self.last_updated = gl.timestamp()
                StudioUXUtils.log_event("GitHubProfileUpdateSuccess", {
                    "username": username,
                    "followers": profile.get("followers"),
                    "public_repos": profile.get("public_repos"),
                    "timestamp": self.last_updated
                })
            else:
                StudioUXUtils.log_event("GitHubProfileUpdateFailed", {"username": username, "reason": "Could not retrieve profile"})
                raise Exception(f"Failed to retrieve GitHub profile for {username}")
        except Exception as e:
            StudioUXUtils.log_event("GitHubProfileUpdateError", {"username": username, "error": str(e)})
            raise

    @gl.public.view
    def get_last_github_profile(self) -> typing.Optional[dict]:
        """
        Returns the last successfully fetched GitHub profile data.
        """
        return self.profile_data
```

### Example: Fetching Twitter (X) Tweet Count

This example demonstrates how to fetch the tweet count for a Twitter (X) user. This requires a Twitter (X) Bearer Token, which should be managed securely.

```python
# { "Depends": "py-genlayer:YOUR_GENLAYER_SDK_VERSION" }
from genlayer import *
from libraries.social_media import SocialMediaLib
from services.studio_ux_utils import StudioUXUtils
from services.secure_api_key_manager import SecureAPIKeyManager

class TwitterMetricsContract(gl.Contract):
    twitter_username: str
    tweet_count: typing.Optional[int]
    last_updated: int

    def __init__(self):
        self.twitter_username = ""
        self.tweet_count = None
        self.last_updated = 0

    @gl.public.write
    def update_twitter_metrics(self, username: str, api_key_manager_address: Address):
        """
        Fetches Twitter (X) metrics for a given username and updates the contract state.
        Retrieves Twitter Bearer Token from SecureAPIKeyManager.
        """
        try:
            # Retrieve API key securely
            api_key_manager = gl.Contract.at(SecureAPIKeyManager, api_key_manager_address)
            twitter_bearer_token = api_key_manager.get_api_key_for_proxy("TwitterBearerToken")

            count = SocialMediaLib.get_tweet_count(username, twitter_bearer_token)
            if count is not None:
                self.twitter_username = username
                self.tweet_count = count
                self.last_updated = gl.timestamp()
                StudioUXUtils.log_event("TwitterMetricsUpdateSuccess", {
                    "username": username,
                    "tweet_count": count,
                    "timestamp": self.last_updated
                })
            else:
                StudioUXUtils.log_event("TwitterMetricsUpdateFailed", {"username": username, "reason": "Could not retrieve tweet count"})
                raise Exception(f"Failed to retrieve Twitter metrics for {username}")
        except Exception as e:
            StudioUXUtils.log_event("TwitterMetricsUpdateError", {"username": username, "error": str(e)})
            raise

    @gl.public.view
    def get_last_tweet_count(self) -> typing.Optional[int]:
        """
        Returns the last successfully fetched tweet count.
        """
        return self.tweet_count
```

## Error Handling and Robustness

- **API Specific Errors**: Both `_fetch_github_profile` and `_fetch_twitter_metrics` methods include checks for HTTP status codes and print detailed error messages in case of failure. This helps in diagnosing issues related to API limits, invalid credentials, or network problems.
- **`None` Return on Failure**: All `get_...` methods return `None` if data retrieval or parsing fails, allowing the calling contract to handle these scenarios gracefully.
- **Contract-Level Exception Handling**: It is crucial for Intelligent Contracts to implement `try-except` blocks to catch exceptions raised by the `SocialMediaLib` and handle them appropriately (e.g., revert, log, or retry).

## Security Considerations

- **API Key Management**: For Twitter (X) integration, a Bearer Token is required. **Never embed API keys or tokens directly in your contract code.** Always use the `SecureAPIKeyManager` service to store encrypted credentials and retrieve them via an authorized proxy contract or trusted oracle service at runtime. This prevents exposure of sensitive credentials.
- **Data Integrity**: The `gl.eq_principle.strict_eq` is used for all external data fetches to ensure that all validators agree on the exact social media data, maintaining the integrity of your contract's state.
- **Rate Limiting**: Be mindful of API rate limits imposed by social media platforms. Implement exponential backoff or other rate-limiting strategies in your external services or oracle interactions to avoid being blocked.
- **Privacy**: When fetching social media data, always respect user privacy and platform terms of service. Only retrieve publicly available information and avoid collecting sensitive data without explicit consent.
