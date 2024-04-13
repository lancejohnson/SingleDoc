import requests
import requests_cache
from bs4 import BeautifulSoup
import tldextract
from time import sleep


requests_cache.install_cache('cache')
cache = requests_cache.get_cache()

# Set the starting URL
start_url = "https://developer.close.io"

# Extract the subdomain
subdomain = tldextract.extract(start_url).subdomain

# Create a set to store the URLs to be scraped
urls_to_scrape = set([start_url])

# Create a set to store the URLs that have already been scraped
scraped_urls = set()

# Create a set to store the URLs within the subdomain
subdomain_urls = set()

# Create a dictionary to store the text content of each page
page_content_htmls = {}


# Create a function to scrape a URL
def scrape_url(url):
    # Add the URL to the set of scraped URLs
    scraped_urls.add(url)
    # Get the page content
    response = requests.get(url)
    # Parse the page content
    soup = BeautifulSoup(response.content, "html.parser")
    # Find all the links on the page
    for link in soup.find_all("a"):
        # Get the URL
        href = link.get("href")
        full_url = f"{start_url}{href}"
        # If the URL is within the subdomain and has not been scraped, add it to the set of URLs to be scraped
        if href and (href.startswith('/')) and '#' not in href and full_url not in scraped_urls:
            urls_to_scrape.add(full_url)
            subdomain_urls.add(full_url)
    page_content_html = soup.find(class_='css-ifkzhd ernxcdh0')
    if not page_content_html:
        print("No HTML for that CSS Selector")
        # Save the HTML content of the page
    page_content_htmls[url] = str(page_content_html)
    # Pause for two seconds
    is_cached = cache.contains(response.cache_key)
    print(f"{full_url} Done | Cached = {is_cached}")
    # If not cached wait so we don't overload the API (limited to 1 call/0.5 sec)
    if not is_cached:
        sleep(0.5)


# Scrape all the URLs in the set of URLs to be scraped
while urls_to_scrape:
    url = urls_to_scrape.pop()
    scrape_url(url)

# Write the text content of each page to a file
with open('finished_docs/close_crm_docs.html', 'w') as file:
    for url, text in page_content_htmls.items():
        file.write(f"<h1>{url}<br/>{text}</h1>")
