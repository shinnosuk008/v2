import streamlit as st
import pandas as pd
import time

# タイトル
st.title("現役利益チェッカー - v2 最終版（画像つき）")

# 入力欄
sku = st.text_input("品番（SKU）を入力してください")
stockx_url = st.text_input("StockXリンクを貼ってください")
snkrdunk_url = st.text_input("スニダンリンクを貼ってください")

# データ仮置き（今後スクレイピング/APIで自動化）
sizes = ['23.0', '23.5', '24.0', '24.5', '25.0']
stockx_bid_prices = [15000, 15200, 14800, 15500, 15300]
stockx_ask_prices = [15500, 15700, 15300, 16000, 15800]
snkrdunk_prices = [14000, 14200, 13800, 14100, 13900]

# スニダン手数料設定（ゴールド会員）
purchase_fee_rate = 0.055  # 5.5%
shipping_fee = 850 - 150   # 通常送料850円、ゴールド会員は150円引き

# 手動更新ボタン
if st.button("手動更新（データ再取得）"):
    st.rerun()

# 商品情報と画像表示
if sku and stockx_url and snkrdunk_url:
    st.image("https://static.snkrdunk.com/images/products/401378/main/standard.png", width=300)
    st.write(f"商品名 ： adidas Gazelle Bold W ピンクグロー")
    st.write(f"サイズ ： 24.0cm")
    st.write(f"最高入札価格（StockX） ： ¥18,000")
    st.write(f"最低アスク価格（StockX） ： ¥22,000")
    st.write(f"スニダン販売価格（仕入れ想定） ： ¥16,500")
    st.write(f"予想利益 ： 1,500円")

# DataFrame作成
data = []
for size, bid, ask, snk_price in zip(sizes, stockx_bid_prices, stockx_ask_prices, snkrdunk_prices):
    snk_total = snk_price * (1 + purchase_fee_rate) + shipping_fee
    profit = bid - snk_total
    profit_rate = profit / snk_total * 100
    data.append({
        'サイズ': size,
        'スニダン仕入れ価格': snk_price,
        'スニダン支払総額': int(snk_total),
        'StockX最高入札価格': bid,
        'StockX最低アスク価格': ask,
        '想定利益（最高入札）': int(profit),
        '利益率（最高入札）%': round(profit_rate, 1)
    })

# DataFrameを表示
df = pd.DataFrame(data)
st.subheader("調査結果")
st.dataframe(df)
