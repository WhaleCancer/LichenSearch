#!/usr/bin/env python3
"""
Remove the incorrectly added Coast Salish territories from sample images
"""

import json

def undo_coast_salish_additions():
    """Remove the Coast Salish territories that were incorrectly added"""
    
    # Load existing territorial mapping
    try:
        with open('corrected_territorial_mapping.json', 'r', encoding='utf-8') as f:
            territorial_mapping = json.load(f)
        print(f"Loaded existing mapping with {len(territorial_mapping)} entries")
    except FileNotFoundError:
        print("ERROR: corrected_territorial_mapping.json not found")
        return
    
    # Images that were incorrectly given Coast Salish territories
    incorrect_images = ['DSC1487', 'DSC1515', 'Photo Name']
    
    removed_count = 0
    for image_name in incorrect_images:
        if image_name in territorial_mapping:
            territory = territorial_mapping[image_name]['first_nation']
            del territorial_mapping[image_name]
            removed_count += 1
            print(f"Removed {territory} territory from {image_name}")
    
    # Save corrected mapping
    with open('corrected_territorial_mapping.json', 'w', encoding='utf-8') as f:
        json.dump(territorial_mapping, f, indent=2, ensure_ascii=False)
    
    print(f"\nRemoved {removed_count} incorrect Coast Salish territory mappings")
    print(f"Total mappings now: {len(territorial_mapping)}")

if __name__ == "__main__":
    undo_coast_salish_additions()


