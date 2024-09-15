import requests
import bs4
import urllib.parse
import json
import logging
from groq import Groq
from .github_search import extract_keyword, search_github_code  
from .shopify import fetch_shopify_products 

# Initialize the Groq API client
api_key = "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"
client = Groq(api_key=api_key)

STORE_URL = 'https://c6805f-4b.myshopify.com'

# Function to extract the text from a webpage
def extract_page_text(page_url):
    try:
        page_response = requests.get(page_url)
        page_soup = bs4.BeautifulSoup(page_response.text, "html.parser")
        
        # Extract text from the page (within <p> tags)
        paragraphs = page_soup.find_all('p')
        page_text = " ".join([para.get_text() for para in paragraphs])
        return page_text
    except Exception as e:
        print(f"Error fetching {page_url}: {str(e)}")
        return ""

def google_search(query, num_results=5):
    url = 'https://google.com/search?q=' + urllib.parse.quote(query)
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    request_result = requests.get(url, headers=headers)
    soup = bs4.BeautifulSoup(request_result.text, "html.parser")
    
    results = []
    reddit_link_found = False
    
    # Initial search for the top 5 results
    for g in soup.find_all('div', class_='BNeawe vvjwJb AP7Wnd'):
        title = g.get_text()
        parent_a_tag = g.find_parent('a')
        if parent_a_tag and 'href' in parent_a_tag.attrs:
            link = parent_a_tag['href']
            if link.startswith("/url?q="):
                link = link.split("/url?q=")[1].split("&")[0]  
                link = urllib.parse.unquote(link)  
            
            page_text = extract_page_text(link)
            results.append({"title": title, "link": link, "text": page_text})
            
            # Check if the link is from Reddit
            if 'reddit.com' in link:
                reddit_link_found = True
            
            if len(results) >= num_results:
                break  # Stop after getting the top 5 results

    # Always perform a Reddit-specific search
    reddit_url = f"https://google.com/search?q={urllib.parse.quote(query)}+site:reddit.com"
    reddit_request_result = requests.get(reddit_url, headers=headers)
    reddit_soup = bs4.BeautifulSoup(reddit_request_result.text, "html.parser")
    
    for g in reddit_soup.find_all('div', class_='BNeawe vvjwJb AP7Wnd'):
        title = g.get_text()
        parent_a_tag = g.find_parent('a')
        if parent_a_tag and 'href' in parent_a_tag.attrs:
            link = parent_a_tag['href']
            if link.startswith("/url?q="):
                link = link.split("/url?q=")[1].split("&")[0]  
                link = urllib.parse.unquote(link)  
            
            page_text = extract_page_text(link)
            results.append({"title": title, "link": link, "text": page_text})
            
            # Only one Reddit result is required
            break

    return results

def google_image_search(query):
    url = 'https://www.google.com/search?q=' + urllib.parse.quote(query) + '&tbm=isch'
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    response = requests.get(url, headers=headers)
    html = response.text

    soup = bs4.BeautifulSoup(html, 'html.parser')
    images = soup.find_all('img')

    for img in images:
        img_url = img.get('src')
        if img_url and img_url.startswith('http'):
            return img_url
    return None

# Function to send the extracted text to the Groq LLM for summarization
# Function to send the extracted text to the Groq LLM for a brief summary
def summarize_text(text):
    prompt = f"Provide a brief summary (1-2 sentences) of the following text and entire topic using markdown. Feel free to using headings (you must use different sizes), bold, bullet points, italics, links and a lot of new lines to space. A lot. Make sure to only return the direct answer and nothing else.\n\n{text}"
    response = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=100
    )
    return response.choices[0].message.content.strip()

# Function to send the extracted text to the Groq LLM for a detailed summary
def detailed_summarize_text(text):
    prompt = f"Summarize the following text with informative format based on trustworthy sources. Make sure to return your answer in Markdown only and you must use href links, lists, headings, bold, italics and as much styling as possible. Make sure to not return anything else other than the direct answer. Here is the text to summarize:\n\n{text}"
    response = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=500
    )
    return response.choices[0].message.content.strip()

# Function to extract important words from a query using Groq
def extract_important_words(query):
    response = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": f"Extract the most important words from the following query, just give me the words straight up, ONLY THE WORDS, no other text:\n\n{query}"}
        ],
        max_tokens=50
    )
    important_words = response.choices[0].message.content.strip().split(' ')

    return important_words

# Function to get Reddit embed response
def get_reddit_embed(reddit_url):
    oembed_url = 'https://www.reddit.com/oembed'
    params = {'url': reddit_url}
    try:
        response = requests.get(oembed_url, params=params)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Error fetching Reddit oEmbed: {str(e)}")
        return None

