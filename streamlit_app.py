import streamlit as st
import pandas as pd
import time

# タイトル
st.title("スニーカー利益チェッカー - v2 最終版")

# 入力欄
sku = st.text_input("品番（SKU）を入力してください")
stockx_url = st.text_input("StockXリンクを貼ってください")
snkrdunk_url = st.text_input("スニダンリンクを貼ってください")

# データ仮置き
sizes = ['23.0', '23.5', '24.0', '24.5', '25.0']
stockx_bid_prices = [15000, 15200, 14800, 15300, 15000]
stockx_ask_prices = [15500, 15700, 15300, 15800, 15500]
snkrdunk_prices = [14000, 14200, 13800, 14100, 13900]

# スニダン手数料 (ゴールド会員)
purchase_fee_rate = 0.055  # 5.5%
shipping_fee = 850 - 150  # 通常送料850円から150円引き

# DataFrame作成
data = []
for size, bid, ask, snk_price in zip(sizes, stockx_bid_prices, stockx_ask_prices, snkrdunk_prices):
    snk_total = snk_price * (1 + purchase_fee_rate) + shipping_fee
    profit = bid - snk_total
    profit_rate = profit / snk_total * 100
    data.append({
        "サイズ": size,
        "スニダン仕入れ価格": snk_price,
        "スニダン支払総額": int(snk_total),
        "StockX最高入札": bid,
        "StockX最低アスク": ask,
        "予想利益": int(profit),
        "利益率(%)": round(profit_rate, 2)
    })

df = pd.DataFrame(data)

# 表示
st.write("調査結果")
st.dataframe(df)

# 商品画像とリンク
if snkrdunk_url:
    st.image("https://static.snkrdunk.com/images/products/1000x1000/default.jpg", width=300)  # 仮画像
    st.markdown(f"[スニダン商品ページへ]({snkrdunk_url})")

# 自動更新（30秒）
time.sleep(30)
st.rerun()
