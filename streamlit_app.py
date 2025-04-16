import streamlit as st
import datetime

st.set_page_config(page_title="あらた v2", layout="wide")

st.title("あらた：スニーカー利益分析ツール v2")
st.subheader("対象モデル：adidas Women's Gazellebold 'Pink Glow/Victory Blue/Gum'")
st.caption("最終更新: " + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

st.info("このツールはスニダン×StockXの価格差を分析し、利益・利益率を自動算出します。")

st.write("**機能（今後の予定含む）**")
st.markdown("""
- 複数サイズを一括表示
- スニダン売値（手数料込み）× StockX買値（Bid/Ask）
- 手動＆30秒自動更新ボタン
- 利益額・利益率表示（販売履歴あり）
""")

# 仮データ（本来はAPIなどから取得する想定）
stockx_bid_price = 18000
sudansell_price = 22000

# 表示
st.header("現在の価格情報")
st.metric(label="StockX 買値（Bid）", value=f"¥{stockx_bid_price:,}")
st.metric(label="スニダン 売値（手数料込）", value=f"¥{sudansell_price:,}")st.success("まもなく自動更新機能を接続します！引き続きよろしくお願いします。")
# --- 仮データでの価格と利益表示（本番では自動取得に変更予定） ---
sundun_price = 16000  # スニダン売値（仮）
stockx_bid = 13000     # StockX Bid（仮）

# 手数料引いた利益計算（スニダン手数料：10%で仮定）
sundun_fee = 0.1
profit = stockx_bid * (1 - sundun_fee) - sundun_price
profit_rate = profit / sundun_price * 100

st.write("### 実際の価格＆利益シミュレーション（仮）")
st.metric("スニダン売値", f"¥{sundun_price:,}")
st.metric("StockX 買取（Bid）", f"¥{stockx_bid:,}")
st.metric("利益", f"¥{profit:,}")
st.metric("利益率", f"{profit_rate:.2f}%")
