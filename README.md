# Shopify Book Descriptions Updater

Automatically fetch book descriptions from Google Books API and update Shopify products.

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Create `config.json` from the example:
```bash
cp config.json.example config.json
```

3. Edit `config.json` with your Shopify credentials:
   - `shop_url`: Your Shopify store URL (e.g., `your-shop.myshopify.com`)
   - `access_token`: Your Shopify Admin API access token

4. Export your products from Shopify as `products.json`

## Getting Shopify API Credentials

1. Go to your Shopify Admin panel
2. Navigate to Apps → Develop apps (or Apps → Manage private apps for older stores)
3. Create a new app
4. Under "Admin API", add the following scopes:
   - `read_products`
   - `write_products`
5. Install the app and copy the Admin API access token

## Usage

Run the script:
```bash
python update_descriptions.py
```

The script will:
1. Read products from `products.json`
2. Extract ISBNs from product variant metafields (namespace: "product", key: "isbn")
3. Fetch descriptions from Google Books API
4. Update product descriptions in Shopify
5. Display a summary of results

## Products JSON Format

Your `products.json` should follow this structure:
```json
{
  "products": [{
    "id": 123456789,
    "title": "Book Title",
    "variants": [{
      "id": 987654321,
      "sku": "BOOK-001",
      "metafields": [{
        "namespace": "product",
        "key": "isbn",
        "value": "978-0-123456-78-9",
        "type": "single_line_text_field"
      }]
    }]
  }]
}
```

## How It Works

- The script extracts ISBNs from variant metafields with namespace "product" and key "isbn"
- Book descriptions are fetched from Google Books API (no API key required for basic usage)
- A 1-second delay is added between requests to avoid rate limiting
- Results are categorized as: success, failed, book not found, or products without ISBN
