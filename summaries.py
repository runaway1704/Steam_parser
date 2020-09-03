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

dollar_rate = 27.70


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
