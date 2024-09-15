import requests
import json
# Shopify API credentials
SHOPIFY_ACCESS_TOKEN = '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'
STORE_URL = 'https://c6805f-4b.myshopify.com'
# Fetch products from the Shopify store
def fetch_shopify_products():
    url = f"{STORE_URL}/admin/api/2024-01/products.json"
    headers = {
        "X-Shopify-Access-Token": SHOPIFY_ACCESS_TOKEN
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()  # Products JSON data
    else:
        return {"error": response.status_code, "message": response.text}
# Example usage:
products = fetch_shopify_products()
if 'products' in products:
    for product in products['products']:
        product_url = f"{STORE_URL}/products/{product['handle']}"
        print(f"Title: {product['title']}")
        print(f"Price: {product['variants'][0]['price']}")
        print(f"Image: {product['image']['src'] if product.get('image') else 'No image'}")
        print(f"Product URL: {product_url}")
else:
    print(f"Error fetching products: {products['message']}")