def find_matching_products(query):
    products_data = fetch_shopify_products()

    if 'products' in products_data:
        products = products_data['products']
    else:
        logging.error(f"Error fetching products: {products_data.get('message', 'Unknown error')}")
        return []

    # Extract necessary fields from products
    products_list = []

    for product in products:
        title = product.get('title', '')
        price = product.get('variants', [{}])[0].get('price', '')
        image_url = ''
        if product.get('image'):
            image_url = product['image'].get('src', '')
        
        # Construct the product URL using the handle
        product_url = f"{STORE_URL}/products/{product.get('handle', '')}"
        
        products_list.append({
            'title': title,
            'Price': price,
            'AbsoluteImageURL': image_url,
            'ProductURL': product_url
        })

    # Simplify the prompt and make it more explicit
    prompt = f"""
You have the following products in your Shopify store:

{json.dumps(products_list, indent=4)}

Please return the products related to the query: "{query}" as a JSON list. ONLY return the list of products. No other words. Nothing else.
Each product in the list should have the following keys:
- "title"
- "Price"
- "AbsoluteImageURL"
- "ProductURL"

Return only the JSON list of matching products. If no products match, return an empty list.
"""

    response = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=500
    )

    matching_products_str = response.choices[0].message.content.strip()

    try:
        # Try to parse the JSON response
        matching_products = json.loads(matching_products_str)
    except json.JSONDecodeError as e:
        logging.error(f"Error decoding JSON: {str(e)}")
        matching_products = []

    logging.debug(f"MATCHED PRODUCTS: {matching_products}")

    return matching_products

# Main function to fetch top 5 results, process them, and send to Groq
def process_search_and_summarize(query):
    logging.basicConfig(level=logging.DEBUG)
    logging.debug(f"Processing query: {query}")
    
    important_words = extract_important_words(query)
    logging.debug(f"Important words: {important_words}")
    
    search_results = google_search(query)
    all_texts = ""
    resource_list = []
    reddit_links = []
    
    # Combine all the text from the top 5 results
    for result in search_results:
        title = result['title']
        link = result['link']
        text = result['text']
        all_texts += f"\n\nFrom {title} ({link}):\n{text[:1000]}"  # Limit text from each source
        resource_list.append(link)
        
        # Check if link is from Reddit
        if 'reddit.com' in link:
            reddit_links.append(link)
    
    logging.debug(f"Combined text: {all_texts[:500]}...")  # Print first 500 characters for brevity

    # Get Reddit embed response
    reddit_embed = None
    if reddit_links:
        reddit_link = reddit_links[0]  # Use the first Reddit link
        reddit_embed = get_reddit_embed(reddit_link)
        logging.debug(f"Reddit embed response: {reddit_embed}")
    else:
        logging.debug("No Reddit link found in search results.")

    # Get image URL
    image_url = google_image_search(query)
    logging.debug(f"Image URL: {image_url}")

    # Initialize summary
    summary = ""
    github_url, github_line_number, github_snippet = "", "", ""
    # Extract the main keyword from the query
    keyword = extract_keyword(query)
    if not keyword:
        logging.error("No valid keyword found in the query.")
        github_url, github_line_number, github_snippet = None, None, None
    else:
        # Call search_github_code and format the summary
        github_token = "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" # Get GitHub Personal Access Token from environment variable
        if not github_token:
            logging.error("GitHub token not found. Please set the GITHUB_TOKEN environment variable.")
        else:
            top_url, top_line_number, top_snippet = search_github_code(keyword, "Luthiraa/Go-Fish", github_token)
            if top_snippet:
                # Save the results to variables
                github_url = top_url
                github_line_number = top_line_number
                github_snippet = top_snippet
                # Format the URL as a hyperlink and the snippet as a code block
                summary += f"Found in line: {github_line_number}\n\nURL: [{github_url}]({github_url})\n\n```python\n{github_snippet}\n```\n"
            else:
                summary += ""

    # Send the combined text and image URL to Groq for summarization
    summary += summarize_text(all_texts)

    detailed_summary = detailed_summarize_text(all_texts)

    logging.debug(f"Summary from Groq: {summary}")

    # Find matching products
    matching_products = find_matching_products(query)
    logging.debug(f"Matching products: {matching_products}")

    # Return the summary, resources, image URL, Reddit embed, GitHub results, and matching products
    return summary, detailed_summary, resource_list, image_url, reddit_embed, github_url, github_line_number, github_snippet, matching_products

if __name__ == "__main__":
    query = "find me where summarize_text is"
    summary, detailed_summary, resources, image_url, reddit_embed, github_url, github_line_number, github_snippet, matching_products = process_search_and_summarize(query)
    important = extract_important_words(query)
    print("### Summary from Groq ###")
    print(summary)
    print("### Matching Products ###")
    print(matching_products)
    print("### GitHub Search Results ###")
    print(f"URL: {github_url}")
    print(f"Line Number: {github_line_number}")
    print(f"Snippet: {github_snippet}")
