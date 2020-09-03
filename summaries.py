from bs4 import BeautifulSoup
import requests


def parse_item_name_id_from_script(last_script):
    last_script_token = last_script.split('(')[-1]

    item_nameid_str = last_script_token.split(');')[0]

    try:
        item_nameid = int(item_nameid_str)
    except ValueError:
        item_nameid = None

    return item_nameid


headers = {
    'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)"
                  " Chrome/83.0.4103.61 Safari/537.36"
}

# html = requests.get("https://steamcommunity.com/market/listings/440/Strange%20Panic%20Attack",
#                     headers=headers).text


def get_buy_order_summary(url):
    html = requests.get(url, headers=headers).text
    soup = BeautifulSoup(html, 'html.parser')
    script = str(soup.find_all("script")[-1])[31:-9]

    name_id = parse_item_name_id_from_script(last_script=script)

    data = requests.get(f"https://steamcommunity.com/market/"
                                    "itemordershistogram?"
                                    "country=UA"
                                    "&language=russian"
                                    "&currency=18"
                                    f"&item_nameid={name_id}&two_factor=0").json()

    buy_order_summary = data["buy_order_summary"][110:-7]

    return buy_order_summary
# count = 0
# f = 'Запросов на покупку: <span class="market_commodity_orders_header_promote">710</span><br>Начальная цена: <span'
# print(len(f))
# def parse_item_name_id(html_doc):
#     soup = BeautifulSoup(html_doc, 'html.parser')
#
#     a = str(soup.find_all('script')[-1])[31:]
#     print(a)
#     return None
#     # item_nameid = parse_item_name_id_from_script(last_script)
# print(str(scrept))
# b = str(scrept)[31:]
# script = b[:-9]

# if a == scrept:
#     print("cyc")
# utem = parse_item_name_id_from_script(script)
# print(utem)
# parse_item_name_id_from_script(html)

summaries = get_buy_order_summary("https://steamcommunity.com/market/listings/440/Strange%20Panic%20Attack")
print(summaries)