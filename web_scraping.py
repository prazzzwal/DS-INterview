

import requests
from bs4 import BeautifulSoup
import pandas as pd


url = 'https://books.toscrape.com/'

print(f"Scraping: {url}")

# Download the webpage
headers = {
    'User-Agent': 'Mozilla/5.0'   
}

response = requests.get(url, headers=headers, timeout=10)

# checking if the request was successful (200 = OK)
print(f"Status code: {response.status_code}")

if response.status_code != 200:
    print("Failed to fetch the page")
else:
    print("Page downloaded successfully!")


# parsing using beautifulsoup
soup = BeautifulSoup(response.text, 'html.parser')

# Find all book cards on the page
# Each book is inside an <article class="product_pod"> tag
all_books = soup.find_all('article', class_='product_pod')

print(f"\nFound {len(all_books)} books on the page")


#  Extracting data from each book card
books_data = []

for book in all_books:
    # Get book title (inside <h3><a title="...">)
    title = book.h3.a['title']

    # price (inside <p class="price_color">)
    price = book.find('p', class_='price_color').text.strip()

    # rating 
    rating_word = book.p['class'][1]   
    books_data.append({
        'title':  title,
        'price':  price,
        'rating': rating_word
    })


# Convert to DataFrame and export to CSV
df_books = pd.DataFrame(books_data)

print("\nFirst 5 scraped books:")
print(df_books.head())

df_books.to_csv('scraped_books.csv', index=False)
print(f"\nAll {len(df_books)} books saved to 'scraped_books.csv'")

