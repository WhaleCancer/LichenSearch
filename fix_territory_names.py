#!/usr/bin/env python3
"""
Fix Territory Names Script
Corrects territory name inconsistencies found in the audit.
"""

import json

def fix_territory_names():
    """Fix territory name inconsistencies"""
    
    # Load the enhanced mapping
    with open('enhanced_territorial_mapping.json', 'r', encoding='utf-8') as f:
        mapping = json.load(f)
    
    # Territory name corrections
    corrections = {
        'theKlahoose': 'Klahoose',
        'Muchalaht or Nuchatlaht': 'Nuchatlaht',  # Assuming Nuchatlaht is the primary
    }
    
    # Apply corrections
    corrected_count = 0
    for photo_name, data in mapping.items():
        original_name = data['first_nation']
        if original_name in corrections:
            data['first_nation'] = corrections[original_name]
            corrected_count += 1
            print(f"Corrected {photo_name}: {original_name} -> {corrections[original_name]}")
    
    # Save corrected mapping
    with open('corrected_territorial_mapping.json', 'w', encoding='utf-8') as f:
        json.dump(mapping, f, indent=2, ensure_ascii=False)
    
    print(f"\nCorrected {corrected_count} territory names")
    print("Saved to corrected_territorial_mapping.json")
    
    # Count territories
    territories = {}
    for data in mapping.values():
        territory = data['first_nation']
        territories[territory] = territories.get(territory, 0) + 1
    
    print(f"\nFinal territory counts:")
    for territory, count in sorted(territories.items()):
        print(f"  {territory}: {count} images")
    
    return mapping

if __name__ == "__main__":
    fix_territory_names()

