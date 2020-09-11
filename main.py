import time
import re
import requests
from bs4 import BeautifulSoup
from summaries import get_buy_order_summary
from const import HEADERS
import csv

print("""<------------------------------------------------------------------------------------->
You need to put url without %27#p_popular_desc
For example:
https://steamcommunity.com/market/search?appid=730
<------------------------------------------------------------------------------------->""")

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
      '&appid=440'

if not url.endswith("%27#p{}_popular_desc"):
    url += "%27#p{}_popular_desc"

name_for_csv = str(time.time())


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
        # time.sleep(10)
    return container


def save_into_csv(list_of_items):
    with open(f"{name_for_csv}.csv", "a", newline="") as file:
        writer = csv.writer(file, delimiter=";")
        writer.writerow(["Name", "Price", "Url", "Auto buy price"])
        for item in list_of_items:
            writer.writerow([item["name"], item["price"], item["url"], item["auto buy price"]])
        return


def get_all_pages(html_page):
    soup = BeautifulSoup(html_page, "html.parser")
    all_pages = soup.find_all("div", class_="market_paging_summary ellipsis")[0].get_text(strip=True)
    pattern = re.compile(r"[0-9]+")
    if "," in all_pages:
        pages_string = all_pages.replace(",", "")
        last_page = pattern.findall(pages_string)
        return last_page[-1]
    else:
        last_page = pattern.findall(all_pages)
        return last_page[-1]


def parse(from_page=1, list_of_items=None):  # from_page=1, last page=100

    items_from_all_pages = []
    if list_of_items is not None:
        items_from_all_pages.extend(list_of_items)

    html_page = get_html(url.format(1))
    if html_page.status_code == 200:
        last_page = int(get_all_pages(html_page.text)) // 10 + 1
    else:
        print("""Try later
        """)
        return

    for i in range(from_page, last_page + 1):
        try:
            html = get_html(url.format(i))
            if html.status_code == 200:
                print(f"page {i} of {last_page} is processing...")
                items_from_all_pages.extend(get_content(html.text))

        except Exception:

            time.sleep(300)
            return parse(from_page=i, list_of_items=items_from_all_pages)

    save_into_csv(items_from_all_pages)
    return


parse()

"""осталось протестить как меньше времени можно юзать"""

# items = parse()
# save_into_csv(items)
# for item in items:
#     if not any(i in item["name"] for i in not_needed_items):
#         for key, value in item.items():
#             print(key + " -> " + value)
#         print("---------------------------------------------" * 3)
