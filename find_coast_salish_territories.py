#!/usr/bin/env python3
"""
Find and extract Musqueam, Tsleil-Waututh, and Squamish territories from image descriptions
"""

import csv
import json
import re

def extract_coast_salish_territories(description):
    """Extract Musqueam, Tsleil-Waututh, and Squamish from descriptions"""
    territories = []
    description_lower = description.lower()
    
    # Check for each territory specifically
    if 'musqueam' in description_lower:
        territories.append('Musqueam')
    
    if 'tsleil-waututh' in description_lower:
        territories.append('Tsleil-Waututh')
    
    if 'squamish' in description_lower:
        territories.append('Squamish')
    
    # Also check for "Coast Salish Nations of" pattern and extract individual nations
    coast_salish_pattern = r'coast salish nations of ([^.]+)'
    match = re.search(coast_salish_pattern, description_lower)
    if match:
        nations_text = match.group(1)
        # Split on commas and "and"
        nations = re.split(r'[,\s]+and\s+|[,\s]+', nations_text)
        for nation in nations:
            nation = nation.strip()
            if nation and nation in ['musqueam', 'tsleil-waututh', 'squamish']:
                territories.append(nation.title())
    
    return list(set(territories))  # Remove duplicates

def find_coast_salish_territories():
    """Find all images that mention Musqueam, Tsleil-Waututh, or Squamish"""
    
    # Load existing territorial mapping
    try:
        with open('corrected_territorial_mapping.json', 'r', encoding='utf-8') as f:
            territorial_mapping = json.load(f)
        print(f"Loaded existing mapping with {len(territorial_mapping)} entries")
    except FileNotFoundError:
        print("ERROR: corrected_territorial_mapping.json not found")
        return
    
    # Load CSV data
    try:
        with open('TempShopify/output_dsc0001-9999.csv', 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            csv_data = list(reader)
        print(f"Loaded {len(csv_data)} images from CSV")
    except FileNotFoundError:
        print("ERROR: CSV file not found")
        return
    
    # Search through all images
    coast_salish_images = []
    updated_mappings = {}
    
    print("\nSearching for Coast Salish Nations in all image descriptions...\n")
    
    for row in csv_data:
        photo_name = row['Photo Name']
        description = row['Description']
        
        # Extract Coast Salish territories from description
        territories = extract_coast_salish_territories(description)
        
        if territories:
            coast_salish_images.append({
                'photo_name': photo_name,
                'territories': territories,
                'description': description
            })
            
            # Update or add territorial mapping
            if len(territories) == 1:
                # Single territory
                territorial_mapping[photo_name] = {
                    'first_nation': territories[0],
                    'full_acknowledgement': f"territorial acknowledgement to the {territories[0]}"
                }
            else:
                # Multiple territories - store as comma-separated
                territories_str = ', '.join(territories)
                territorial_mapping[photo_name] = {
                    'first_nation': territories_str,
                    'full_acknowledgement': f"territorial acknowledgement to the {territories_str}"
                }
            
            updated_mappings[photo_name] = territories
    
    # Display results
    print(f"FOUND {len(coast_salish_images)} IMAGES WITH COAST SALISH NATIONS:\n")
    
    for i, img in enumerate(coast_salish_images, 1):
        print(f"{i}. {img['photo_name']}")
        print(f"   Territories: {', '.join(img['territories'])}")
        
        # Show relevant part of description
        desc = img['description']
        if len(desc) > 150:
            desc = desc[:150] + "..."
        print(f"   Description: {desc}")
        print()
    
    # Show summary by territory
    territory_counts = {}
    for img in coast_salish_images:
        for territory in img['territories']:
            territory_counts[territory] = territory_counts.get(territory, 0) + 1
    
    print("TERRITORY SUMMARY:")
    for territory, count in sorted(territory_counts.items()):
        print(f"  {territory}: {count} images")
    
    # Save updated mapping
    if updated_mappings:
        with open('corrected_territorial_mapping.json', 'w', encoding='utf-8') as f:
            json.dump(territorial_mapping, f, indent=2, ensure_ascii=False)
        
        print(f"\nUpdated territorial mapping with {len(updated_mappings)} Coast Salish territories")
        print(f"Total mappings now: {len(territorial_mapping)}")
    else:
        print("\nNo Coast Salish territories found in any image descriptions")

if __name__ == "__main__":
    find_coast_salish_territories()


