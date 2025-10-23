import requests
from bs4 import BeautifulSoup
import csv

def get_html(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except requests.HTTPError as e:
        print(f"HTTP error: {e} for URL: {url}")
        return None

def clean_text(text):
    # Replace non-breaking spaces
    text = text.replace('\xa0', ' ')
    # Remove space after '/'
    text = text.replace('/ ', '/')
    # Add space after full stops if missing
    text = text.replace('. ', '.').replace('.', '. ')
    # Correct "moreabout" to "more about"
    text = text.replace('moreabout', 'more about')
    return text.strip()

def extract_data(base_url, start, end):
    data = []
    for i in range(start, end + 1):
        product_number = str(i).zfill(3)
        page_url = f"{base_url}/CamilleHavasBC-{product_number}"
        
        html = get_html(page_url)
        if html is None:
            print(f"Failed to retrieve: {page_url}")
            continue
        
        soup = BeautifulSoup(html, 'html.parser')
        
        # Extract the photo name
        photo_name_tag = soup.find('h1', {'class': 'h2 product-single__title'})
        photo_name = clean_text(photo_name_tag.get_text(strip=True)) if photo_name_tag else 'No photo name'
        
        # Extract the description
        description_tag = soup.find('div', {'class': 'product-single__description rte'})
        description_text = clean_text(description_tag.get_text(strip=True)) if description_tag else 'No description'
        
        output_line = f"URL: {page_url} | Photo Name: {photo_name} | Description: {description_text}"
        print(output_line)
        
        # Add to data list
        data.append([page_url, photo_name, description_text])

    return data

def write_to_csv(data, filename='output.csv'):
    try:
        with open(filename, mode='w', newline='', encoding='utf-8') as file:
            csv_writer = csv.writer(file)
            csv_writer.writerow(['URL', 'Photo Name', 'Description'])
            csv_writer.writerows(data)
    except Exception as e:
        print(f"Error writing to CSV: {e}")

base_url = 'https://lichenproject.org/collections/full-library/products'

# Gather data
data = extract_data(base_url, 100, 100)  # Test with a smaller range

# Write to CSV
write_to_csv(data)