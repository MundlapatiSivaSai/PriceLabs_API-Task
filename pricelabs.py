import hrequests
import csv
import json
import time

def fetch_listings(address, page_size, retries=5, backoff_factor=1):
    url = "https://www.vrbo.com/graphql"
    headers = {
        'authority': 'www.vrbo.com',
        'accept': '*/*',
        'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8,no;q=0.7,de;q=0.6',
        'cache-control': 'no-cache',
        'client-info': 'shopping-pwa,unknown,unknown',
        'content-type': 'application/json',
        'origin': 'https://www.vrbo.com',
        'pragma': 'no-cache',
        'referer': 'https://www.vrbo.com/search?adults=2&amenities=&children=&d1=2023-12-27&d2=2023-12-28&destination=73%20W%20Monroe%20St%2C%20Chicago%2C%20IL%2060603%2C%20USA&endDate=2024-03-05&latLong=&mapBounds=&pwaDialog=&regionId&semdtl=&sort=RECOMMENDED&startDate=2024-03-01&theme=&userIntent=',
        'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'x-enable-apq': 'true',
        'x-page-id': 'page.Hotel-Search,H,20'
    }
    body = json.dumps({
  "operationName": "LodgingPwaPropertySearch",
  "variables": {
    "context": {
      "siteId": 9001001,
      "locale": "en_US",
      "eapid": 1,
      "currency": "USD",
      "device": {
        "type": "DESKTOP"
      },
      "identity": {
        "duaid": "7e524f17-1fa3-5cb8-baf4-dfa5f0f893e4",
        "expUserId": "-1",
        "tuid": "-1",
        "authState": "ANONYMOUS"
      },
      "privacyTrackingState": "CAN_TRACK",
      "debugContext": {
        "abacusOverrides": []
      }
    },
    "criteria": {
      "primary": {
        "dateRange": {
          "checkInDate": {
            "day": 3,
            "month": 3,
            "year": 2024
          },
          "checkOutDate": {
            "day": 5,
            "month": 3,
            "year": 2024
          }
        },
        "destination": {
          "regionName": "73 W Monroe St, Chicago, IL 60603, USA",
          "regionId": None,
          "coordinates": None,
          "pinnedPropertyId": None,
          "propertyIds": None,
          "mapBounds": None
        },
        "rooms": [
          {
            "adults": 2,
            "children": []
          }
        ]
      },
      "secondary": {
        "counts": [
          {
            "id": "resultsStartingIndex",
            "value": 15
          },
          {
            "id": "resultsSize",
            "value": 50
          }
        ],
        "booleans": [],
        "selections": [
          {
            "id": "sort",
            "value": "RECOMMENDED"
          },
          {
            "id": "privacyTrackingState",
            "value": "CAN_TRACK"
          },
          {
            "id": "useRewards",
            "value": "SHOP_WITHOUT_POINTS"
          },
          {
            "id": "searchId",
            "value": "d1342ebe-2e4c-4c8d-8838-a3967204a6f2"
          }
        ],
        "ranges": []
      }
    },
    "destination": {
      "regionName": None,
      "regionId": None,
      "coordinates": None,
      "pinnedPropertyId": None,
      "propertyIds": None,
      "mapBounds": None
    },
    "shoppingContext": {
      "multiItem": None
    },
    "returnPropertyType": False,
    "includeDynamicMap": True
  },
  "extensions": {
    "persistedQuery": {
      "sha256Hash": "e4ffcd90dd44f01455f9ddd89228915a177f9ec674f0df0db442ea1b20f551c3",
      "version": 1
    }
  }
})
    print(f"Fetching the API URL - {url}")

    for attempt in range(retries):
        response = hrequests.post(url, json=body, headers=headers)
        if response.status_code == 200:
            data = response.json()
            listings = data['data']['propertySearch']['propertySearchListings']
            return listings
        elif response.status_code == 429:
            sleep_time = backoff_factor * (2 ** attempt)
            print(f"Rate limit exceeded. Retrying in {sleep_time} seconds...")
            time.sleep(sleep_time)
        else:
            print(f"Failed to fetch listings due to error: {response.status_code}")
            return []
    print("Failed to fetch listings after retrying.")
    return []

def generate_csv(listings, filename="listings.csv"):
    try:
        with open(filename, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Listing ID", "Listing Title", "Nightly Price", "Listing URL"])

            for listing in listings:
                try:
                    writer.writerow([
                        listing['id'],
                        listing.get('headingSection', {}).get('heading', 'N/A'),
                        listing.get('priceSection', {}).get('priceSummary', {}).get('displayMessages', [{}])[0].get('lineItems', [{}])[0].get('price', {}).get('formatted', 'N/A'),
                        listing.get('cardLink', {}).get('resource', {}).get('value', 'N/A')
                    ])
                except (KeyError, TypeError) as e:
                    print(f"Error processing listing: {e}")
    except IOError as e:
        print(f"IOError occurred: {e}")
    except csv.Error as e:
        print(f"CSV error occurred: {e}")

def main(address, page_size):
    listings = fetch_listings(address, page_size)
    if listings:
        generate_csv(listings)
    else:
        print("No listings fetched.")

if __name__ == "__main__":
    address = "73 W Monroe St, Chicago, IL 60603, USA"
    page_size = 50
    main(address, page_size)
