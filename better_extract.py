#!/usr/bin/env python3
"""
Better extraction of all endpoints from the EnrichLayer client library.
"""

import re
import json
from pathlib import Path


def extract_endpoints_from_file(file_path):
    """Extract all endpoints from a library file."""
    with open(file_path, "r") as f:
        content = f.read()

    endpoints = {}

    # Split content by class definitions
    class_sections = re.split(r"(?=class )", content)

    for section in class_sections:
        if not section.strip():
            continue

        # Extract class name
        class_match = re.match(r"class (_?\w+)", section)
        if not class_match:
            continue

        class_name = class_match.group(1)
        if class_name == "EnrichLayer":
            continue

        if not class_name.startswith("_"):
            continue

        category = class_name.lstrip("_").lower()
        endpoints[category] = {}

        # Find all async methods
        method_matches = re.finditer(
            r"async def (\w+)\((.*?)\) -> .*?:", section, re.DOTALL
        )

        for match in method_matches:
            method_name = match.group(1)
            params_str = match.group(2)

            # Extract parameters
            params = []
            if params_str.strip():
                # Split by comma but handle nested structures
                param_parts = []
                current_param = ""
                paren_count = 0

                for char in params_str:
                    if char == "," and paren_count == 0:
                        param_parts.append(current_param.strip())
                        current_param = ""
                    else:
                        current_param += char
                        if char == "(":
                            paren_count += 1
                        elif char == ")":
                            paren_count -= 1

                if current_param.strip():
                    param_parts.append(current_param.strip())

                for param in param_parts:
                    param = param.strip()
                    if param and param != "self":
                        param_info = {"name": param, "type": "str", "default": None}

                        if ":" in param:
                            name_part, type_part = param.split(":", 1)
                            param_info["name"] = name_part.strip()

                            if "=" in type_part:
                                type_name, default_val = type_part.split("=", 1)
                                param_info["type"] = type_name.strip()
                                param_info["default"] = default_val.strip()
                            else:
                                param_info["type"] = type_part.strip()
                        elif "=" in param:
                            name_part, default_val = param.split("=", 1)
                            param_info["name"] = name_part.strip()
                            param_info["default"] = default_val.strip()
                        else:
                            param_info["name"] = param

                        params.append(param_info)

            # Extract docstring
            method_start = match.end()
            method_section = section[method_start:]

            docstring_match = re.search(r'"""(.*?)"""', method_section, re.DOTALL)
            docstring = docstring_match.group(1).strip() if docstring_match else ""

            # Extract cost
            cost_match = re.search(r"Cost: (.*?) credit", docstring)
            cost = cost_match.group(1) if cost_match else "Unknown"

            # Extract description (first line)
            description_lines = docstring.split("\n")
            description = description_lines[0].strip() if description_lines else ""

            endpoints[category][method_name] = {
                "description": description,
                "cost": cost,
                "parameters": params,
                "docstring": docstring,
            }

    return endpoints


def main():
    # Extract from asyncio implementation
    asyncio_file = Path(
        "/home/scythx/Documents/git/vertical-int/enrich-layer/enrichlayer-py/enrichlayer_client/asyncio/library.py"
    )
    endpoints = extract_endpoints_from_file(asyncio_file)

    # Save to JSON file
    output_file = Path(
        "/home/scythx/Documents/git/vertical-int/enrich-layer/enrichlayer-py/complete_endpoints_analysis.json"
    )
    with open(output_file, "w") as f:
        json.dump(endpoints, f, indent=2)

    print(f"Complete endpoints extracted to: {output_file}")

    # Print summary
    total_endpoints = sum(len(methods) for methods in endpoints.values())
    print("\nSummary:")
    print(f"Total categories: {len(endpoints)}")
    print(f"Total endpoints: {total_endpoints}")

    for category, methods in endpoints.items():
        print(f"\n{category.upper()} ({len(methods)} endpoints):")
        for method_name, details in methods.items():
            param_count = len(details["parameters"])
            print(
                f"  - {method_name}() - {param_count} parameters - Cost: {details['cost']}"
            )


if __name__ == "__main__":
    main()
