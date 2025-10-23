#!/usr/bin/env python3
"""
Search for Coast Salish Nations in CSV data
"""

import csv
import re

def search_coast_salish():
    """Search for Coast Salish Nations and related terms"""
    
    try:
        with open('TempShopify/output_dsc0001-9999.csv', 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            csv_data = list(reader)
    except FileNotFoundError:
        print("ERROR: CSV file not found.")
        return
    
    # Search terms
    search_terms = [
        'coast salish',
        'musqueam',
        'tsleil-waututh',
        'squamish',
        'christopher brown',
        'brown',
        'nations of',
        'territorial acknowledgement'
    ]
    
    found_matches = []
    
    for row in csv_data:
        photo_name = row['Photo Name']
        description = row['Description']
        
        for term in search_terms:
            if term.lower() in description.lower():
                found_matches.append({
                    'photo_name': photo_name,
                    'term': term,
                    'description': description
                })
                break  # Only add once per photo
    
    print(f"Found {len(found_matches)} matches:")
    print("=" * 50)
    
    for match in found_matches:
        print(f"Photo: {match['photo_name']}")
        print(f"Term: {match['term']}")
        print(f"Description: {match['description'][:200]}...")
        print("-" * 30)

if __name__ == "__main__":
    search_coast_salish()


