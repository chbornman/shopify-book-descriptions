# Shopify Book Descriptions Updater

This tool automatically fetches book descriptions from Google Books and adds them to your Shopify products. Perfect for bookstores that want to add professional descriptions to their inventory without manually copying and pasting hundreds of descriptions.

## What This Tool Does

1. Reads your Shopify product list (which includes ISBN numbers stored in product metafields)
2. Looks up each ISBN in Google Books database
3. Downloads the book description
4. Updates your Shopify product with that description

## Before You Start

You'll need:
- A computer with Python installed (see installation instructions below)
- Admin access to your Shopify store
- Products in Shopify that have ISBN numbers stored in metafields
- About 30-45 minutes to set everything up

### ⚠️ IMPORTANT: Test First on a Development Store

**We STRONGLY recommend testing this tool on a Shopify development/test store before running it on your live production store.**

**Why?** This tool will modify your product descriptions. While it only updates descriptions and doesn't delete or modify other product data, it's always safer to test first.

**How to create a development store:**

1. Go to https://www.shopify.com/partners
2. Sign up for a free Shopify Partner account
3. Once logged in, click **Stores** in the left sidebar
4. Click **Add store** → **Create development store**
5. Fill out the store details and create it
6. Add a few test products with ISBN metafields
7. Run this tool on the development store first
8. Once you're confident everything works correctly, use it on your production store

**Development stores are completely free and give you a safe environment to test without any risk to your live store.**

---

## Part 1: Installing Python (If You Don't Have It)

### On Windows:
1. Go to https://www.python.org/downloads/
2. Click the big yellow "Download Python" button
3. Run the installer
4. **IMPORTANT**: Check the box that says "Add Python to PATH" before clicking Install
5. Click "Install Now"

### On Mac:
1. Open Terminal (press Cmd+Space, type "Terminal", press Enter)
2. Type this command and press Enter:
   ```bash
   python3 --version
   ```
3. If you see a version number (like "Python 3.11.5"), you're good to go!
4. If not, install Python from https://www.python.org/downloads/

### On Linux:
Python is usually already installed. Open Terminal and type:
```bash
python3 --version
```

---

## Part 2: Download This Tool

### Option A: Download as ZIP (Easier for Non-Technical Users)
1. Go to https://github.com/chbornman/shopify-book-descriptions
2. Click the green "Code" button
3. Click "Download ZIP"
4. Unzip the file to a location you'll remember (like your Desktop or Documents folder)

### Option B: Using Git (If You Have It)
Open Terminal/Command Prompt and type:
```bash
git clone https://github.com/chbornman/shopify-book-descriptions.git
cd shopify-book-descriptions
```

---

## Part 3: Install Required Software

1. Open Terminal (Mac/Linux) or Command Prompt (Windows)

2. Navigate to the folder where you downloaded the tool:
   ```bash
   cd path/to/shopify-book-descriptions
   ```
   **Example on Windows**: `cd C:\Users\YourName\Desktop\shopify-book-descriptions`
   **Example on Mac**: `cd ~/Desktop/shopify-book-descriptions`

3. Install the required software:
   ```bash
   pip install -r requirements.txt
   ```
   **Mac/Linux users**: If that doesn't work, try `pip3 install -r requirements.txt`

---

## Part 4: Get Your Shopify API Credentials

This is the most technical part, but follow these steps carefully:

### Step 1: Create a Custom App in Shopify

1. Log into your Shopify Admin panel
2. Click on **Settings** (bottom left corner)
3. Click on **Apps and sales channels**
4. Click **Develop apps** (at the top)
5. If you see a button saying "Allow custom app development", click it and confirm
6. Click **Create an app**
7. Give it a name like "Book Description Updater"
8. Click **Create app**

### Step 2: Configure API Permissions

1. Click on **Configure Admin API scopes**
2. Scroll down and find these two permissions:
   - **Products**: Check both `read_products` and `write_products`
3. Click **Save** at the bottom

### Step 3: Install the App

1. Click the **API credentials** tab at the top
2. Click **Install app** 
3. Confirm by clicking **Install**

### Step 4: Get Your Access Token

1. After installing, you'll see **Admin API access token**
2. Click **Reveal token once**
3. **IMPORTANT**: Copy this token immediately and save it somewhere safe
   - You won't be able to see it again!
   - Treat it like a password - don't share it publicly

### Step 5: Get Your Shop URL

Your shop URL is your store's Shopify address. It looks like:
- `your-store-name.myshopify.com`

You can find it in your Shopify admin URL bar.

---

## Part 5: Export Your Products from Shopify

You need to export your products in a specific format with metafields included.

### Method 1: Using Shopify Admin (Recommended)

1. In your Shopify Admin, go to **Products** → **All products**
2. Click **Export**
3. Choose "Plain CSV file" or use the API

**Note**: Unfortunately, the standard Shopify product export doesn't include metafields. You'll need to use one of these methods:

### Method 2: Using a Shopify App

1. Install a metafield export app from the Shopify App Store (search for "metafield export")
2. Many are free or have free trials
3. Export your products including the ISBN metafields

### Method 3: Using the Shopify Admin API Directly

If you're comfortable with APIs, you can use:
```bash
curl -X GET "https://your-store.myshopify.com/admin/api/2024-01/products.json?fields=id,title,variants&limit=250" \
  -H "X-Shopify-Access-Token: your-access-token"
```

Save the output to `products.json`

### Expected Format

Your `products.json` file should look like this:

```json
{
  "products": [
    {
      "id": 123456789,
      "title": "The Great Gatsby",
      "variants": [
        {
          "id": 987654321,
          "sku": "BOOK-001",
          "metafields": [
            {
              "namespace": "product",
              "key": "isbn",
              "value": "9780743273565",
              "type": "single_line_text_field"
            }
          ]
        }
      ]
    }
  ]
}
```

**Important Notes:**
- The ISBN must be stored in a metafield with namespace `product` and key `isbn`
- If your ISBNs are stored differently, you may need to adjust them first

---

## Part 6: Configure the Tool

1. In the folder where you downloaded the tool, find the file `config.json.example`

2. Make a copy of it and rename it to `config.json`

3. Open `config.json` in a text editor (Notepad on Windows, TextEdit on Mac)

4. Fill in your information:
   ```json
   {
     "shop_url": "your-store-name.myshopify.com",
     "access_token": "paste-your-access-token-here"
   }
   ```

5. Save the file

**Security Warning**: Never share your `config.json` file or post it online. It contains your store's access credentials!

---

## Part 7: Add Your Products File

1. Place your `products.json` file in the same folder as `update_descriptions.py`

2. Make sure it's named exactly `products.json` (all lowercase)

---

## Part 8: Run the Tool

### ⚠️ Remember: Test on a Development Store First!

Before running on your live store, make sure you've tested on a development store (see "Before You Start" section).

### On Windows:
1. Open Command Prompt
2. Navigate to your project folder:
   ```bash
   cd C:\path\to\shopify-book-descriptions
   ```
3. Run the script:
   ```bash
   python update_descriptions.py
   ```

### On Mac/Linux:
1. Open Terminal
2. Navigate to your project folder:
   ```bash
   cd ~/path/to/shopify-book-descriptions
   ```
3. Run the script:
   ```bash
   python3 update_descriptions.py
   ```

### What You'll See

The tool will display progress as it runs:

```
Processing Product 123456789 (The Great Gatsby) - ISBN: 9780743273565
Successfully updated product 123456789

Processing Product 987654321 (To Kill a Mockingbird) - ISBN: 9780061120084
Successfully updated product 987654321

==================================================
SUMMARY
==================================================
Successfully updated: 45
Failed to update: 2
Book not found in Google Books: 3
Products without ISBN: 5
```

---

## Part 9: Verify the Results

1. Go back to your Shopify Admin
2. Open a few products that were listed as "Successfully updated"
3. Check that the descriptions were added correctly
4. If everything looks good, you're done!

---

## Troubleshooting

### "Python is not recognized" or "command not found"
- **Windows**: You didn't check "Add Python to PATH" during installation. Reinstall Python and check that box.
- **Mac/Linux**: Try using `python3` instead of `python`

### "No module named 'requests'"
Run this command:
```bash
pip install -r requirements.txt
```
Or on Mac/Linux:
```bash
pip3 install -r requirements.txt
```

### "Error updating product: 401 Unauthorized"
- Your access token is wrong or has expired
- Go back to Part 4 and get a new access token
- Make sure you copied the entire token with no extra spaces

### "No book found for ISBN: [number]"
- The ISBN isn't in Google Books database
- Double-check that the ISBN is correct
- Some books (especially very new or very old ones) might not be in Google Books

### "Products without ISBN: [large number]"
- Your product metafields might not be set up correctly
- Check that ISBNs are stored in metafields with namespace `product` and key `isbn`
- You may need to add ISBNs to your products first

### The tool is running but nothing is updating
- Check your Shopify API permissions - make sure `write_products` is enabled
- Verify your shop URL is correct (should be `your-store.myshopify.com`)
- Check that you're using the correct access token

---

## Important Notes

### Rate Limiting
- The tool includes a 1-second delay between each product to avoid overwhelming the Google Books API
- For 100 products, expect the tool to run for about 2-3 minutes
- Don't run the tool multiple times simultaneously

### API Usage
- Google Books API is free for basic usage (no API key needed)
- Shopify API has rate limits - the tool respects these automatically

### Data Safety
- The tool only updates product descriptions (the `body_html` field)
- It does not modify titles, prices, variants, or other product information
- The tool does not delete any existing data

### Testing on a Development Store (Recommended Workflow)

**Step-by-step process for safe testing:**

1. **Create a development store** (free from Shopify Partners program at https://www.shopify.com/partners)
2. **Add a few test products** with ISBN metafields to the development store
3. **Export those test products** as `products.json`
4. **Create API credentials** for the development store (follow Part 4)
5. **Update your `config.json`** with the development store's URL and access token
6. **Run the tool** on the development store
7. **Verify the results** look correct
8. **Once confident**, switch to your production store:
   - Export products from your production store
   - Update `config.json` with production store credentials
   - Run the tool on production

This workflow ensures you never risk accidentally damaging your live store data.

---

## Getting Help

If you run into issues:

1. Check the Troubleshooting section above
2. Make sure all files are in the right place and named correctly
3. Double-check your Shopify credentials
4. Open an issue on GitHub: https://github.com/chbornman/shopify-book-descriptions/issues

---

## What Files Do What?

- **update_descriptions.py** - The main script that does all the work
- **config.json** - Your Shopify credentials (you create this)
- **products.json** - Your exported products (you create this)
- **requirements.txt** - List of software needed (used during installation)
- **config.json.example** - Template for your config file
- **products.json.example** - Example of what your products file should look like

---

## Advanced: Running in Dry-Run Mode

Want to test without actually updating anything? Edit `update_descriptions.py` and look for the commented-out dry-run mode, or contact the developer for a dry-run version.

---

## Credits

This tool uses:
- Google Books API for book descriptions
- Shopify Admin API for updating products
- Python with the `requests` library

---

## License

This project is open source and free to use for your bookstore.
