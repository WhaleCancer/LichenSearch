#!/usr/bin/env python3
"""
Thorough search for any Coast Salish related terms in image descriptions
"""

import csv
import re

def thorough_coast_salish_search():
    """Search for any Coast Salish related terms with variations"""
    
    # Load CSV data
    try:
        with open('TempShopify/output_dsc0001-9999.csv', 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            csv_data = list(reader)
        print(f"Loaded {len(csv_data)} images from CSV")
    except FileNotFoundError:
        print("ERROR: CSV file not found")
        return
    
    # Search terms and variations
    search_terms = [
        'musqueam', 'tsleil', 'waututh', 'squamish', 'coast salish',
        'salish', 'christopher brown', 'brown', 'nations of',
        'territorial acknowledgement', 'acknowledgement'
    ]
    
    print("\nSearching for Coast Salish related terms...\n")
    
    found_matches = []
    
    for row in csv_data:
        photo_name = row['Photo Name']
        description = row['Description']
        description_lower = description.lower()
        
        matches_in_desc = []
        for term in search_terms:
            if term in description_lower:
                matches_in_desc.append(term)
        
        if matches_in_desc:
            found_matches.append({
                'photo_name': photo_name,
                'matches': matches_in_desc,
                'description': description
            })
    
    print(f"Found {len(found_matches)} images with Coast Salish related terms:\n")
    
    for i, match in enumerate(found_matches, 1):
        print(f"{i}. {match['photo_name']}")
        print(f"   Matches: {', '.join(match['matches'])}")
        print(f"   Description: {match['description']}")
        print()
    
    # Also search for any description that might contain multiple territories
    print("\nSearching for descriptions with multiple territory mentions...\n")
    
    multi_territory_matches = []
    for row in csv_data:
        photo_name = row['Photo Name']
        description = row['Description']
        
        # Count territory-related words
        territory_words = ['territory', 'territorial', 'acknowledgement', 'acknowledgment', 'nation', 'nations']
        count = sum(1 for word in territory_words if word in description.lower())
        
        if count > 1:  # Multiple territory-related words
            multi_territory_matches.append({
                'photo_name': photo_name,
                'count': count,
                'description': description
            })
    
    print(f"Found {len(multi_territory_matches)} images with multiple territory-related terms:\n")
    
    for i, match in enumerate(multi_territory_matches[:10], 1):  # Show first 10
        print(f"{i}. {match['photo_name']} ({match['count']} territory terms)")
        print(f"   Description: {match['description']}")
        print()

if __name__ == "__main__":
    thorough_coast_salish_search()


