#!/usr/bin/env python3
"""
Extract territory data from image credits for images that don't already have territorial mappings
"""

import csv
import json
import re

def extract_territories_from_description(description):
    """Extract territory information from image descriptions with enhanced patterns"""
    territories = []
    
    # Enhanced patterns to match territorial acknowledgments
    patterns = [
        r'territorial acknowledgement to (?:the )?([^.]+?)(?:\.|,|$)',
        r'acknowledgement to (?:the )?([^.]+?)(?:\.|,|$)',
        r'on (?:the )?([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*(?:\s+Territory)?)\s+territory',
        r'([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*(?:\s+Territory)?)\s+territory',
    ]
    
    for pattern in patterns:
        matches = re.finditer(pattern, description, re.IGNORECASE)
        for match in matches:
            territory_text = match.group(1).strip()
            
            # Clean up the territory text
            territory_text = re.sub(r'^the\s+', '', territory_text, flags=re.IGNORECASE)
            territory_text = re.sub(r'\s*\.$', '', territory_text)
            
            # Handle special cases for Coast Salish Nations
            if 'coast salish nations of' in territory_text.lower():
                # Extract individual nations from "Coast Salish Nations of X, Y and Z"
                nations_text = re.sub(r'coast salish nations of\s*', '', territory_text, flags=re.IGNORECASE)
                # Split on common separators
                nations = re.split(r'[,\s]+and\s+|[,\s]+', nations_text)
                for nation in nations:
                    nation = nation.strip()
                    if nation and len(nation) > 2:
                        territories.append(nation)
            # Handle multiple territories separated by commas, "and", etc.
            elif ',' in territory_text or ' and ' in territory_text:
                # Split on common separators
                sub_territories = re.split(r'[,\s]+and\s+|[,\s]+', territory_text)
                for sub_territory in sub_territories:
                    sub_territory = sub_territory.strip()
                    if sub_territory and len(sub_territory) > 2:
                        territories.append(sub_territory)
            else:
                if territory_text and len(territory_text) > 2:
                    territories.append(territory_text)
    
    return list(set(territories))  # Remove duplicates

def normalize_territory_name(territory):
    """Normalize territory names for consistent matching"""
    # Common normalizations
    normalizations = {
        'coast salish': 'Coast Salish',
        'musqueam': 'Musqueam',
        'tsleil-waututh': 'Tsleil-Waututh',
        'squamish': 'Squamish',
        'secwepemc': 'Secwepemc',
        'tahltan': 'Tahltan',
        'mowachaht/muchalaht': 'Mowachaht/Muchalaht',
        'mowachaht-muchalaht': 'Mowachaht/Muchalaht',
        'klahoose': 'Klahoose',
        'nuchatlaht': 'Nuchatlaht',
        'gitxsan': 'Gitxsan',
        'nisga\'a': 'Nisga\'a',
        'taku river tlingit': 'Taku River Tlingit',
        'theklahoose': 'Klahoose',  # Handle concatenated names
        'muchalaht or nuchatlaht': 'Nuchatlaht',
    }
    
    territory_lower = territory.lower().strip()
    return normalizations.get(territory_lower, territory.strip())

def extract_missing_territories():
    """Extract territory data from credits for images without existing mappings"""
    
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
    
    # Find images without territorial mappings
    unmapped_images = []
    for row in csv_data:
        photo_name = row['Photo Name']
        if photo_name not in territorial_mapping:
            unmapped_images.append(row)
    
    print(f"\nFound {len(unmapped_images)} images without territorial mappings")
    print("Analyzing their credits for territory information...\n")
    
    new_mappings = {}
    territories_found = {}
    
    # Analyze each unmapped image
    for row in unmapped_images:
        photo_name = row['Photo Name']
        description = row['Description']
        
        # Extract territories from description
        territories = extract_territories_from_description(description)
        
        if territories:
            # Normalize territory names
            normalized_territories = [normalize_territory_name(t) for t in territories]
            
            # For now, take the first territory found (you can modify this logic)
            primary_territory = normalized_territories[0]
            
            new_mappings[photo_name] = {
                'first_nation': primary_territory,
                'full_acknowledgement': f"territorial acknowledgement to the {primary_territory}"
            }
            
            # Count territories found
            if primary_territory in territories_found:
                territories_found[primary_territory] += 1
            else:
                territories_found[primary_territory] = 1
            
            print(f"✓ {photo_name}: Found territory '{primary_territory}'")
            
            # Show the description excerpt
            desc_excerpt = description[:100] + "..." if len(description) > 100 else description
            print(f"  Credit: {desc_excerpt}")
            print()
    
    if new_mappings:
        # Add new mappings to existing mapping
        territorial_mapping.update(new_mappings)
        
        # Save updated mapping
        with open('corrected_territorial_mapping.json', 'w', encoding='utf-8') as f:
            json.dump(territorial_mapping, f, indent=2, ensure_ascii=False)
        
        print(f"\nSUMMARY:")
        print(f"  Added {len(new_mappings)} new territorial mappings")
        print(f"  Total mappings now: {len(territorial_mapping)}")
        
        print(f"\nTERRITORIES FOUND:")
        for territory, count in sorted(territories_found.items()):
            print(f"  {territory}: {count} new images")
    else:
        print("\nNo new territories found in unmapped images")

if __name__ == "__main__":
    extract_missing_territories()


