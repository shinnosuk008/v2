import streamlit as st
import requests
from bs4 import BeautifulSoup

# 商品情報
stockx_url = "https://stockx.com/adidas-gazelle-bold-pink-glow-w"
snkrdunk_url = "https://snkrdunk.com/products/H06122?slide=right"

# StockXデータ取得
def get_stockx_data(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        bid = soup.select_one('div[data-testid="highest-bid"] span')
        ask = soup.select_one('div[data-testid="lowest-ask"] span')
        return bid.text if bid else "N/A", ask.text if ask else "N/A"
    except Exception as e:
        return "Error", "Error"

# スニダン画像取得
def get_snkrdunk_image(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        image = soup.find("img")
        return image["src"] if image else None
    except Exception as e:
        return None

# データ取得
stockx_bid, stockx_ask = get_stockx_data(stockx_url)
snkrdunk_image_url = get_snkrdunk_image(snkrdunk_url)

# UI表示
st.title("リアルタイム利益リサーチツール v2 完成版")
st.write("【対象モデル】 adidas Gazelle Bold 'Pink Glow'")

if snkrdunk_image_url:
    st.image(snkrdunk_image_url, caption="スニダン商品画像", use_column_width=True)
else:
    st.warning("商品画像が取得できませんでした")

st.subheader("StockX情報")
st.write(f"最高入札価格 (Bid): {stockx_bid}")
st.write(f"最低販売希望価格 (Ask): {stockx_ask}")

# 更新ボタン
if st.button("データを手動更新"):
    stockx_bid, stockx_ask = get_stockx_data(stockx_url)
    snkrdunk_image_url = get_snkrdunk_image(snkrdunk_url)
    st.rerun()
