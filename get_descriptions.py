import requests
import time
import json
import sys
from typing import Dict, Optional

GOOGLE_BOOKS_API_URL = "https://www.googleapis.com/books/v1/volumes"

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
            print(f"  ⚠️  No book found for ISBN: {isbn}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"  ❌ Error fetching book {isbn}: {e}")
        return None

def extract_isbn_from_product(product: Dict) -> Optional[str]:
    for variant in product.get('variants', []):
        metafields = variant.get('metafields', [])
        for metafield in metafields:
            if metafield.get('namespace') == 'product' and metafield.get('key') == 'isbn':
                isbn = metafield.get('value', '').strip()
                if isbn:
                    return isbn
    return None

def process_products(input_file: str, output_file: str, delay: float = 1.0):
    print(f"\n📖 Reading products from: {input_file}")
    
    try:
        with open(input_file, 'r') as f:
            products_data = json.load(f)
    except FileNotFoundError:
        print(f"❌ Error: File '{input_file}' not found!")
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"❌ Error: File '{input_file}' is not valid JSON!")
        sys.exit(1)
    
    products = products_data.get('products', [])
    print(f"Found {len(products)} products to process\n")
    
    results = {
        'success': 0,
        'not_found': 0,
        'no_isbn': 0
    }
    
    for i, product in enumerate(products, 1):
        product_id = product.get('id')
        product_title = product.get('title', 'Unknown')
        
        print(f"[{i}/{len(products)}] Processing: {product_title} (ID: {product_id})")
        
        isbn = extract_isbn_from_product(product)
        
        if not isbn:
            print(f"  ⚠️  No ISBN found in metafields")
            results['no_isbn'] += 1
            continue
        
        print(f"  📚 ISBN: {isbn}")
        
        description = fetch_book_description(isbn)
        
        if description:
            product['body_html'] = description
            print(f"  ✅ Description fetched ({len(description)} characters)")
            results['success'] += 1
        else:
            results['not_found'] += 1
        
        if i < len(products):
            time.sleep(delay)
    
    print(f"\n💾 Saving results to: {output_file}")
    with open(output_file, 'w') as f:
        json.dump(products_data, f, indent=2)
    
    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)
    print(f"✅ Successfully fetched descriptions: {results['success']}")
    print(f"⚠️  Book not found in Google Books: {results['not_found']}")
    print(f"⚠️  Products without ISBN: {results['no_isbn']}")
    print(f"\nTotal products processed: {len(products)}")
    print(f"Output saved to: {output_file}")
    print("="*60)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python get_descriptions.py <input_file.json> [output_file.json]")
        print("\nExample:")
        print("  python get_descriptions.py products.json")
        print("  python get_descriptions.py products.json products_with_descriptions.json")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else "products_with_descriptions.json"
    
    process_products(input_file, output_file)
