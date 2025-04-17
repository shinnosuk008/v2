import streamlit as st
import datetime

# ページ設定
st.set_page_config(page_title="あらた v2", layout="centered")

st.title("あらた：スニーカー利益分析ツール v2")
st.subheader("対象モデル：adidas Women's Gazellebold 'Pink Glow/Victory Blue/Gum'")
st.caption("最終更新: " + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

# ▼ スニダン vs StockX 比較（手入力）
st.header("【手動入力】価格情報")

st.subheader("スニダン売値（手数料込み）")
sundun_sell_price = st.number_input("スニダン売値（円）", value=22000)

st.subheader("StockX買取価格（Bid）")
stockx_bid_price = st.number_input("StockX 入札価格（Bid）", value=18000)

st.subheader("StockX販売価格（Ask）")
stockx_ask_price = st.number_input("StockX 出品価格（Ask）", value=20000)

# ▼ 利益計算
st.header("【利益シミュレーション】")

sundun_price = st.number_input("スニダン仕入れ価格（円）", value=16000)
sundun_fee = 0.1  # スニダン手数料10%

profit = stockx_bid_price * (1 - sundun_fee) - sundun_price
profit_rate = profit / sundun_price * 100 if sundun_price else 0

st.metric("利益", f"¥{profit:,.0f}")
st.metric("利益率", f"{profit_rate:.2f}%")

# ▼ 販売履歴入力（手動）
st.header("【販売履歴】")
history_raw = st.text_area("販売履歴を入力（例：2025/4/15 ¥18,000）", height=150)

# ▼ 入力内容の整理表示
st.subheader("表示された販売履歴")
if history_raw.strip():
    history_lines = history_raw.strip().split("\n")
    for line in history_lines:
        st.write("・" + line)

# ▼ 更新ボタン
st.divider()
if st.button("更新"):
    st.rerun()
