from bs4 import BeautifulSoup
import requests
import re
from const import HEADERS, DOLLAR_RATE
import time


def parse_item_name_id_from_script(last_script):
    last_script_token = last_script.split('(')[-1]

    item_nameid_str = last_script_token.split(');')[0]

    try:
        item_nameid = int(item_nameid_str)
    except ValueError:
        item_nameid = None

    return item_nameid


def get_buy_order_summary(url):
    html = requests.get(url, headers=HEADERS)
    if html.status_code != 200:
        time.sleep(10)
        return get_buy_order_summary(url)
    soup = BeautifulSoup(html.text, 'html.parser')
    script = str(soup.find_all("script")[-1])[31:-9]

    name_id = parse_item_name_id_from_script(last_script=script)

    data = requests.get(f"https://steamcommunity.com/market/"
                        "itemordershistogram?"
                        "country=UA"
                        "&language=russian"
                        "&currency=18"
                        f"&item_nameid={name_id}&two_factor=0").json()

    buy_order_summary = data["buy_order_summary"]  # [110:-7]  # string with auto buy price data
    if "," in buy_order_summary:
        pattern = re.compile(r'[0-9]+\.[0-9]+')
        buy_order_summary = buy_order_summary.replace(",", ".").replace(" ", "")
        price = float(pattern.findall(buy_order_summary)[0])
        auto_buy_price = round(price / DOLLAR_RATE, 2)  # convert into dollars
        return f"{auto_buy_price}"

    else:
        pattern = re.compile(r"[0-9]+")
        price = float(int(pattern.findall(buy_order_summary)[0]))
        auto_buy_price = round(price / DOLLAR_RATE, 2)
        return f"{auto_buy_price}"


def get_app_id(url):
    last_element = url.rfind("&")
    app_id_with_page_number = url[last_element:]
    not_needed_part_of_string = app_id_with_page_number.rfind("#")
    app_id = app_id_with_page_number[:not_needed_part_of_string]
    return app_id.strip()


def get_params(url):
    last_element = url.rfind("&")
    index_of_equals = url.find("=")
    params = url[index_of_equals + 1:last_element].strip()
    return params
