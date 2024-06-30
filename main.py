import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import re
import json

def scrape_website_info(url):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(options=chrome_options)
    
    driver.get(url)
    time.sleep(5)
    
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    
    website_info = {
        'url': url,
        'title': '',
        'products_services': [],
        'social_media': [],
        'contact_info': '',
        'about_info': ''
    }
    
    title_elem = soup.find('title')
    if title_elem:
        website_info['title'] = title_elem.text.strip()
    
    product_elems = soup.find_all(['h2', 'h3', 'h4'], string=re.compile(r'products|services', re.IGNORECASE))
    for elem in product_elems:
        next_elem = elem.find_next(['ul', 'p'])
        if next_elem:
            website_info['products_services'].extend([item.text.strip() for item in next_elem.find_all('li')])
    
    social_media_patterns = ['facebook.com', 'twitter.com', 'linkedin.com', 'instagram.com']
    for link in soup.find_all('a', href=True):
        if any(pattern in link['href'] for pattern in social_media_patterns):
            website_info['social_media'].append(link['href'])
    
    contact_elem = soup.find(['div', 'section'], string=re.compile(r'contact', re.IGNORECASE))
    if contact_elem:
        website_info['contact_info'] = contact_elem.get_text(strip=True)
    
    about_elem = soup.find(['div', 'section'], string=re.compile(r'about', re.IGNORECASE))
    if about_elem:
        website_info['about_info'] = about_elem.get_text(strip=True)
    
    driver.quit()
    return website_info

websites = [
    'https://amul.com/',
    'https://www.paperboatfoods.com/',
    'https://www.myntra.com/',
    'https://www.parleagro.com/',
    'https://www.patanjaliayurved.net/',
    'https://blinkit.com/',
    'https://himalayawellness.in/',
    'https://www.biba.in/',
    'https://www.indiamart.com/',
    'https://www.namasteindiafoods.com/'
]

all_website_info = []

for website in websites:
    print(f"Scraping information for {website}...")
    website_info = scrape_website_info(website)
    all_website_info.append(website_info)
    time.sleep(5)

# Save the results to a JSON file
with open('website_info.json', 'w', encoding='utf-8') as f:
    json.dump(all_website_info, f, ensure_ascii=False, indent=4)

print("Scraping completed. Results saved to website_info.json")