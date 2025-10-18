import requests
import time
import json
import sys
from typing import Dict

SHOPIFY_API_VERSION = "2024-01"

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
        return True
    except requests.exceptions.RequestException as e:
        print(f"  ❌ Error: {e}")
        return False

def process_products(input_file: str, shop_url: str, access_token: str, delay: float = 1.0):
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
    print(f"Found {len(products)} products to update\n")
    
    results = {
        'success': 0,
        'failed': 0,
        'skipped': 0
    }
    
    for i, product in enumerate(products, 1):
        product_id = str(product.get('id'))
        product_title = product.get('title', 'Unknown')
        description = product.get('body_html', '')
        
        print(f"[{i}/{len(products)}] Updating: {product_title} (ID: {product_id})")
        
        if not description or description.strip() == "":
            print(f"  ⚠️  No description to update, skipping")
            results['skipped'] += 1
            continue
        
        success = update_shopify_product(shop_url, access_token, product_id, description)
        
        if success:
            print(f"  ✅ Successfully updated")
            results['success'] += 1
        else:
            results['failed'] += 1
        
        if i < len(products):
            time.sleep(delay)
    
    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)
    print(f"✅ Successfully updated: {results['success']}")
    print(f"❌ Failed to update: {results['failed']}")
    print(f"⚠️  Skipped (no description): {results['skipped']}")
    print(f"\nTotal products processed: {len(products)}")
    print("="*60)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python update_shopify.py <products_with_descriptions.json>")
        print("\nExample:")
        print("  python update_shopify.py products_with_descriptions.json")
        print("\nMake sure you have config.json set up with your Shopify credentials!")
        sys.exit(1)
    
    input_file = sys.argv[1]
    
    try:
        with open('config.json', 'r') as f:
            config = json.load(f)
    except FileNotFoundError:
        print("❌ Error: config.json not found!")
        print("Please create config.json with your Shopify credentials.")
        print("See config.json.example for the format.")
        sys.exit(1)
    except json.JSONDecodeError:
        print("❌ Error: config.json is not valid JSON!")
        sys.exit(1)
    
    shop_url = config.get('shop_url')
    access_token = config.get('access_token')
    
    if not shop_url or not access_token:
        print("❌ Error: config.json must contain 'shop_url' and 'access_token'")
        sys.exit(1)
    
    print(f"🏪 Connected to Shopify store: {shop_url}")
    
    process_products(input_file, shop_url, access_token)
