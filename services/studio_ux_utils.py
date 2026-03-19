from genlayer import *
import typing
import json

class StudioUXUtils:
    """
    A collection of utilities to improve the Studio and UX for GenLayer developers.
    """
    
    @staticmethod
    def format_json_output(data: dict) -> str:
        """
        Formats JSON output for better readability in the Studio.
        """
        return json.dumps(data, indent=4)

    @staticmethod
    def log_event(event_name: str, data: dict):
        """
        Logs an event with a specific name and data for debugging in the Studio.
        """
        print(f"[{event_name}] {json.dumps(data)}")

    @staticmethod
    def validate_input(input_data: str, schema: dict) -> bool:
        """
        Validates input data against a simple schema for better error handling.
        """
        # Placeholder for schema validation logic
        # In a real-world scenario, use a library like jsonschema
        return True

    @staticmethod
    def get_contract_status(contract_address: Address) -> str:
        """
        Returns the current status of a contract for better visibility in the Studio.
        """
        # Placeholder for contract status retrieval logic
        return "Active"
