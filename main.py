import requests
from bs4 import BeautifulSoup
from summaries import get_buy_order_summary

url = 'https://steamcommunity.com/market/search?q=&category_440_Collection%5B%5D=any&category_440_Type%5B%5D=any&category_440_Exterior%5B%5D=tag_TFUI_InvTooltip_FieldTested&category_440_Exterior%5B%5D=tag_TFUI_InvTooltip_WellWorn&category_440_Exterior%5B%5D=tag_TFUI_InvTooltip_MinimalWear&category_440_Exterior%5B%5D=tag_TFUI_InvTooltip_FactoryNew&category_440_Exterior%5B%5D=tag_TFUI_InvTooltip_BattleScared&category_440_Quality%5B%5D=tag_Unique&category_440_Quality%5B%5D=tag_paintkitweapon&category_440_Quality%5B%5D=tag_strange&category_440_Quality%5B%5D=tag_vintage&category_440_Quality%5B%5D=tag_rarity1&category_440_Quality%5B%5D=tag_rarity4&category_440_Quality%5B%5D=tag_haunted&category_440_Quality%5B%5D=tag_collectors&category_440_Quality%5B%5D=tag_selfmade&category_440_Quality%5B%5D=tag_Normal&category_440_Rarity%5B%5D=tag_Rarity_Rare&category_440_Rarity%5B%5D=tag_Rarity_Common&category_440_Rarity%5B%5D=tag_Rarity_Mythical&category_440_Rarity%5B%5D=tag_Rarity_Uncommon&category_440_Rarity%5B%5D=tag_Rarity_Legendary&category_440_Rarity%5B%5D=tag_Rarity_Ancient&appid=440'

headers = {
    'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36"
}


def get_html(path):
    response = requests.get(path, headers=headers)
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
            "url": str(item.get("href")),
            "auto buy price": get_buy_order_summary(str(item.get("href")))
        })
    for items in container:
        if not any(i in items["name"] for i in not_needed_items):
            for key, value in items.items():
                print(key + " -> " + value)
            print("---------------------------------------------" * 3)


def parse():
    html = get_html(url)
    get_content(html.text)


parse()
