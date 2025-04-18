import time
import streamlit as st
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

# スニダン・StockXのURLをここに
SNKR_URL = "https://snkrdunk.com/products/H06122"
STOCKX_URL = "https://stockx.com/adidas-gazelle-bold-pink-glow-w"

# Streamlitアプリタイトル
st.title("Sneaker Research Tool V2（最終版）")

# 手動更新ボタン
if st.button("最新データを取得（手動更新）"):

    # Seleniumセットアップ
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)

    try:
        # スニダンページ取得
        driver.get(SNKR_URL)
        time.sleep(2)

        # スニダンの商品画像取得
        snkr_image = driver.find_element(By.CSS_SELECTOR, "img.swiper-lazy").get_attribute("src")

        # スニダン価格取得
        snkr_price_text = driver.find_element(By.CLASS_NAME, "c-product__price").text
        snkr_price = int(''.join(filter(str.isdigit, snkr_price_text)))

        # StockXページ取得
        driver.get(STOCKX_URL)
        time.sleep(2)

        # StockXのBid（最高購入希望額）取得
        stockx_bid_text = driver.find_element(By.CLASS_NAME, "css-12whm1e").text
        stockx_bid = int(''.join(filter(str.isdigit, stockx_bid_text)))

        # スニダンの手数料・送料を考慮
        snkr_fee = int(snkr_price * 0.055)  # 5.5%
        snkr_shipping = 800  # 仮に800円と設定（※あとで調整可能）

        # 総仕入れ価格
        total_snkr_cost = snkr_price + snkr_fee + snkr_shipping

        # 利益計算
        profit = stockx_bid - total_snkr_cost

        # 画面に表示
        st.image(snkr_image, caption="スニダン商品画像", use_column_width=True)
        st.write(f"【スニダン価格】：¥{snkr_price:,}")
        st.write(f"【StockX最高Bid】：¥{stockx_bid:,}")
        st.write(f"【スニダン購入合計】：¥{total_snkr_cost:,}")
        st.success(f"【期待利益】：¥{profit:,}")

    except Exception as e:
        st.error(f"エラーが発生しました: {e}")

    finally:
        driver.quit()
