import streamlit as st
import pandas as pd
import time

# タイトル
st.title("スニダン → StockX 利益リサーチ v2正式版")

# 入力欄
sku = st.text_input("品番（SKU）を入力してください", value="H06122")
stockx_url = st.text_input("StockXリンクを貼り付けてください")
snkrdunk_url = st.text_input("スニダンリンクを貼り付けてください")

# データ仮置き（今後スクレイピング/APIで自動化）
sizes = ['23.0', '23.5', '24.0', '24.5', '25.0']
stockx_bid_prices = [15000, 15200, 14800, 15100, 14900]
stockx_ask_prices = [15500, 15700, 15300, 15600, 15400]
snkrdunk_prices = [14000, 14200, 13800, 14100, 13900]

# スニダン手数料（ゴールド会員）
purchase_fee_rate = 0.055  # 5.5%
shipping_fee = 850 - 150    # 通常送料850円、ゴールド会員150円引き

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
        'StockX最高Bid': bid,
        'StockX最低Ask': ask,
        '想定利益（円）': int(profit),
        '利益率（%）': round(profit_rate, 1)
    })

df = pd.DataFrame(data)

# 表示
st.subheader("リサーチ結果")
st.dataframe(df)

# リンクボタン
st.markdown("---")
st.subheader("リンク一覧")

if stockx_url:
    st.markdown(f"[StockX商品ページへ移動]({stockx_url})", unsafe_allow_html=True)
if snkrdunk_url:
    st.markdown(f"[スニダン商品ページへ移動]({snkrdunk_url})", unsafe_allow_html=True)

# 手動更新ボタン
if st.button("手動で再読み込みする"):
    st.rerun()

# 自動更新（30秒）
st.experimental_set_query_params(dummy=str(time.time()))
time.sleep(30)
st.experimental_rerun()
