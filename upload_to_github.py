#!/usr/bin/env python3
"""
Script to help upload territorial_mapping.json to GitHub.
This script provides instructions for manual upload since we can't directly push to GitHub from here.
"""

import json
import os

def main():
    print("GitHub Upload Instructions for Territorial Data")
    print("=" * 50)
    
    # Check if territorial_mapping.json exists
    if not os.path.exists('territorial_mapping.json'):
        print("ERROR: territorial_mapping.json not found. Run extract_territorial_data.py first.")
        return
    
    print("SUCCESS: territorial_mapping.json found!")
    print("\nTo upload to GitHub:")
    print("1. Go to: https://github.com/WhaleCancer/LichenThumbnail")
    print("2. Navigate to the 'main' branch")
    print("3. Click 'Add file' -> 'Upload files'")
    print("4. Drag and drop 'territorial_mapping.json'")
    print("5. Add commit message: 'Add territorial mapping data'")
    print("6. Click 'Commit changes'")
    print("\nOnce uploaded, your Streamlit app will be able to access the territorial data!")
    
    # Show file size
    file_size = os.path.getsize('territorial_mapping.json')
    print(f"\nFILE SIZE: {file_size:,} bytes ({file_size/1024:.1f} KB)")
    
    # Show preview of data
    with open('territorial_mapping.json', 'r') as f:
        data = json.load(f)
    
    print(f"DATA: Contains territorial data for {len(data)} images")
    
    # Count territories
    territories = {}
    for mapping in data.values():
        territory = mapping.get('first_nation', 'Unknown')
        territories[territory] = territories.get(territory, 0) + 1
    
    print("\nTERRITORIES INCLUDED:")
    for territory, count in sorted(territories.items()):
        print(f"   {territory}: {count} images")

if __name__ == "__main__":
    main()
