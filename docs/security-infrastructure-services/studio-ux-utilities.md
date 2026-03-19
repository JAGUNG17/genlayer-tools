# Studio & UX Utilities

## Overview

The `StudioUXUtils` class provides a collection of helper functions designed to significantly improve the developer experience within the GenLayer Studio. These utilities focus on enhancing readability, debugging capabilities, and input validation, making the process of developing, testing, and maintaining Intelligent Contracts more efficient and less prone to errors.

## Features

- **Formatted JSON Output**: Presents complex JSON data in a human-readable, indented format, crucial for debugging and understanding contract states.
- **Event Logging**: Provides a standardized way to log custom events and data, offering better visibility into contract execution flow within the Studio logs.
- **Input Validation**: Offers a basic framework for validating contract inputs against defined schemas, helping to prevent common data-related errors.
- **Contract Status Retrieval**: (Placeholder) A utility to retrieve the current status of a deployed contract, aiding in monitoring and operational oversight.

## Usage

To leverage the `StudioUXUtils`, simply import the class into your Intelligent Contract. These are static methods, so you don't need to instantiate the class.

### Example: Formatting JSON Output and Logging Events

This example demonstrates how to use `format_json_output` for better readability and `log_event` for structured logging within your contract.

```python
# { "Depends": "py-genlayer:YOUR_GENLAYER_SDK_VERSION" }
from genlayer import *
from services.studio_ux_utils import StudioUXUtils

class DataProcessorContract(gl.Contract):
    processed_records: list[dict]

    def __init__(self):
        self.processed_records = []

    @gl.public.write
    def process_data(self, raw_input_json: str):
        """
        Processes raw JSON input, logs the event, and stores the formatted result.
        """
        try:
            input_data = json.loads(raw_input_json)
            
            # Simulate some processing
            processed_data = {
                "id": len(self.processed_records) + 1,
                "original_input": input_data,
                "timestamp": gl.timestamp(),
                "status": "completed"
            }
            self.processed_records.append(processed_data)

            # Log the event for visibility in GenLayer Studio
            StudioUXUtils.log_event("DataProcessed", processed_data)

            # Format output for better readability in Studio logs
            formatted_output = StudioUXUtils.format_json_output(processed_data)
            print(f"\n--- Processed Data ---\n{formatted_output}\n----------------------")

        except json.JSONDecodeError as e:
            StudioUXUtils.log_event("JSONParsingError", {"input": raw_input_json, "error": str(e)})
            raise Exception(f"Invalid JSON input: {e}")
        except Exception as e:
            StudioUXUtils.log_event("ProcessingError", {"input": raw_input_json, "error": str(e)})
            raise

    @gl.public.view
    def get_all_processed_records(self) -> list[dict]:
        """
        Returns all processed records.
        """
        return self.processed_records
```

### Example: Input Validation

While `StudioUXUtils.validate_input` provides a basic placeholder, in a real-world scenario, you would integrate a more robust schema validation library (e.g., `jsonschema`).

```python
# { "Depends": "py-genlayer:YOUR_GENLAYER_SDK_VERSION" }
from genlayer import *
from services.studio_ux_utils import StudioUXUtils
import json

class ValidatedInputContract(gl.Contract):
    last_valid_config: typing.Optional[dict]

    def __init__(self):
        self.last_valid_config = None

    @gl.public.write
    def set_configuration(self, config_json: str):
        """
        Sets a new configuration after validating its structure.
        """
        config_schema = {
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "version": {"type": "number"},
                "enabled": {"type": "boolean"}
            },
            "required": ["name", "version", "enabled"]
        }

        try:
            config_data = json.loads(config_json)
            
            # In a real scenario, use a library like jsonschema.validate(config_data, config_schema)
            if StudioUXUtils.validate_input(config_data, config_schema): # Placeholder validation
                self.last_valid_config = config_data
                StudioUXUtils.log_event("ConfigUpdateSuccess", config_data)
            else:
                StudioUXUtils.log_event("ConfigUpdateFailed", {"config": config_json, "reason": "Validation failed"})
                raise Exception("Configuration validation failed.")
        except json.JSONDecodeError as e:
            StudioUXUtils.log_event("JSONParsingError", {"input": config_json, "error": str(e)})
            raise Exception(f"Invalid JSON input for configuration: {e}")
        except Exception as e:
            StudioUXUtils.log_event("ConfigUpdateError", {"config": config_json, "error": str(e)})
            raise

    @gl.public.view
    def get_current_config(self) -> typing.Optional[dict]:
        """
        Returns the last successfully validated configuration.
        """
        return self.last_valid_config
```

## Best Practices for Studio & UX

- **Consistent Logging**: Use `StudioUXUtils.log_event` consistently throughout your contracts to provide clear, structured logs that are easy to parse and debug in the GenLayer Studio.
- **Descriptive Messages**: When logging or raising exceptions, provide clear and concise messages that help pinpoint the source of the issue.
- **Pre-validation**: Whenever possible, validate inputs before performing complex or resource-intensive operations to save gas and prevent unnecessary execution.
- **Modular Design**: Keep your utility functions focused and reusable. This promotes cleaner code and easier maintenance.

By incorporating these utilities and best practices, developers can significantly enhance the clarity, debuggability, and overall user experience when working with GenLayer Intelligent Contracts.
