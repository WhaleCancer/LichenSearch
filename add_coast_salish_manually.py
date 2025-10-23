#!/usr/bin/env python3
"""
Manually add Coast Salish Nations territories for specific images
"""

import json

def add_coast_salish_manually():
    """Add Coast Salish Nations territories for specific images"""
    
    # Load existing territorial mapping
    try:
        with open('corrected_territorial_mapping.json', 'r', encoding='utf-8') as f:
            territorial_mapping = json.load(f)
        print(f"Loaded existing mapping with {len(territorial_mapping)} entries")
    except FileNotFoundError:
        print("ERROR: corrected_territorial_mapping.json not found")
        return
    
    # Add the specific image from the screenshot
    coast_salish_images = {
        'DSC1018': {
            'first_nation': 'Musqueam, Tsleil-Waututh, Squamish',
            'full_acknowledgement': 'territorial acknowledgement to the Coast Salish Nations of Musqueam, Tsleil-Waututh and Squamish'
        }
    }
    
    print("\nAdding Coast Salish Nations territories for specific images...\n")
    
    added_count = 0
    for photo_name, territory_info in coast_salish_images.items():
        territorial_mapping[photo_name] = territory_info
        added_count += 1
        print(f"+ Added {photo_name}: {territory_info['first_nation']}")
    
    # Save updated mapping
    with open('corrected_territorial_mapping.json', 'w', encoding='utf-8') as f:
        json.dump(territorial_mapping, f, indent=2, ensure_ascii=False)
    
    print(f"\nAdded {added_count} Coast Salish Nations territories")
    print(f"Total mappings now: {len(territorial_mapping)}")
    
    # Show current territories
    territories = set()
    for mapping in territorial_mapping.values():
        territories.add(mapping['first_nation'])
    
    print(f"\nCurrent territories in mapping:")
    for territory in sorted(territories):
        count = sum(1 for m in territorial_mapping.values() if m['first_nation'] == territory)
        print(f"  {territory}: {count} images")

if __name__ == "__main__":
    add_coast_salish_manually()
