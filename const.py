import requests
from bs4 import BeautifulSoup


def get_dollar_rate():
    url = 'https://www.google.com/search?q=%D0%B4%D0%BE%D0%BB%D0%BB%D0%B0%D1%80' \
          '+%D0%BA+%D0%B3%D1%80%D0%B8%D0%B2%D0%BD%D0%B5&oq=%D0%B4%D0%BE%D0%BB%D0%BB%D0%B0%D1%80' \
          '+%D0%BA+&aqs=chrome.1.69i57j35i39j0l6.3263j1j7' \
          '&sourceid=chrome&ie=UTF-8'
    response = requests.get(url, headers=HEADERS).text
    soup = BeautifulSoup(response, 'html.parser')
    span_with_dollar_rate = soup.find_all("span", class_='DFlfde SwHCTb')[0].get_text(strip=True).replace(',', '.')
    dollar_rate = float(span_with_dollar_rate)
    return dollar_rate


HEADERS = {
    'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36"
}

DOLLAR_RATE = get_dollar_rate()

URL = "https://steamcommunity.com/market/search?q=&category_440_Collection%5B%5D=any&category_440_Type%5B%5D=any&category_440_Exterior%5B%5D=tag_TFUI_InvTooltip_FieldTested&category_440_Exterior%5B%5D=tag_TFUI_InvTooltip_WellWorn&category_440_Exterior%5B%5D=tag_TFUI_InvTooltip_MinimalWear&category_440_Exterior%5B%5D=tag_TFUI_InvTooltip_FactoryNew&category_440_Exterior%5B%5D=tag_TFUI_InvTooltip_BattleScared&category_440_Quality%5B%5D=tag_Unique&category_440_Quality%5B%5D=tag_paintkitweapon&category_440_Quality%5B%5D=tag_strange&category_440_Quality%5B%5D=tag_vintage&category_440_Quality%5B%5D=tag_rarity1&category_440_Quality%5B%5D=tag_rarity4&category_440_Quality%5B%5D=tag_haunted&category_440_Quality%5B%5D=tag_collectors&category_440_Quality%5B%5D=tag_selfmade&category_440_Quality%5B%5D=tag_Normal&category_440_Rarity%5B%5D=tag_Rarity_Rare&category_440_Rarity%5B%5D=tag_Rarity_Common&category_440_Rarity%5B%5D=tag_Rarity_Mythical&category_440_Rarity%5B%5D=tag_Rarity_Uncommon&category_440_Rarity%5B%5D=tag_Rarity_Legendary&category_440_Rarity%5B%5D=tag_Rarity_Ancient&appid=440%27#p9_popular_desc"
