import time
import re
import requests
from bs4 import BeautifulSoup
from summaries import get_buy_order_summary, get_app_id, get_params
from const import HEADERS, URL, FROM_PAGE
import csv

if not FROM_PAGE:
    FROM_PAGE = 1
else:
    FROM_PAGE = int(FROM_PAGE)

if not URL.endswith("#p{}_popular_desc"):
    URL += "#p{}_popular_desc"

name_for_csv = time.strftime("%d-%m-%Y %Hh %M minutes")
now_time = time.time()


def get_html(path):
    response = requests.get(path, headers=HEADERS)
    return response


not_needed_items = ()


def get_content(html):
    soup = BeautifulSoup(html, "html.parser")
    items = soup.find_all("a", class_="market_listing_row_link")  # all "a" elements
    container = []
    pattern = re.compile(r'[0-9]+\.[0-9]+')
    for item in items:
        container.append({
            "name": item.find("span", class_="market_listing_item_name").get_text(strip=True),
            "price": str(pattern.findall(
                item.find("span", class_="market_table_value normal_price").get_text(strip=True).replace(',', ''))[0]),
            "url": str(item.get("href")),
            "auto buy price": get_buy_order_summary(str(item.get("href")))
        })
        time.sleep(10)
    return container


def save_into_csv(list_of_items):
    with open(f"{name_for_csv}.csv", "w", newline="", encoding='utf-8') as file:
        writer = csv.writer(file, delimiter=";")
        writer.writerow(["Name", "Price in $", "Url", "Auto buy price in $", "Profit"])
        # if not any(i in item["name"] for i in not_needed_items):
        for item in list_of_items:
            writer.writerow([item["name"], item["price"] + "$", item["url"], item["auto buy price"] + "$", str(
                round((float(item['price']) / float(item["auto buy price"]) - 1) * 100,
                      2)) + "%"])  # float(item["auto buy price"] / float(item['price']))
        return


def get_all_items_from_all_pages(html_page):
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


def parse(from_page=1, list_of_items=None):
    global items_from_all_pages
    try:
        items_from_all_pages = []
        if list_of_items is not None:
            items_from_all_pages.extend(list_of_items)
        html_page = requests.get(URL.format(1))
        if html_page.status_code == 200:
            last_page = int(get_all_items_from_all_pages(html_page.text)) // 100 + 1
        else:
            print("Try later")
            return
        app_id = get_app_id(URL)
        params = get_params(URL)
        for i in range(from_page, last_page + 1):
            try:
                start = i * 100 - 100
                response = requests.get(URL.format(i))
                if response.status_code == 200:
                    important_url = f"https://steamcommunity.com/market/search/render/?query=&start={start}&count=100&search_descriptions=0&sort_column=popular&sort_dir=desc{app_id}{params}"
                    res = requests.get(important_url)
                    if res.status_code == 200:
                        print(f"Page {i} of {last_page} is processing...")
                        items_from_all_pages.extend(get_content(res.json()["results_html"]))
                    else:
                        time.sleep(30)
                        return parse(from_page=i, list_of_items=items_from_all_pages)
            except Exception:
                # time.sleep(60)
                save_into_csv(items_from_all_pages)
                return
        save_into_csv(items_from_all_pages)
        return
    except KeyboardInterrupt:
        save_into_csv(items_from_all_pages)
        return


parse(from_page=FROM_PAGE)

# for item in items:
#     if not any(i in item["name"] for i in not_needed_items):
#         for key, value in item.items():
#             print(key + " -> " + value)
#         print("---------------------------------------------" * 3)
