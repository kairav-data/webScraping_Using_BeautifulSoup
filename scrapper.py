## importing library 
import requests
from bs4 import BeautifulSoup
import pandas as pd


headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'}

try:
    names = []
    prices = []
    ratings = []

    for i in range(1,5):
        baseurl='https://www.walmart.com/search?q=computer&page='
        url= baseurl + str(i)
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, "html.parser")

        product_elements = soup.find_all('div', class_='mb0 ph0-xl pt0-xl bb b--near-white w-25 pb3-m ph1')

        for product_desc in product_elements:
            
            ## Scraping product Name
            product_name = product_desc.find('span', class_='normal dark-gray mb0 mt1 lh-title f6 f5-l lh-copy')
            for name_desc in product_name:
                name=name_desc.text.strip()
                names.append(name)

            ## Scraping product Price
            price_elements = product_desc.find_all('span', class_='w_iUH7')
            for price_desc in price_elements:
                if 'price' in price_desc.text:
                    price_text = price_desc.text.split('$')[-1].strip()
                    prices.append(price_text)

            ## Scraping product Rating
            rating_elements = product_desc.find_all('span', class_='w_iUH7')
            for rating_desc in rating_elements:
                if 'Stars' in rating_desc.text:
                    # Get the text of the span element
                    rating_text = rating_desc.text.split(' ')[0].strip()
                    ratings.append(rating_text)  
        
    # print(len(names))    
    # print(len(prices))    
    # print(len(ratings))    
    df = pd.DataFrame({'Name': names, 'Price': prices, 'Rating': ratings})

    df.to_csv('products.csv', index=False)
    print("product.csv updated")

except Exception as e:
    print(e)
