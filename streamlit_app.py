import streamlit as st
import requests
from bs4 import BeautifulSoup

# 商品情報
product_name = "adidas Originals Gazelle Bold 'Pink Glow/Victory Blue/Gum'"
stockx_url = "https://stockx.com/adidas-gazelle-bold-pink-glow-victory-blue-gum"
snkrdunk_url = "https://snkrdunk.com/products/32222150"

# スニダンから画像取得
def get_snkrdunk_image(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
        img_tag = soup.find("img", {"class": "item-detail__main-img"})
        if img_tag:
            return img_tag.get("src")
        else:
            return None
    except Exception:
        return None

# StockXからBid/Ask取得
def fetch_stockx_data(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
        size_data = {}
        tables = soup.find_all("div", {"class": "css-1ca67uc"})  # サイズ・価格テーブル領域
        for table in tables:
            size = table.find("p", {"class": "chakra-text css-1q6lf6u"}).text.strip()
            price = table.find("div", {"class": "css-w0rmfk"}).text.strip()
            size_data[size] = price
        return size_data
    except Exception:
        return None

# ページ構成
st.title(f"{product_name} リサーチツール")

# 画像表示
img_url = get_snkrdunk_image(snkrdunk_url)
if img_url:
    st.image(img_url, caption=product_name)
else:
    st.warning("商品画像を取得できませんでした。")

# リンク表示
st.subheader("StockXリンク")
st.markdown(f"[StockXで見る]({stockx_url})")

st.subheader("スニダンリンク")
st.markdown(f"[スニダンで見る]({snkrdunk_url})")

# 手動更新ボタン
if st.button("手動更新"):
    st.rerun()

# サイズ別リアルタイム価格＆利益表示
st.subheader("サイズ別 リアルタイム価格＆利益一覧")

stockx_data = fetch_stockx_data(stockx_url)

if stockx_data:
    for size, price in stockx_data.items():
        st.write(f"サイズ {size}：{price}")
else:
    st.warning("現在、StockX価格情報を取得できませんでした。")
