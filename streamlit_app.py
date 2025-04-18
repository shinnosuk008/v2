import streamlit as st
import requests
from bs4 import BeautifulSoup

# StockXとスニダンの商品ページURL
stockx_url = "https://stockx.com/adidas-gazelle-bold-pink-glow-w"
snkrdunk_url = "https://snkrdunk.com/products/H06122?slide=right"

# ページ情報取得用関数
def fetch_stockx_price(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        price_element = soup.find("div", class_="css-1bqj4bj")  # 最低価格の部分
        if price_element:
            return price_element.text.strip()
        else:
            return "価格情報が見つかりません"
    except Exception as e:
        return f"エラー: {e}"

def fetch_snkrdunk_info(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        # 商品画像を取得
        img_element = soup.find("img")
        img_url = img_element["src"] if img_element else ""

        # 価格情報取得（仮）
        price_element = soup.find("div", class_="l-right-column__main-price")
        if price_element:
            price_text = price_element.text.strip()
        else:
            price_text = "価格情報なし"

        return img_url, price_text
    except Exception as e:
        return "", f"エラー: {e}"

# Streamlitアプリ開始
st.title("v2 スニダン × StockX 手動更新版")

# 手動更新ボタン
if st.button("手動更新"):
    stockx_price = fetch_stockx_price(stockx_url)
    snkrdunk_img_url, snkrdunk_price = fetch_snkrdunk_info(snkrdunk_url)

    st.subheader("StockX 最低価格")
    st.write(stockx_price)

    st.subheader("スニダン情報")
    if snkrdunk_img_url:
        st.image(snkrdunk_img_url, width=300)
    else:
        st.write("画像が見つかりませんでした。")
    st.write(f"スニダン価格: {snkrdunk_price}")
else:
    st.info("「手動更新」ボタンを押して、情報を取得してください。")
