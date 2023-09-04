import time
import json
from typing import List, Dict
from urllib.parse import quote

from url_processor import URLProcessor

def sort_keys_by_value(json_obj):
    sorted_json_obj = {}
    for outer_key, inner_dict in json_obj.items():
        # Sort the keys of the inner dictionary based on their numerical value
        sorted_keys = sorted(inner_dict, key=lambda k: inner_dict[k], reverse=True)
        
        # Create a new dictionary with the sorted keys and their respective values
        sorted_inner_dict = {k: inner_dict[k] for k in sorted_keys}
        
        # Add the sorted inner dictionary to the result dictionary using the original outer key
        sorted_json_obj[outer_key] = sorted_inner_dict

    return sorted_json_obj

def main():
    band_pages = "band_pages.txt"
    output_file = "output.json"

    url_processor = URLProcessor(band_pages)
    results = url_processor.process_urls()
    sorted = sort_keys_by_value(results)
    with open(output_file, "w") as f:
        json.dump(sorted, f, indent=4)

if __name__ == "__main__":
    main()