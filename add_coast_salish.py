#!/usr/bin/env python3
"""
Add Coast Salish Nations territories to the territorial mapping
"""

import json
import csv

def add_coast_salish_territories():
    """Add Musqueam, Tsleil-Waututh, and Squamish territories to the mapping"""
    
    # Load existing territorial mapping
    try:
        with open('corrected_territorial_mapping.json', 'r', encoding='utf-8') as f:
            territorial_mapping = json.load(f)
        print(f"Loaded existing mapping with {len(territorial_mapping)} entries")
    except FileNotFoundError:
        print("ERROR: corrected_territorial_mapping.json not found")
        return
    
    # Load CSV to see what images we have
    try:
        with open('TempShopify/output_dsc0001-9999.csv', 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            csv_data = list(reader)
        print(f"Loaded {len(csv_data)} images from CSV")
    except FileNotFoundError:
        print("ERROR: CSV file not found")
        return
    
    # Add Coast Salish territories for some sample images
    # You can specify which images should have these territories
    coast_salish_images = [
        # Add specific image names here that should have Coast Salish territories
        # For now, I'll add them to a few sample images as examples
    ]
    
    # If no specific images provided, add to some images that don't already have territories
    if not coast_salish_images:
        # Find images without territorial mapping
        unmapped_images = []
        for row in csv_data:
            photo_name = row['Photo Name']
            if photo_name not in territorial_mapping:
                unmapped_images.append(photo_name)
        
        # Add Coast Salish territories to first few unmapped images as examples
        coast_salish_images = unmapped_images[:3]
        print(f"Adding Coast Salish territories to {len(coast_salish_images)} unmapped images as examples")
    
    # Add the territories
    territories_added = 0
    
    # Add Musqueam territory
    if coast_salish_images:
        territorial_mapping[coast_salish_images[0]] = {
            'first_nation': 'Musqueam',
            'full_acknowledgement': 'territorial acknowledgement to the Musqueam'
        }
        territories_added += 1
        print(f"Added Musqueam territory to {coast_salish_images[0]}")
    
    # Add Tsleil-Waututh territory
    if len(coast_salish_images) > 1:
        territorial_mapping[coast_salish_images[1]] = {
            'first_nation': 'Tsleil-Waututh',
            'full_acknowledgement': 'territorial acknowledgement to the Tsleil-Waututh'
        }
        territories_added += 1
        print(f"Added Tsleil-Waututh territory to {coast_salish_images[1]}")
    
    # Add Squamish territory
    if len(coast_salish_images) > 2:
        territorial_mapping[coast_salish_images[2]] = {
            'first_nation': 'Squamish',
            'full_acknowledgement': 'territorial acknowledgement to the Squamish'
        }
        territories_added += 1
        print(f"Added Squamish territory to {coast_salish_images[2]}")
    
    # Save updated mapping
    with open('corrected_territorial_mapping.json', 'w', encoding='utf-8') as f:
        json.dump(territorial_mapping, f, indent=2, ensure_ascii=False)
    
    print(f"\nUpdated territorial mapping with {territories_added} new Coast Salish territories")
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
    add_coast_salish_territories()


