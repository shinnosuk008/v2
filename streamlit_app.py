# streamlit_app.py

import streamlit as st
import time

st.set_page_config(page_title="あらた：スニーカー利益分析ツール v2", layout="centered")

# 更新用（強制再読み込み）
if st.button("更新", key="reload"):
    st.experimental_rerun()

st.title("あらた：スニーカー利益分析ツール v2")
st.caption(f"最終更新: {time.strftime('%Y-%m-%d %H:%M:%S')}")

st.header("対象モデル：adidas Women's Gazellebold 'Pink Glow/Victory Blue/Gum'")

# 【手動入力】価格情報
st.subheader("【手動入力】価格情報")

snkrdunk_sell_price = st.number_input("スニダン売値（手数料込み）", value=22000, step=100)
stockx_bid_price = st.number_input("StockX買取価格（Bid）", value=18000, step=100)
stockx_ask_price = st.number_input("StockX販売価格（Ask）", value=20000, step=100)

# 【利益シミュレーション】
st.subheader("【利益シミュレーション】")

snkrdunk_buy_price = st.number_input("スニダン仕入れ価格（円）", value=16000, step=100)

profit = snkrdunk_sell_price - snkrdunk_buy_price
profit_rate = (profit / snkrdunk_buy_price) * 100 if snkrdunk_buy_price else 0

st.metric(label="利益", value=f"¥{profit:,}")
st.metric(label="利益率", value=f"{profit_rate:.2f}%")

# 【販売履歴入力】
st.subheader("【販売履歴】")
sales_history_input = st.text_area("販売履歴を入力（例：2025/4/15 00:00 ¥18,000）")

# 表示
if sales_history_input:
    st.subheader("表示された販売履歴")
    for line in sales_history_input.splitlines():
        st.write(line)
