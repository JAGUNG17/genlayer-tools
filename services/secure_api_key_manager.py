from genlayer import *
import typing
import json

class SecureAPIKeyManager(gl.Contract):
    """
    A service for GenLayer Intelligent Contracts to manage API keys securely.
    This contract allows the owner to store encrypted API keys and 
    provides a mechanism for authorized contracts to use them via a proxy.
    
    API keys are stored encrypted. The actual decryption and usage should occur
    in a trusted off-chain environment or a secure oracle service that interacts
    with this contract.
    """
    
    api_keys: dict[str, str]  # Mapping of service name to encrypted API key
    owner: Address
    authorized_proxies: dict[Address, bool] # Mapping of authorized proxy contract addresses

    def __init__(self):
        self.api_keys = {}
        self.owner = gl.message.sender
        self.authorized_proxies = {}

    @gl.public.write
    def set_api_key(self, service: str, encrypted_key: str):
        """
        Allows the owner to set an encrypted API key for a service.
        Only the owner can call this function.
        """
        if gl.message.sender != self.owner:
            raise Exception("Only the owner can set API keys.")
        self.api_keys[service] = encrypted_key
        print(f"API key for service {service} set by owner {self.owner}")

    @gl.public.write
    def remove_api_key(self, service: str):
        """
        Allows the owner to remove an API key.
        Only the owner can call this function.
        """
        if gl.message.sender != self.owner:
            raise Exception("Only the owner can remove API keys.")
        if service in self.api_keys:
            del self.api_keys[service]
            print(f"API key for service {service} removed by owner {self.owner}")

    @gl.public.write
    def authorize_proxy(self, proxy_address: Address, is_authorized: bool):
        """
        Allows the owner to authorize or de-authorize a proxy contract.
        Only authorized proxy contracts can request API keys.
        """
        if gl.message.sender != self.owner:
            raise Exception("Only the owner can authorize proxies.")
        self.authorized_proxies[proxy_address] = is_authorized
        print(f"Proxy {proxy_address} authorization set to {is_authorized} by owner {self.owner}")

    @gl.public.view
    def get_api_key_for_proxy(self, service: str) -> str:
        """
        Returns the encrypted API key for a service if the caller is an authorized proxy.
        This method is intended to be called by a trusted proxy contract.
        """
        if gl.message.sender not in self.authorized_proxies or not self.authorized_proxies[gl.message.sender]:
            raise Exception("Caller is not an authorized proxy contract.")
        if service not in self.api_keys:
            raise Exception(f"API key for {service} not found.")
        print(f"API key for service {service} requested by authorized proxy {gl.message.sender}")
        return self.api_keys[service]


class APIKeyProxy(gl.Contract):
    """
    A proxy contract that requests API keys from the SecureAPIKeyManager.
    This contract acts as an intermediary, allowing other contracts to request
    API keys without directly interacting with the SecureAPIKeyManager.
    """
    api_key_manager_address: Address

    def __init__(self, manager_address: Address):
        self.api_key_manager_address = manager_address

    @gl.public.view
    def request_api_key(self, service: str) -> str:
        """
        Requests an encrypted API key for a given service from the SecureAPIKeyManager.
        This method can be called by other Intelligent Contracts.
        """
        manager = gl.Contract.at(SecureAPIKeyManager, self.api_key_manager_address)
        # The manager will check if this proxy contract is authorized
        encrypted_key = manager.get_api_key_for_proxy(service)
        print(f"API key for service {service} retrieved via proxy {gl.message.sender}")
        return encrypted_key
