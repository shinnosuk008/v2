import streamlit as st
import datetime

# ページ設定
st.set_page_config(page_title="あらた v2", layout="centered")

# タイトル・サブヘッダー
st.title("あらた：スニーカー利益分析ツール v2")
st.subheader("対象モデル：adidas Women's Gazellebold 'Pink Glow/Victory Blue/Gum'")
st.caption("最終更新: " + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

st.info("このツールはスニダン×StockXの価格差を分析し、利益・利益率を自動計算します。")

# 機能リスト
st.write("**機能（今後の予定含む）**")
st.markdown("""
- 複数のサイズを一括表示  
- スニダン売値（手数料込み） × StockX買値（Bid/Ask）  
- 手動＆30秒自動更新ボタン  
- 利益金額・利益率表示（販売履歴あり）
""")

# ----------------------------
# 入力欄：手動価格入力エリア
# ----------------------------
st.header("現在の価格情報")

stockx_bid_price = st.number_input("StockX 買取（入札）価格", value=18000)
sundun_sell_price = st.number_input("スニダン売値（手数料込み）", value=22000)

# ----------------------------
# 利益シミュレーション（仮）
# ----------------------------
st.write("### 実際の価格＆利益シミュレーション（仮）")

sundun_price = st.number_input("スニダン販売価格（仮）", value=16000)
stockx_bid = st.number_input("StockX買取（仮）", value=13000)
sundun_fee = 0.1  # スニダン手数料10%

profit = stockx_bid * (1 - sundun_fee) - sundun_price
profit_rate = profit / sundun_price * 100 if sundun_price != 0 else 0

st.metric("利益", f"¥{profit:,.0f}")
st.metric("利益率", f"{profit_rate:.2f}%")

# ----------------------------
# 更新ボタン
# ----------------------------
if st.button("更新"):
    st.rerun()
