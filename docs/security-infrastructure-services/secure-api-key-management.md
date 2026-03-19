# Secure API Key Management

## Overview

The `SecureAPIKeyManager` is a critical Intelligent Contract designed to address the challenge of securely managing sensitive API keys within the GenLayer ecosystem. It implements a robust proxy pattern, allowing contract owners to store encrypted API keys on-chain while ensuring that only authorized proxy contracts can retrieve them for use in external API calls. This approach significantly enhances security by isolating sensitive credentials from direct exposure within application-level contracts.

## Architecture and Security Model

### Key Principles

1.  **Separation of Concerns**: API keys are not stored directly within the application logic of Intelligent Contracts. Instead, a dedicated `SecureAPIKeyManager` contract handles their storage and access control.
2.  **Encryption at Rest**: API keys are stored in an encrypted format on-chain. The actual decryption process is intended to occur in a trusted off-chain environment (e.g., a secure oracle service or a Trusted Execution Environment (TEE)) that interacts with the GenLayer network.
3.  **Access Control via Proxy Pattern**: Access to encrypted API keys is restricted. Only contracts explicitly authorized by the `SecureAPIKeyManager`'s owner (via the `authorize_proxy` function) can request keys. This introduces an additional layer of security and flexibility.
4.  **Owner-Controlled Management**: The deployment and management (setting, removing, authorizing proxies) of API keys are strictly controlled by the contract owner, ensuring centralized oversight of sensitive credentials.

### How it Works

1.  **Deployment**: The `SecureAPIKeyManager` contract is deployed by an owner.
2.  **Key Storage**: The owner calls `set_api_key` to store an *encrypted* API key for a specific service (e.g., 
"OpenWeatherMap", "AlphaVantage").
3.  **Proxy Authorization**: The owner authorizes specific proxy contracts (e.g., `APIKeyProxy` instances) that are allowed to request API keys.
4.  **Key Request**: An application Intelligent Contract that needs an API key interacts with an `APIKeyProxy` contract. The `APIKeyProxy` then calls `get_api_key_for_proxy` on the `SecureAPIKeyManager`.
5.  **Access Check**: The `SecureAPIKeyManager` verifies if the calling `APIKeyProxy` is authorized. If so, it returns the *encrypted* API key.
6.  **Off-chain Decryption/Usage**: The `APIKeyProxy` (or an associated off-chain service) then passes this encrypted key to a trusted oracle or TEE for decryption and actual use in making external API calls.

## Contract Details

### `SecureAPIKeyManager` Contract

```python
from genlayer import *
import typing
import json

class SecureAPIKeyManager(gl.Contract):
    api_keys: dict[str, str]
    owner: Address
    authorized_proxies: dict[Address, bool]

    def __init__(self):
        self.api_keys = {}
        self.owner = gl.message.sender
        self.authorized_proxies = {}

    @gl.public.write
    def set_api_key(self, service: str, encrypted_key: str):
        if gl.message.sender != self.owner:
            raise Exception("Only the owner can set API keys.")
        self.api_keys[service] = encrypted_key
        print(f"API key for service {service} set by owner {self.owner}")

    @gl.public.write
    def remove_api_key(self, service: str):
        if gl.message.sender != self.owner:
            raise Exception("Only the owner can remove API keys.")
        if service in self.api_keys:
            del self.api_keys[service]
            print(f"API key for service {service} removed by owner {self.owner}")

    @gl.public.write
    def authorize_proxy(self, proxy_address: Address, is_authorized: bool):
        if gl.message.sender != self.owner:
            raise Exception("Only the owner can authorize proxies.")
        self.authorized_proxies[proxy_address] = is_authorized
        print(f"Proxy {proxy_address} authorization set to {is_authorized} by owner {self.owner}")

    @gl.public.view
    def get_api_key_for_proxy(self, service: str) -> str:
        if gl.message.sender not in self.authorized_proxies or not self.authorized_proxies[gl.message.sender]:
            raise Exception("Caller is not an authorized proxy contract.")
        if service not in self.api_keys:
            raise Exception(f"API key for {service} not found.")
        print(f"API key for service {service} requested by authorized proxy {gl.message.sender}")
        return self.api_keys[service]
```

### `APIKeyProxy` Contract

This is an example of a proxy contract that would be authorized by the `SecureAPIKeyManager` to retrieve encrypted API keys. Other application-level Intelligent Contracts would then interact with this `APIKeyProxy`.

```python
from genlayer import *
import typing
import json

# Assuming SecureAPIKeyManager is imported or available
# from services.secure_api_key_manager import SecureAPIKeyManager # This would be needed in a real setup

class APIKeyProxy(gl.Contract):
    api_key_manager_address: Address

    def __init__(self, manager_address: Address):
        self.api_key_manager_address = manager_address

    @gl.public.view
    def request_api_key(self, service: str) -> str:
        manager = gl.Contract.at(SecureAPIKeyManager, self.api_key_manager_address)
        encrypted_key = manager.get_api_key_for_proxy(service)
        print(f"API key for service {service} retrieved via proxy {gl.message.sender}")
        return encrypted_key
```

## Usage Flow

1.  **Deploy `SecureAPIKeyManager`**: Deploy an instance of `SecureAPIKeyManager` to the GenLayer network. The deployer becomes the owner.
2.  **Deploy `APIKeyProxy`**: Deploy one or more instances of `APIKeyProxy`, providing the address of the deployed `SecureAPIKeyManager` during initialization.
3.  **Owner Sets API Keys**: The owner of `SecureAPIKeyManager` calls `set_api_key("ServiceName", "ENCRYPTED_KEY_STRING")` to store encrypted API keys.
4.  **Owner Authorizes Proxies**: The owner calls `authorize_proxy(proxy_contract_address, True)` for each `APIKeyProxy` instance that should have access.
5.  **Application Contract Requests Key**: An application Intelligent Contract calls `APIKeyProxy.request_api_key("ServiceName")`. The `APIKeyProxy` then retrieves the encrypted key from the `SecureAPIKeyManager`.
6.  **Off-chain Processing**: The encrypted key is then passed to an off-chain oracle or TEE for decryption and use in external API calls. The result of the external API call is then returned to the Intelligent Contract, potentially via another transaction or a verifiable computation.

## Best Practices for API Key Encryption

- **Asymmetric Encryption**: Use asymmetric encryption (e.g., RSA) where the public key is known to the contract owner for encryption, and the private key is held securely by the off-chain oracle/TEE for decryption.
- **Key Rotation**: Implement a strategy for regularly rotating API keys to minimize the impact of a potential compromise.
- **Least Privilege**: Ensure that the API keys themselves have only the necessary permissions for their intended use.
- **Auditing**: Leverage GenLayer's logging capabilities to audit access requests to the `SecureAPIKeyManager`.

This secure API key management pattern provides a robust foundation for building Intelligent Contracts that interact with external services while maintaining a high level of security for sensitive credentials.
