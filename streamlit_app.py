import streamlit as st
import pandas as pd
import time

# サンプルデータ
def fetch_data():
    data = {
        "商品画像": ["https://images.stockx.com/images/adidas-Gazelle-Bold-Pink-Glow-W-Product.jpg"],
        "商品名": ["adidas Gazelle Bold W Pink Glow"],
        "サイズ": ["24.0cm"],
        "最高Bid価格（StockX）": ["¥18,000"],
        "最低Ask価格（StockX）": ["¥22,000"],
        "スニダン販売価格（仕入れ想定）": ["¥16,500"],
        "見込み利益": ["¥1,500"],
    }
    return pd.DataFrame(data)

# ページ設定
st.set_page_config(page_title="Sneaker Profit Checker", layout="wide")

# タイトル
st.title("Sneaker Profit Checker - v2 最終版")

# 更新ボタン
if st.button("手動更新（データ再取得）"):
    st.rerun()

# 自動更新
refresh_interval = 30  # 秒
countdown = st.empty()

# メイン表示
while True:
    df = fetch_data()

    # 商品画像と情報を横並びで表示
    for idx, row in df.iterrows():
        col1, col2 = st.columns([1, 3])
        with col1:
            st.image(row["商品画像"], width=150)
        with col2:
            st.write(f"**商品名：** {row['商品名']}")
            st.write(f"**サイズ：** {row['サイズ']}")
            st.write(f"**最高Bid価格（StockX）：** {row['最高Bid価格（StockX）']}")
            st.write(f"**最低Ask価格（StockX）：** {row['最低Ask価格（StockX）']}")
            st.write(f"**スニダン販売価格（仕入れ想定）：** {row['スニダン販売価格（仕入れ想定）']}")
            st.write(f"**見込み利益：** {row['見込み利益']}")

    # カウントダウン
    for seconds in range(refresh_interval, 0, -1):
        countdown.markdown(f"### 次回自動更新まで：{seconds}秒")
        time.sleep(1)

    # 更新！
    st.rerun()
