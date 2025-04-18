import streamlit as st
import requests
from bs4 import BeautifulSoup

# 商品情報
product_name = "adidas Originals Gazelle Bold 'Pink Glow/Victory Blue/Gum'"
stockx_url = "https://stockx.com/adidas-gazelle-bold-pink-glow-w"
snkrdunk_url = "https://snkrdunk.com/products/H06122"

# スニダンから画像を取得
def get_snkrdunk_image(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
        img_tag = soup.find("img", {"class": "item-detail__item-img"})
        if img_tag:
            return img_tag.get("src")
        else:
            return None
    except Exception as e:
        return None

# ページ構成
st.title("商品情報")

# 商品名表示
st.header(product_name)

# 画像表示
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
