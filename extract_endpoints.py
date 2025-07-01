#!/usr/bin/env python3
"""
Extract all endpoints from the EnrichLayer client library.
"""

import re
import json
from pathlib import Path

def extract_endpoints_from_file(file_path):
    """Extract all endpoints from a library file."""
    with open(file_path, 'r') as f:
        content = f.read()
    
    endpoints = {}
    
    # Find all classes and their content
    class_pattern = r'class (_\w+):(.*?)(?=class|\Z)'
    classes = re.findall(class_pattern, content, re.DOTALL)
    
    for class_name, class_content in classes:
        if class_name == 'EnrichLayer':
            continue
            
        category = class_name.lstrip('_').lower()
        endpoints[category] = {}
        
        # Find all async methods in this class
        method_pattern = r'async def (\w+)\(\s*self,?\s*(.*?)\) -> .*?:'
        methods = re.findall(method_pattern, class_content, re.DOTALL)
        
        # Also find docstrings separately
        docstring_pattern = r'async def (\w+)\(.*?\):.*?"""(.*?)"""'
        docstrings = dict(re.findall(docstring_pattern, class_content, re.DOTALL))
        
        for method_name, params_str in methods:
            # Parse parameters
            params = []
            if params_str.strip():
                param_lines = [p.strip() for p in params_str.split(',')]
                for param in param_lines:
                    param = param.strip()
                    if param:
                        # Extract parameter name and type
                        if ':' in param:
                            parts = param.split(':')
                            param_name = parts[0].strip()
                            param_type = parts[1].split('=')[0].strip()
                            default_value = None
                            if '=' in parts[1]:
                                default_value = parts[1].split('=')[1].strip()
                            params.append({
                                'name': param_name,
                                'type': param_type,
                                'default': default_value
                            })
                        else:
                            param_name = param.split('=')[0].strip()
                            params.append({
                                'name': param_name,
                                'type': 'str',
                                'default': 'None' if '=' in param else None
                            })
            
            # Get docstring for this method
            docstring = docstrings.get(method_name, '')
            
            # Extract cost and description from docstring
            cost_match = re.search(r'Cost: (.*?) credit', docstring)
            cost = cost_match.group(1) if cost_match else 'Unknown'
            
            # Extract first line as description
            description_lines = docstring.strip().split('\n')
            description = description_lines[0].strip() if description_lines else ''
            
            endpoints[category][method_name] = {
                'description': description,
                'cost': cost,
                'parameters': params,
                'docstring': docstring.strip()
            }
    
    return endpoints

def main():
    # Extract from asyncio implementation
    asyncio_file = Path('/home/scythx/Documents/git/vertical-int/enrich-layer/enrichlayer-py/enrichlayer_client/asyncio/library.py')
    endpoints = extract_endpoints_from_file(asyncio_file)
    
    # Save to JSON file
    output_file = Path('/home/scythx/Documents/git/vertical-int/enrich-layer/enrichlayer-py/endpoints_analysis.json')
    with open(output_file, 'w') as f:
        json.dump(endpoints, f, indent=2)
    
    print(f"Endpoints extracted to: {output_file}")
    
    # Print summary
    total_endpoints = sum(len(methods) for methods in endpoints.values())
    print(f"\nSummary:")
    print(f"Total categories: {len(endpoints)}")
    print(f"Total endpoints: {total_endpoints}")
    
    for category, methods in endpoints.items():
        print(f"\n{category.upper()} ({len(methods)} endpoints):")
        for method_name, details in methods.items():
            param_count = len(details['parameters'])
            print(f"  - {method_name}() - {param_count} parameters - Cost: {details['cost']}")

if __name__ == '__main__':
    main()