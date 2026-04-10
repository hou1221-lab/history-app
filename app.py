import streamlit as st
import pandas as pd

# 這是修正後的 Google Sheets CSV 下載網址
# 請直接複製這一行替換掉原本的 sheet_url
sheet_url = "https://docs.google.com/spreadsheets/d/1vWKvVc9ySyWY0au2gGTdnkNjZ3wsqAIRk_vD7wERbE/gviz/tq?tqx=out:csv"

st.set_page_config(page_title="我的歷史AI人物誌", layout="wide")

# 設定標題
st.title("📜 中國歷史朝代時間軸程式")
st.markdown("---")

# 讀取資料邏輯
try:
    # 讀取雲端試算表
    df = pd.read_csv(sheet_url)
    
    # 側邊欄：功能選單
    st.sidebar.header("🔍 歷史導覽")
    
    # 檢查資料表是否有朝代這欄
    if not df.empty and 'dynasty' in df.columns:
        dynasty_options = ["全部總覽"] + list(df['dynasty'].unique())
    else:
        dynasty_options = ["全部總覽"]

    selected = st.sidebar.selectbox("請選擇想查看的朝代", dynasty_options)
    
    # 畫面顯示
    if selected == "全部總覽":
        st.subheader("我的學習進度總覽")
        if df.empty:
            st.warning("目前資料庫是空的，請先在 Google 試算表中填入人物資料。")
        else:
            # 顯示原始資料表
            st.dataframe(df, use_container_width=True)
            st.write(f"目前已記錄 {len(df)} 位歷史人物。")
    else:
        st.subheader(f"📍 {selected} 的歷史人物")
        # 篩選出該朝代的人物
        filtered_df = df[df['dynasty'] == selected]
        
        if not filtered_df.empty:
            # 使用橫向欄位顯示火柴人（最多4欄）
            cols = st.columns(min(len(filtered_df), 4)) 
            for i, row in enumerate(filtered_df.itertuples()):
                with cols[i % 4]:
                    st.container()
                    st.markdown(f"### 🚶‍♂️ {row.name}")
                    st.write(f"**身分：** {row.type}")
                    # 顯示年份（如果有這欄）
                    if 'year' in df.columns:
                        st.caption(f"年份：西元 {row.year}")
                    # 顯示備註（如果有這欄）
                    if 'note' in df.columns and pd.notna(row.note):
                        st.info(row.note)
                    st.markdown("---")
        else:
            st.write("這個朝代暫時還沒有記錄。")

except Exception as e:
    st.error("讀取失敗！")
    st.info("請檢查：1. Google 試算表是否已開啟「知道連結的任何人均可查看」。 2. 欄位名稱是否包含 name, dynasty, type。")
    st.write(f"系統錯誤訊息：{e}")
