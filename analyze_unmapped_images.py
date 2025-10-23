#!/usr/bin/env python3
"""
Analyze unmapped images to see what's in their descriptions
"""

import csv
import json

def analyze_unmapped_images():
    """Analyze images without territorial mappings to understand their descriptions"""
    
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
    print("Analyzing their descriptions...\n")
    
    # Analyze descriptions
    description_patterns = {}
    
    for i, row in enumerate(unmapped_images[:10]):  # Show first 10 examples
        photo_name = row['Photo Name']
        description = row['Description']
        
        print(f"=== IMAGE {i+1}: {photo_name} ===")
        print(f"Description: {description}")
        
        # Check for common patterns
        if 'territorial acknowledgement' in description.lower():
            print("  + Contains 'territorial acknowledgement'")
        elif 'acknowledgement' in description.lower():
            print("  + Contains 'acknowledgement'")
        elif 'territory' in description.lower():
            print("  + Contains 'territory'")
        else:
            print("  - No obvious territory keywords found")
        
        print()
        
        # Categorize description patterns
        if 'credit:' in description.lower():
            if 'credit:' not in description_patterns:
                description_patterns['credit:'] = 0
            description_patterns['credit:'] += 1
        
        if 'donated' in description.lower():
            if 'donated' not in description_patterns:
                description_patterns['donated'] = 0
            description_patterns['donated'] += 1
        
        if 'licensed' in description.lower():
            if 'licensed' not in description_patterns:
                description_patterns['licensed'] = 0
            description_patterns['licensed'] += 1
    
    print(f"\nDESCRIPTION PATTERNS IN UNMAPPED IMAGES:")
    for pattern, count in description_patterns.items():
        print(f"  '{pattern}': {count} images")
    
    # Show a few more examples if there are more than 10
    if len(unmapped_images) > 10:
        print(f"\n... and {len(unmapped_images) - 10} more unmapped images")

if __name__ == "__main__":
    analyze_unmapped_images()
