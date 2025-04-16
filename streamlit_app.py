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

st.success("まもなく自動更新機能を接続します！引き続きよろしくお願いします。")
