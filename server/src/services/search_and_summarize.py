import requests
import bs4
import urllib.parse
from groq import Groq
import logging
from .github_search import search_github_code  
from shopify import fetch_shopify_products  # Imported fetch_shopify_products
import json  # Imported json for parsing

# Initialize the Groq API client
api_key = "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"
client = Groq(api_key=api_key)

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

# Function to get top 5 Google search results
def google_search(query, num_results=5):
    url = 'https://google.com/search?q=' + urllib.parse.quote(query)
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    request_result = requests.get(url, headers=headers)
    soup = bs4.BeautifulSoup(request_result.text, "html.parser")
    
    results = []
    

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
            if len(results) >= num_results:
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
def summarize_text(text):
    # Modify the prompt to include the image URL
    prompt = f"Summarize the following text and provide key takeaways. Make sure to return your answer in Markdown only. Format the bullet points, paragraphs, links, bold, etc., styling with appropriate tags. Make it look super pretty, readable, and well-formatted with spaces. Have extra links at the end too. Here is the text to summarize:\n\n{text}"
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

# New function to find matching products
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
        products_list.append({
            'title': title,
            'Price': price,
            'AbsoluteImageURL': image_url
        })

    # Prepare the prompt
    prompt = f"""I have the following products in my shopify store:

{products_list}

Find any products that are similar to the following query: "{query}".

Return the matching products as a JSON list of objects, where each object has the keys "title", "Price", "AbsoluteImageURL".

If there are no matching products, return an empty list.

Here is an example of the desired output:

[{{"title": "Blue fish",
"Price": "0.87",
"AbsoluteImageURL": "https://cdn.shopify.com/s/files/1/0674/2363/3586/files/1930365526_e36f10b40e_c.jpg?v=1726367899"}}]
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
        matching_products = json.loads(matching_products_str)
    except json.JSONDecodeError as e:
        logging.error(f"Error decoding JSON: {str(e)}")
        matching_products = []

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
    summary = ""
    # Call search_github_code and format the summary
    github_results = search_github_code(query, "Luthiraa/Go-Fish", "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")
    if github_results:
        snippet, line_number, file_url = github_results

        # #! Save the snippet to a text file
        # summary = f"Found in line: {line_number} \n \n URL: {file_url} \n```python\n{snippet}\n```\n"
    else:
        summary = ""
        snippet, line_number, file_url = "", "", ""

    # Send the combined text and image URL to Groq for summarization
    summary += summarize_text(all_texts)

    logging.debug(f"Summary from Groq: {summary}")

    # Find matching products
    matching_products = find_matching_products(query)
    logging.debug(f"Matching products: {matching_products}")

    # Return the summary, resources, image URL, Reddit embed, GitHub results, and matching products
    return summary, resource_list, image_url, reddit_embed,  snippet,line_number, file_url, matching_products

if __name__ == "__main__":
    query = "find me where summarize_text is"
    summary, resources, image_url, reddit_embed, github_results, matching_products = process_search_and_summarize(query)
    important = extract_important_words(query)
    print("### Summary from Groq ###")
    print(summary)
    print("### Matching Products ###")
    print(matching_products)
