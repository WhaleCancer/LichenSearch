import csv
import json
import re

def extract_territorial_data():
    """Extract territorial data from CSV and create mapping"""
    territorial_mapping = {}
    
    with open('TempShopify/output_dsc0001-9999.csv', 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        
        for row in reader:
            photo_name = row['Photo Name']
            description = row['Description']
            
            # Extract First Nation from territorial acknowledgement
            territory_match = re.search(r'territorial acknowledgement to the ([^.]+)', description, re.IGNORECASE)
            
            if territory_match:
                first_nation = territory_match.group(1).strip()
                # Clean up formatting issues (remove "the" if it appears twice)
                first_nation = first_nation.replace('the', '').strip()
                # Fix spacing issues like "theKlahoose" -> "Klahoose"
                first_nation = re.sub(r'^the', '', first_nation, flags=re.IGNORECASE).strip()
                
                territorial_mapping[photo_name] = {
                    'first_nation': first_nation,
                    'full_acknowledgement': territory_match.group(0)
                }
    
    # Save the mapping
    with open('territorial_mapping.json', 'w', encoding='utf-8') as f:
        json.dump(territorial_mapping, f, indent=2)
    
    print(f"Extracted territorial data for {len(territorial_mapping)} images")
    
    # Print summary of territories found
    territories = {}
    for mapping in territorial_mapping.values():
        territory = mapping['first_nation']
        territories[territory] = territories.get(territory, 0) + 1
    
    print("\nTerritories found:")
    for territory, count in sorted(territories.items()):
        print(f"  {territory}: {count} images")
    
    return territorial_mapping

if __name__ == "__main__":
    extract_territorial_data()

