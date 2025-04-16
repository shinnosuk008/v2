import streamlit as st
import datetime
import time  # 自動更新用

# ページ設定
st.set_page_config(page_title="あらた v2", layout="wide")

# 自動更新（30秒ごとに再実行）
st.experimental_set_query_params(_=str(int(time.time() // 30)))

# ヘッダー
st.title("あらた：スニーカー利益分析ツール v2")
st.subheader("対象モデル：adidas Women's Gazellebold 'Pink Glow/Victory Blue/Gum'")
st.caption("最終更新: " + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
st.info("このツールはスニダン×StockXの価格差を分析し、利益・利益率を自動計算します。")

# 今後の予定
st.write("**機能（今後の予定含む）**")
st.markdown("""
- 複数サイズを一括表示  
- スニダン売値（手数料込み）× StockX買値（Bid/Ask）  
- 手動＆30秒自動更新ボタン  
- 利益金額・利益率表示（販売履歴あり）  
""")

# 仮データ（本来はAPIで取得）
stockx_bid_price = 18000
sundun_sell_price = 22000

# 表示（仮データ）
st.header("現在の価格情報")
st.metric(label="StockX 買取（Bid）", value=f"¥{stockx_bid_price:,}")
st.metric(label="スニダン 売値（手数料込）", value=f"¥{sundun_sell_price:,}")

# 利益シミュレーション
st.write("### 実際の価格＆利益シミュレーション（仮）")
sundun_price = 16000  # 仮の売値
stockx_bid = 13000    # 仮のBid
sundun_fee = 0.1       # スニダン手数料10%
profit = stockx_bid * (1 - sundun_fee) - sundun_price
profit_rate = profit / sundun_price * 100

st.metric("スニダン売値", f"¥{sundun_price:,}")
st.metric("StockX 買取（Bid）", f"¥{stockx_bid:,}")
st.metric("利益", f"¥{profit:,.0f}")
st.metric("利益率", f"{profit_rate:.2f}%")

# 手動更新ボタン
st.divider()
if st.button("手動で更新する"):
    st.experimental_rerun()
