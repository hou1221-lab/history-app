import streamlit as st
import pandas as pd

# --- 1. 頁面設定 ---
st.set_page_config(page_title="中國歷史朝代時間軸", layout="wide")

# --- 2. 初始資料庫 ---
if 'history_data' not in st.session_state:
    st.session_state.history_data = pd.DataFrame([
        {"name": "孔子", "dynasty": "東周", "year": -551, "type": "思想家"},
        {"name": "秦始皇", "dynasty": "秦朝", "year": -259, "type": "君主"},
        {"name": "漢武帝", "dynasty": "西漢", "year": -156, "type": "君主"},
        {"name": "曹操", "dynasty": "三國", "year": 155, "type": "君主"},
        {"name": "李白", "dynasty": "唐朝", "year": 701, "type": "詩人"},
        {"name": "朱元璋", "dynasty": "明朝", "year": 1328, "type": "君主"},
        {"name": "康熙", "dynasty": "清朝", "year": 1654, "type": "君主"}
    ])

# --- 3. 側邊欄 ---
st.sidebar.title("📚 歷史小助手")
selected_dynasty = st.sidebar.selectbox("🗺️ 選擇檢視範圍", ["首頁：歷史時間軸封面", "東周", "秦朝", "西漢", "三國", "唐朝", "明朝", "清朝"])

# 新增功能
with st.sidebar.expander("👤 新增認識的人物"):
    add_name = st.text_input("姓名")
    add_dyn = st.selectbox("所屬朝代", ["東周", "秦朝", "西漢", "三國", "唐朝", "明朝", "清朝"])
    add_year = st.number_input("年份", value=0)
    if st.button("點擊新增火柴人"):
        new_person = {"name": add_name, "dynasty": add_dyn, "year": add_year, "type": "新學習"}
        st.session_state.history_data = pd.concat([st.session_state.history_data, pd.DataFrame([new_person])], ignore_index=True)
        st.success(f"已將 {add_name} 加入 {add_dyn}！")
        st.rerun()

# --- 4. 主要畫面邏輯 ---

if selected_dynasty == "首頁：歷史時間軸封面":
    # 顯示你在 GitHub 上傳的那張圖
    st.title("📜 中國歷史朝代時間軸程式")
    
    # 這裡是我幫你組合好的正確圖片路徑 (hou1221-lab + history-app + cover.jpg)
    image_url = "https://raw.githubusercontent.com/hou1221-lab/history-app/main/cover.jpg"
    
    # 用最直接的方式顯示圖片
    st.image(image_url, use_container_width=True)
    st.info("💡 點擊左側選單選擇朝代，查看詳細的火柴人人物誌！")

else:
    # 進入特定朝代的頁面
    st.title(f"📍 {selected_dynasty} 英雄榜")
    df = st.session_state.history_data
    filtered_df = df[df['dynasty'] == selected_dynasty]
    
    if not filtered_df.empty:
        # 顯示卡片
        cols = st.columns(min(len(filtered_df), 4))
        for i, row in enumerate(filtered_df.itertuples()):
            with cols[i % 4]:
                st.markdown(f"""
                <div style="border:2px solid #ddd; padding:20px; border-radius:10px; text-align:center; background-color:#f9f9f9; margin-bottom:10px;">
                    <h1 style="margin:0;">🚶‍♂️</h1>
                    <h2 style="color:#333;">{row.name}</h2>
                    <p style="color:#666; margin:0;">西元 {row.year} 年</p>
                    <small>{row.type}</small>
                </div>
                """, unsafe_allow_html=True)
    else:
        st.write("這個朝代暫時還沒有火柴人，快去左邊新增一個吧！")
