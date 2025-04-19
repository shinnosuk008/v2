import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup

# 商品基本情報
product_name = "adidas Originals Gazelle Bold 'Pink Glow/Victory Blue/Gum'"
stockx_url = "https://stockx.com/adidas-gazelle-bold-pink-glow-w"
snkrdunk_url = "https://snkrdunk.com/products/H06122"

# スニダンから商品画像取得
def get_snkrdunk_image(url):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0"
        }
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, "html.parser")
        img_tag = soup.find("img", {"alt": product_name})
        if img_tag:
            return img_tag.get("src")
        else:
            return None
    except Exception:
        return None

# StockXからリアルタイムBid/Ask価格取得
def fetch_stockx_data(url):
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    try:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, "html.parser")
        size_boxes = soup.find_all("div", {"class": "tile"})

        data = []
        for box in size_boxes:
            size_tag = box.find("div", {"class": "tile-size"})
            bid_tag = box.find("div", {"class": "tile-bid"})
            ask_tag = box.find("div", {"class": "tile-ask"})

            if size_tag and bid_tag and ask_tag:
                size = size_tag.text.strip()
                bid = bid_tag.text.strip().replace("¥", "").replace(",", "")
                ask = ask_tag.text.strip().replace("¥", "").replace(",", "")

                if bid.isdigit() and ask.isdigit():
                    bid = int(bid)
                    ask = int(ask)
                    # スニダン購入時の手数料・送料加算（仮設定）
                    purchase_price = ask * 1.055 + 1500
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

# Streamlit画面構成
st.title(f"{product_name} リサーチツール")

# 商品画像表示
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

# サイズ別価格＆利益表
st.subheader("サイズ別 リアルタイム価格＆利益一覧")
data = fetch_stockx_data(stockx_url)
if not data.empty:
    st.dataframe(data)
else:
    st.warning("現在、StockX価格情報を取得できませんでした。")
