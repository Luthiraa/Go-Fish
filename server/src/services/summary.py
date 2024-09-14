import requests
import bs4
import urllib.parse

text = "dog water"
url = 'https://google.com/search?q=' + text

request_result = requests.get(url)

# Parse the fetched URL content with BeautifulSoup
soup = bs4.BeautifulSoup(request_result.text, "html.parser")

# Initialize a list to store the top 5 results
results = []

# Function to extract the text from a webpage
def extract_page_text(page_url):
    try:
        page_response = requests.get(page_url)
        page_soup = bs4.BeautifulSoup(page_response.text, "html.parser")
        
        # Extract text from the page. This is a simple method and can be improved based on the page structure.
        paragraphs = page_soup.find_all('p')  # Extracts all text inside <p> tags
        page_text = " ".join([para.get_text() for para in paragraphs])
        return page_text
    except Exception as e:
        print(f"Error fetching {page_url}: {str(e)}")
        return ""

# Find all result divs, limiting to top 5
for g in soup.find_all('div', class_='BNeawe vvjwJb AP7Wnd')[:5]:
    title = g.get_text()
    # Get the parent anchor tag's href (link) and clean it
    parent_a_tag = g.find_parent('a')
    if parent_a_tag and 'href' in parent_a_tag.attrs:
        link = parent_a_tag['href']
        # Google links usually start with "/url?q=", so we split and decode the URL
        if link.startswith("/url?q="):
            link = link.split("/url?q=")[1].split("&")[0]  # Extract the actual URL
            link = urllib.parse.unquote(link)  # Decode the URL
        
        # Fetch and print the page text from each link
        page_text = extract_page_text(link)
        print(f"Title: {title}")
        print(f"Link: {link}")
        print(f"Extracted Text: {page_text[:500]}")  # Print the first 500 characters to avoid too much output
        print("-" * 40)


