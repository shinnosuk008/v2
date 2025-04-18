import streamlit as st
import requests
from bs4 import BeautifulSoup
from datetime import datetime

st.set_page_config(page_title="スニダン × StockX リサーチツール", layout="wide")

# スニダンとStockXのURL
snkrdunk_url = "https://snkrdunk.com/products/H06122?slide=right"
stockx_url = "https://stockx.com/adidas-gazelle-bold-pink-glow-w"

# 商品画像を取得（スニダンから）
def get_snkrdunk_image(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        img_tag = soup.find("img", {"class": "product-showcase__img"})
        if img_tag and 'src' in img_tag.attrs:
            return img_tag['src']
    except Exception:
        return None
    return None

# StockX情報取得
def get_stockx_info(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        highest_bid = soup.find("div", {"data-testid": "highest-bid"}).text.strip()
        lowest_ask = soup.find("div", {"data-testid": "lowest-ask"}).text.strip()
        return highest_bid, lowest_ask
    except Exception:
        return None, None

# データ取得
image_url = get_snkrdunk_image(snkrdunk_url)
highest_bid, lowest_ask = get_stockx_info(stockx_url)

# 表示
st.title("スニダン仕入れ × StockX販売 リサーチツール")
st.caption("開発バージョン: v2-beta 最終版")

col1, col2 = st.columns(2)

with col1:
    st.header("スニーカーダンク")
    st.write(f"[スニダン商品ページへ移動]({snkrdunk_url})")
    if image_url:
        st.image(image_url, use_column_width=True)
    else:
        st.write("商品画像が取得できませんでした。")

with col2:
    st.header("StockX")
    st.write(f"[StockX商品ページへ移動]({stockx_url})")
    if highest_bid and lowest_ask:
        st.subheader("リアルタイム価格情報")
        st.metric(label="最高Bid（購入希望）", value=highest_bid)
        st.metric(label="最低Ask（販売希望）", value=lowest_ask)
    else:
        st.write("価格情報が取得できませんでした。")

# 手動更新ボタン
if st.button("データ更新（手動）"):
    st.rerun()

# タイムスタンプ表示
now = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
st.caption(f"最終データ更新: {now}")
