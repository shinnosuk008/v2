import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd

# 商品情報
product_name = "adidas Originals Gazelle Bold 'Pink Glow/Victory Blue/Gum'"
stockx_url = "https://stockx.com/adidas-gazelle-bold-pink-glow-w"
snkrdunk_url = "https://snkrdunk.com/products/H06122"

# スニダンから商品画像取得
def get_snkrdunk_image(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
        img_tag = soup.find("img", {"class": "sc-9cysau-6 iLMVUj"})
        if img_tag:
            return img_tag.get("src")
        else:
            return None
    except Exception:
        return None

# StockXからリアルタイム価格（Bid/Ask）取得
def fetch_stockx_data(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
        size_boxes = soup.find_all("div", {"class": "tile"})
        data = []

        for box in size_boxes:
            size = box.find("div", {"class": "tile-size"}).text.strip()
            bid = box.find("div", {"class": "tile-bid"}).text.strip().replace("¥", "").replace(",", "")
            ask = box.find("div", {"class": "tile-ask"}).text.strip().replace("¥", "").replace(",", "")
            if bid.isdigit() and ask.isdigit():
                bid = int(bid)
                ask = int(ask)
                # スニダン手数料と送料差し引き後の利益計算（仮設定）
                purchase_price = ask * 1.055 + 1500  # スニダン購入手数料5.5%＋送料仮
                profit = bid - purchase_price
                profit_rate = profit / purchase_price * 100
                data.append({
                    "サイズ": size,
                    "最高入札（Bid）": bid,
                    "最低販売希望（Ask）": ask,
                    "利益（概算）": int(profit),
                    "利益率（概算）": f"{profit_rate:.1f}%"
                })

        df = pd.DataFrame(data)
        return df
    except Exception:
        return pd.DataFrame()

# Streamlit ページ構成
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

# サイズ別リスト表示
st.subheader("サイズ別 リアルタイム価格＆利益一覧")
data = fetch_stockx_data(stockx_url)
if not data.empty:
    st.dataframe(data)
else:
    st.warning("現在、StockX価格情報を取得できませんでした。")
