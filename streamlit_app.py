import streamlit as st
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import requests
from bs4 import BeautifulSoup
import time

# 商品情報
product_name = "adidas Originals Gazelle Bold 'Pink Glow/Victory Blue/Gum'"
stockx_url = "https://stockx.com/adidas-gazelle-bold-pink-glow-victory-blue-gum"
snkrdunk_url = "https://snkrdunk.com/products/30866393"

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
    except Exception as e:
        return None

# StockXからリアルタイム価格取得
def fetch_stockx_data(url):
    try:
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)
        driver.get(url)
        time.sleep(5)  # ページ読み込み待ち

        soup = BeautifulSoup(driver.page_source, "html.parser")
        driver.quit()

        data = []
        size_blocks = soup.find_all("div", {"class": "tile"})

        for block in size_blocks:
            size_tag = block.find("div", {"class": "tile-title"})
            price_tag = block.find("div", {"class": "tile-subtitle"})

            if size_tag and price_tag:
                size = size_tag.text.strip()
                price = price_tag.text.strip()
                data.append((size, price))

        return data
    except Exception as e:
        return []

# ページ構成
st.title(f"{product_name} リサーチツール")

# 商品画像表示
img_url = get_snkrdunk_image(snkrdunk_url)
if img_url:
    st.image(img_url, caption=product_name)
else:
    st.warning("商品画像を取得できませんでした。")

# StockXリンク
st.subheader("StockXリンク")
st.markdown(f"[StockXで見る]({stockx_url})")

# スニダンリンク
st.subheader("スニダンリンク")
st.markdown(f"[スニダンで見る]({snkrdunk_url})")

# 手動更新ボタン
if st.button("手動更新"):
    st.experimental_rerun()

# サイズ別リアルタイム価格一覧
st.subheader("サイズ別 リアルタイム価格")
stockx_data = fetch_stockx_data(stockx_url)

if stockx_data:
    for size, price in stockx_data:
        st.write(f"サイズ {size}：{price}")
else:
    st.warning("現在、StockX価格情報を取得できませんでした。")
