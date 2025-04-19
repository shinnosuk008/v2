import streamlit as st
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time

# 商品情報
product_name = "adidas Originals Gazelle Bold 'Pink Glow/Victory Blue/Gum'"
stockx_url = "https://stockx.com/adidas-gazelle-bold-pink-glow-victory-blue-gum"
snkrdunk_url = "https://snkrdunk.com/products/adc-tzx8001"

# スニダンから商品画像を取得
def get_snkrdunk_image(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
        img_tag = soup.find("img", {"class": "ItemMainImages_item-main-images__image__XJjV9"})
        if img_tag:
            return img_tag.get("src")
        else:
            return None
    except Exception:
        return None

# StockXからリアルタイムBid/Ask情報を取得
def fetch_stockx_data(url):
    try:
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
        driver.get(url)
        time.sleep(5)  # ページ読み込み待ち

        page_source = driver.page_source
        soup = BeautifulSoup(page_source, "html.parser")

        bids = soup.find_all("div", {"class": "bid-ask-sizes"})
        driver.quit()

        size_price_list = []
        if bids:
            size_blocks = soup.find_all("div", {"class": "tile"})
            for block in size_blocks:
                size = block.find("div", {"class": "tile-title"}).text.strip() if block.find("div", {"class": "tile-title"}) else "-"
                price = block.find("div", {"class": "tile-subtitle"}).text.strip() if block.find("div", {"class": "tile-subtitle"}) else "-"
                size_price_list.append((size, price))
        return size_price_list

    except Exception:
        return []

# ページ構成
st.title(product_name + " リサーチツール")

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
    st.rerun()

# サイズ別リアルタイム価格＆利益一覧
st.subheader("サイズ別 リアルタイム価格＆利益一覧")
stockx_data = fetch_stockx_data(stockx_url)

if stockx_data:
    for size, price in stockx_data:
        st.write(f"サイズ: {size} ／ 価格: {price}")
else:
    st.warning("現在、StockX価格情報を取得できませんでした。")
