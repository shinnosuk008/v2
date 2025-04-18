import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup

# タイトル
st.title("慎之介's Gazellebold リサーチツール")

# 手動更新ボタン
refresh = st.button('手動更新')

# 本番用StockXページURL
stockx_url = "https://stockx.com/adidas-gazelle-bold-pink-glow-w"

# サイズリスト
sizes = ['22.0', '22.5', '23.0', '23.5', '24.0', '24.5', '25.0', '25.5', '26.0']

# データ取得関数
def fetch_stockx_data(url):
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")

    bid_prices = []
    ask_prices = []
    sale_histories = []

    for size in sizes:
        # 仮のスクレイピング（StockXのページ構成で後日微修正する）
        bid = soup.find('div', class_="bid-amount")
        bid_price = bid.text.strip() if bid else "取得失敗"
        bid_prices.append(bid_price)

        ask = soup.find('div', class_="ask-amount")
        ask_price = ask.text.strip() if ask else "取得失敗"
        ask_prices.append(ask_price)

        history = soup.find('div', class_="sale-amount")
        sale_price = history.text.strip() if history else "取得失敗"
        sale_histories.append(sale_price)

    df = pd.DataFrame({
        "サイズ": sizes,
        "Bid価格": bid_prices,
        "Ask価格": ask_prices,
        "販売履歴": sale_histories
    })

    return df

# 初回データ取得（ページロード時）
data = fetch_stockx_data(stockx_url)
data_placeholder = st.empty()
data_placeholder.dataframe(data)

# 手動更新ボタン押下時
if refresh:
    data = fetch_stockx_data(stockx_url)
    data_placeholder.dataframe(data)
