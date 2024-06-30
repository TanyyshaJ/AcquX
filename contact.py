import requests
from bs4 import BeautifulSoup
import re
import json
from urllib.parse import urljoin

def find_contact_info(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        contact_info = {
            'emails': set(),
            'phones': set(),
            'social_media': set()
        }
        
        # Find emails
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        emails = re.findall(email_pattern, response.text)
        contact_info['emails'].update(emails)
        
        # Find phone numbers (this is a simple pattern and might need refinement)
        phone_pattern = r'\+?[0-9]{10,14}'
        phones = re.findall(phone_pattern, response.text)
        contact_info['phones'].update(phones)
        
        # Find social media links
        social_media_patterns = ['facebook.com', 'twitter.com', 'linkedin.com', 'instagram.com']
        for link in soup.find_all('a', href=True):
            if any(pattern in link['href'] for pattern in social_media_patterns):
                contact_info['social_media'].add(link['href'])
        
        # Look for 'Contact Us' or similar pages
        contact_links = soup.find_all('a', text=re.compile(r'contact', re.I))
        for link in contact_links:
            contact_url = urljoin(url, link.get('href'))
            contact_response = requests.get(contact_url, headers=headers, timeout=10)
            contact_soup = BeautifulSoup(contact_response.text, 'html.parser')
            
            # Search for emails and phones on the contact page
            contact_emails = re.findall(email_pattern, contact_response.text)
            contact_phones = re.findall(phone_pattern, contact_response.text)
            contact_info['emails'].update(contact_emails)
            contact_info['phones'].update(contact_phones)
        
        # Convert sets to lists for JSON serialization
        contact_info['emails'] = list(contact_info['emails'])
        contact_info['phones'] = list(contact_info['phones'])
        contact_info['social_media'] = list(contact_info['social_media'])
        
        return contact_info
    
    except Exception as e:
        print(f"Error scraping {url}: {str(e)}")
        return None

# Load the existing data
with open('website_info.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Find contact information for each website
for website in data:
    print(f"Scraping contact info for {website['url']}...")
    contact_info = find_contact_info(website['url'])
    if contact_info:
        website['contact_details'] = contact_info

# Save the updated data
with open('website_info_with_contacts.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)

print("Contact information has been added to the JSON file.")