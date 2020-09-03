import requests
from bs4 import BeautifulSoup
import time
import os
from summaries import get_buy_order_summary

url = 'https://steamcommunity.com/market/search?appid=440'

headers = {
    'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36"
}


def get_html(url):
    response = requests.get(url, headers=headers)
    return response


def get_content(html):
    soup = BeautifulSoup(html, "html.parser")
    items = soup.find_all("a", class_="market_listing_row_link")
    not_needed_items = ()
    container = []
    for item in items:
        container.append({
            "name": item.find("span", class_="market_listing_item_name").get_text(strip=True),
            "price": item.find("span", class_="market_table_value normal_price").get_text(strip=True),
            "url": str(item.get("href"))
        })

    for i in container:
        print(get_buy_order_summary(i["url"]))

    for items in container:
        if not any(i in items["name"] for i in not_needed_items):
            for key, value in items.items():
                print(key + " -> " + value)
            print("---------------------------------------------" * 3)


def parse():
    html = get_html(url)
    os.system('cls||clear')
    get_content(html.text)


parse()
