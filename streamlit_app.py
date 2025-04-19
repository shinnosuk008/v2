import streamlit as st
import requests
from bs4 import BeautifulSoup

# 商品情報
product_name = "adidas Originals Gazelle Bold 'Pink Glow/Victory Blue/Gum'"
stockx_url = "https://stockx.com/adidas-gazelle-bold-pink-glow-victory-blue-gum"
snkrdunk_url = "https://snkrdunk.com/products/30866393"

# スニダンから画像を取得
def get_snkrdunk_image(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
        img_tag = soup.find("img", {"class": "sc-87922daa-0 jxkKsu"})
        if img_tag:
            return img_tag.get("src")
        else:
            return None
    except Exception as e:
        return None

# StockXから価格データを取得
def fetch_stockx_data(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
        size_price_data = {}

        # サイズと価格情報をスクレイピング
        size_blocks = soup.find_all("div", {"class": "tile"})
        for block in size_blocks:
            size = block.find("div", {"class": "tile-title"}).text.strip()
            price = block.find("div", {"class": "tile-subtitle"}).text.strip()
            size_price_data[size] = price

        return size_price_data
    except Exception as e:
        return {}

# ページ構成
st.title(f"{product_name} リサーチツール")

# 商品画像表示
img_url = get_snkrdunk_image(snkrdunk_url)
if img_url:
    st.image(img_url, caption=product_name)
else:
    st.warning("商品画像を取得できませんでした。")

# StockXリンク表示
st.subheader("StockXリンク")
st.markdown(f"[StockXで見る]({stockx_url})")

# スニダンリンク表示
st.subheader("スニダンリンク")
st.markdown(f"[スニダンで見る]({snkrdunk_url})")

# 手動更新ボタン
if st.button("手動更新"):
    st.rerun()

# サイズ別価格表示
st.subheader("サイズ別 リアルタイム価格＆利益一覧")

stockx_data = fetch_stockx_data(stockx_url)

if stockx_data:
    for size, price in stockx_data.items():
        st.write(f"サイズ {size}： {price}")
else:
    st.warning("現在、StockX価格情報を取得できませんでした。")
