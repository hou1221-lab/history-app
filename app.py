import streamlit as st
import pandas as pd

# --- 1. 設定頁面 ---
st.set_page_config(page_title="中國歷史朝代時間軸", layout="wide")

# --- 2. 內建資料庫 (直接寫在程式裡，最穩定！) ---
# 之後你想新增人物，只要模仿格式加在下面的清單裡即可
if 'history_data' not in st.session_state:
    st.session_state.history_data = pd.DataFrame([
        {"name": "孔子", "dynasty": "東周", "year": -551, "type": "思想家", "note": "至聖先師，儒家創始人"},
        {"name": "秦始皇", "dynasty": "秦朝", "year": -259, "type": "君主", "note": "統一六國，築長城"},
        {"name": "漢武帝", "dynasty": "西漢", "year": -156, "type": "君主", "note": "罷黜百家，獨尊儒術"},
        {"name": "曹操", "dynasty": "三國", "year": 155, "type": "君主", "note": "魏國奠基者，一代梟雄"},
        {"name": "關羽", "dynasty": "三國", "year": 160, "type": "武將", "note": "武聖，義薄雲天"},
        {"name": "李白", "dynasty": "唐朝", "year": 701, "type": "詩人", "note": "詩仙，豪放不羈"},
        {"name": "朱元璋", "dynasty": "明朝", "year": 1328, "type": "君主", "note": "明朝開國皇帝"},
        {"name": "康熙", "dynasty": "清朝", "year": 1654, "type": "君主", "note": "開啟康雍乾盛世"}
    ])

df = st.session_state.history_data

# --- 3. 側邊欄：新增功能與篩選 ---
st.sidebar.header("🛠️ 動作選單")

# 新增人物的功能
with st.sidebar.expander("➕ 新增歷史人物"):
    new_name = st.text_input("姓名")
    new_dynasty = st.selectbox("朝代", ["東周", "秦朝", "西漢", "東漢", "三國", "晉朝", "隋朝", "唐朝", "宋朝", "元朝", "明朝", "清朝"])
    new_year = st.number_input("年份 (西元前請輸入負數)", value=2026)
    new_type = st.text_input("人物類型 (如：詩人、君主)")
    new_note = st.text_area("筆記")
    
    if st.button("確認新增"):
        new_row = {"name": new_name, "dynasty": new_dynasty, "year": new_year, "type": new_type, "note": new_note}
        st.session_state.history_data = pd.concat([st.session_state.history_data, pd.DataFrame([new_row])], ignore_index=True)
        st.rerun()

selected_dynasty = st.sidebar.selectbox("🔍 切換朝代檢視", ["全部總覽"] + list(df['dynasty'].unique()))

# --- 4. 主要畫面展示 ---
st.title("📜 中國歷史朝代時間軸程式")

if selected_dynasty == "全部總覽":
    st.subheader("我的歷史學習封面")
    # 這裡放一個簡單的模擬時間軸圖形
    st.info("💡 提示：點擊左側選單可以切換朝代，並看到該朝代的火柴人！")
    
    # 用進度條或簡單列表模擬時間軸順序
    sorted_df = df.sort_values(by="year")
    st.write("### ⏳ 歷史人物時間軸線")
    for index, row in sorted_df.iterrows():
        st.write(f"{row['year']}年 ➔ **{row['name']}** ({row['dynasty']})")

else:
    st.subheader(f"📍 {selected_dynasty} 的歷史人物")
    filtered_df = df[df['dynasty'] == selected_dynasty]
    
    if not filtered_df.empty:
        cols = st.columns(len(filtered_df))
        for i, row in enumerate(filtered_df.itertuples()):
            with cols[i]:
                st.markdown("### 🚶‍♂️")
                st.subheader(row.name)
                st.write(f"**身分：** {row.type}")
                st.caption(f"西元 {row.year} 年")
                if pd.notna(row.note):
                    st.info(row.note)
    else:
        st.write("目前這個朝代還沒有認識的人物喔！")

# --- 5. 資料檢視 (底部) ---
with st.expander("查看原始資料表"):
    st.table(df)
