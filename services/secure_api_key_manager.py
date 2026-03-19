from genlayer import *
import typing
import json

class SecureAPIKeyManager(gl.Contract):
    """
    A service for GenLayer Intelligent Contracts to manage API keys securely.
    This contract allows the owner to store encrypted API keys and 
    provides a mechanism for authorized contracts to use them.
    """
    
    # Mapping of service name to encrypted API key
    # In a real-world scenario, keys would be encrypted with a public key 
    # and decrypted only within the validator's secure execution environment.
    api_keys: dict[str, str]
    owner: Address

    def __init__(self):
        self.api_keys = {}
        self.owner = gl.message.sender

    @gl.public.write
    def set_api_key(self, service: str, encrypted_key: str):
        """
        Allows the owner to set an encrypted API key for a service.
        """
        if gl.message.sender != self.owner:
            raise Exception("Only the owner can set API keys.")
        self.api_keys[service] = encrypted_key

    @gl.public.view
    def get_api_key(self, service: str) -> str:
        """
        Returns the encrypted API key for a service.
        Authorized contracts can then use this key in their web requests.
        """
        if service not in self.api_keys:
            raise Exception(f"API key for {service} not found.")
        return self.api_keys[service]

    @gl.public.write
    def remove_api_key(self, service: str):
        """
        Allows the owner to remove an API key.
        """
        if gl.message.sender != self.owner:
            raise Exception("Only the owner can remove API keys.")
        if service in self.api_keys:
            del self.api_keys[service]
