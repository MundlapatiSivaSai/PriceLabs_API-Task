# PriceLabs_API-Task

This script is designed to fetch property listings from VRBO (Vacation Rentals by Owner) based on specified criteria, such as location and date range. It utilizes the VRBO GraphQL API to retrieve listings and then generates a CSV file containing details about each listing, including the listing ID, title, nightly price, and URL.

## Live Demo

[PriceLabs Demo](https://colab.research.google.com/drive/1fHShi2t-l2tV547HSh0sULl-98pei4xt?usp=sharing)

## Features

- Fetch listings from VRBO using GraphQL API.
- Retry mechanism with exponential backoff to handle rate limits.
- Generate a CSV file with listings information.

## Prerequisites

Before you run this script, ensure you have the following installed:
- Python 3.x
- `hrequests` library for making HTTP requests. You can install it using pip:
  ```
  pip install -U hrequests
  ```

## Usage

To use this script, follow these steps:

1. Modify the `address` and `page_size` variables in the `main` function to match your search criteria.
   - `address`: The location you are searching for listings in.
   - `page_size`: The number of listings you want to retrieve per page.

2. Run the script:
   ```
   python pricelabs.py
   ```

## Function Descriptions

- **`fetch_listings(address, page_size, retries=5, backoff_factor=1)`**:
  Fetches listings from the VRBO API. Parameters:
  - `address`: Search location.
  - `page_size`: Number of listings per page.
  - `retries`: Number of attempts to make in case of failures or rate limits.
  - `backoff_factor`: Factor by which the wait time increases after each retry.

- **`generate_csv(listings, filename="listings.csv")`**:
  Generates a CSV file from the fetched listings. Parameters:
  - `listings`: The listings data fetched from VRBO.
  - `filename`: Name of the CSV file to generate.

- **`main(address, page_size)`**:
  Main function to run the script. Parameters:
  - `address`: Search location.
  - `page_size`: Number of listings per page.

## Example Output

After running the script, you will get a CSV file named `listings.csv` by default, containing columns for Listing ID, Listing Title, Nightly Price, and Listing URL.

---
