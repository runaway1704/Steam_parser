import requests
from bs4 import BeautifulSoup
from summaries import get_buy_order_summary
from const import HEADERS

url = 'https://steamcommunity.com/market/search?q=&category_440_Collection%5B%5D=any' \
      '&category_440_Type%5B%5D=any' \
      '&category_440_Exterior%5B%5D=tag_TFUI_InvTooltip_FieldTested' \
      '&category_440_Exterior%5B%5D=tag_TFUI_InvTooltip_WellWorn' \
      '&category_440_Exterior%5B%5D=tag_TFUI_InvTooltip_MinimalWear' \
      '&category_440_Exterior%5B%5D=tag_TFUI_InvTooltip_FactoryNew' \
      '&category_440_Exterior%5B%5D=tag_TFUI_InvTooltip_BattleScared' \
      '&category_440_Quality%5B%5D=tag_Unique' \
      '&category_440_Quality%5B%5D=tag_paintkitweapon' \
      '&category_440_Quality%5B%5D=tag_strange' \
      '&category_440_Quality%5B%5D=tag_vintage' \
      '&category_440_Quality%5B%5D=tag_rarity1' \
      '&category_440_Quality%5B%5D=tag_rarity4' \
      '&category_440_Quality%5B%5D=tag_haunted' \
      '&category_440_Quality%5B%5D=tag_collectors' \
      '&category_440_Quality%5B%5D=tag_selfmade' \
      '&category_440_Quality%5B%5D=tag_Normal' \
      '&category_440_Rarity%5B%5D=tag_Rarity_Rare' \
      '&category_440_Rarity%5B%5D=tag_Rarity_Common' \
      '&category_440_Rarity%5B%5D=tag_Rarity_Mythical' \
      '&category_440_Rarity%5B%5D=tag_Rarity_Uncommon' \
      '&category_440_Rarity%5B%5D=tag_Rarity_Legendary' \
      '&category_440_Rarity%5B%5D=tag_Rarity_Ancient' \
      '&appid=440%27#p{}_popular_desc'


def get_html(path):
    response = requests.get(path, headers=HEADERS)
    return response


not_needed_items = ()


def get_content(html):
    soup = BeautifulSoup(html, "html.parser")
    items = soup.find_all("a", class_="market_listing_row_link")  # all "a" elements
    container = []
    for item in items:
        container.append({
            "name": item.find("span", class_="market_listing_item_name").get_text(strip=True),
            "price": item.find("span", class_="market_table_value normal_price").get_text(strip=True),
            "url": str(item.get("href")),
            "auto buy price": get_buy_order_summary(str(item.get("href")))
        })
    return container


def parse():
    items = []

    for i in range(1, 10):

        try:
            html = get_html(url.format(i))

            if html.status_code == 200:
                print(f"page {i} is processing...")
                items.extend(get_content(html.text))

        except Exception:

            return items

    return items


items = parse()
for item in items:
    if not any(i in item["name"] for i in not_needed_items):
        for key, value in item.items():
            print(key + " -> " + value)
        print("---------------------------------------------" * 3)
print(f"Returned {len(items)} items")
