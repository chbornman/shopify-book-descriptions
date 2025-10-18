import requests
import time
import json
from typing import List, Dict, Optional

GOOGLE_BOOKS_API_URL = "https://www.googleapis.com/books/v1/volumes"
SHOPIFY_API_VERSION = "2024-01"

def fetch_book_description(isbn: str) -> Optional[str]:
    params = {
        'q': f'isbn:{isbn}',
        'maxResults': 1
    }
    
    try:
        response = requests.get(GOOGLE_BOOKS_API_URL, params=params)
        response.raise_for_status()
        data = response.json()
        
        if 'items' in data and len(data['items']) > 0:
            volume_info = data['items'][0].get('volumeInfo', {})
            description = volume_info.get('description')
            return description
        else:
            print(f"No book found for ISBN: {isbn}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Error fetching book {isbn}: {e}")
        return None

def update_shopify_product(shop_url: str, access_token: str, product_id: str, description: str) -> bool:
    url = f"https://{shop_url}/admin/api/{SHOPIFY_API_VERSION}/products/{product_id}.json"
    
    headers = {
        'X-Shopify-Access-Token': access_token,
        'Content-Type': 'application/json'
    }
    
    payload = {
        'product': {
            'id': product_id,
            'body_html': description
        }
    }
    
    try:
        response = requests.put(url, headers=headers, json=payload)
        response.raise_for_status()
        print(f"Successfully updated product {product_id}")
        return True
    except requests.exceptions.RequestException as e:
        print(f"Error updating product {product_id}: {e}")
        return False

def extract_isbn_from_product(product: Dict) -> Optional[str]:
    for variant in product.get('variants', []):
        metafields = variant.get('metafields', [])
        for metafield in metafields:
            if metafield.get('namespace') == 'product' and metafield.get('key') == 'isbn':
                isbn = metafield.get('value', '').strip()
                if isbn:
                    return isbn
    return None

def process_products(products_data: Dict, shop_url: str, access_token: str, delay: float = 1.0):
    results = {
        'success': [],
        'failed': [],
        'not_found': [],
        'no_isbn': []
    }
    
    products = products_data.get('products', [])
    
    for product in products:
        product_id = str(product['id'])
        product_title = product.get('title', 'Unknown')
        
        isbn = extract_isbn_from_product(product)
        
        if not isbn:
            print(f"\nProduct {product_id} ({product_title}): No ISBN found in metafields")
            results['no_isbn'].append({'id': product_id, 'title': product_title})
            continue
        
        print(f"\nProcessing Product {product_id} ({product_title}) - ISBN: {isbn}")
        
        description = fetch_book_description(isbn)
        
        if description:
            success = update_shopify_product(shop_url, access_token, product_id, description)
            if success:
                results['success'].append({'id': product_id, 'title': product_title, 'isbn': isbn})
            else:
                results['failed'].append({'id': product_id, 'title': product_title, 'isbn': isbn})
        else:
            results['not_found'].append({'id': product_id, 'title': product_title, 'isbn': isbn})
        
        time.sleep(delay)
    
    print("\n" + "="*50)
    print("SUMMARY")
    print("="*50)
    print(f"Successfully updated: {len(results['success'])}")
    print(f"Failed to update: {len(results['failed'])}")
    print(f"Book not found in Google Books: {len(results['not_found'])}")
    print(f"Products without ISBN: {len(results['no_isbn'])}")
    
    return results

if __name__ == "__main__":
    with open('config.json', 'r') as f:
        config = json.load(f)
    
    shop_url = config['shop_url']
    access_token = config['access_token']
    
    with open('products.json', 'r') as f:
        products_data = json.load(f)
    
    process_products(products_data, shop_url, access_token)
