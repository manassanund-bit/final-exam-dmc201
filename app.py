import streamlit as st
import pandas as pd

# ตั้งค่าหน้าเว็บ
st.set_page_config(page_title="ประกาศที่นั่งสอบปลายภาค DMC 201 / DMR 201", page_icon="🎓", layout="centered")

# ปรับแต่งฟอนต์ Angsana New / Sarabun สไตล์เอกสารทางการที่โดดเด่น
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Sarabun:wght@400;600;700&display=swap');
    
    html, body, [class*="css"], div, span, p, h1, h2, h3, h4, input, button {
        font-family: 'Angsana New', 'Sarabun', sans-serif !important;
    }
    
    .header-box {
        background: linear-gradient(135deg, #1b2845, #274060, #335c67);
        color: white;
        padding: 28px 20px;
        border-radius: 16px;
        text-align: center;
        box-shadow: 0px 6px 18px rgba(0,0,0,0.18);
        margin-bottom: 20px;
        border-bottom: 5px solid #e09f3e;
    }
    
    .header-box h1 {
        color: #ffffff !important;
        font-size: 36px !important;
        font-weight: 700 !important;
        margin-bottom: 4px !important;
        line-height: 1.2 !important;
    }
    
    .header-box h3 {
        color: #ffea9f !important;
        font-size: 28px !important;
        font-weight: 600 !important;
        margin-top: 0px !important;
        margin-bottom: 8px !important;
    }

    .header-box p {
        color: #f0f4f8 !important;
        font-size: 23px !important;
        margin: 0 !important;
    }
    
    .exam-schedule-card {
        background-color: #f4f7f9;
        border-left: 6px solid #274060;
        padding: 15px 20px;
        border-radius: 10px;
        margin-bottom: 20px;
        color: #1b2845;
        font-size: 24px !important;
        line-height: 1.4 !important;
    }

    .stTextInput label p {
        font-size: 25px !important;
        font-weight: 700 !important;
        color: #1b2845 !important;
    }
    .stTextInput input {
        font-size: 24px !important;
    }
    [data-testid="stMetricValue"] {
        font-size: 34px !important;
        font-weight: 700 !important;
        color: #1b2845 !important;
    }
    [data-testid="stMetricLabel"] p {
        font-size: 22px !important;
        font-weight: 600 !important;
    }
    .stAlert p {
        font-size: 22px !important;
        line-height: 1.3 !important;
    }
    </style>
""", unsafe_allow_html=True)

# ส่วนหัวข้อประกาศ
st.markdown("""
    <div class="header-box">
        <h1>🎓 ประกาศรายชื่อผู้มีสิทธิ์สอบและเลขที่นั่งสอบปลายภาค</h1>
        <h3>รายวิชา DMC 201 / DMR 201 หลักการตลาด</h3>
        <p>ภาคเรียนที่ 1 ปีการศึกษา 2569</p>
    </div>
""", unsafe_allow_html=True)

# ส่วนแจ้งวันและเวลาสอบ
st.markdown("""
    <div class="exam-schedule-card">
        <b>📅 กำหนดการสอบ:</b> วันพุธที่ 9 ธันวาคม 2569  |  <b>⏰ เวลาสอบ:</b> 10.00 - 11.30 น.<br>
        <span style="font-size: 21px; color: #555;">💡 กรุณากรอกรหัสนักศึกษาด้านล่าง เพื่อตรวจสอบห้องสอบและเลขที่นั่งสอบส่วนบุคคล</span>
    </div>
""", unsafe_allow_html=True)

# Sheet ID และ GID ของแท็บสอบปลายภาค
GOOGLE_SHEET_ID = "1rLbcHIPuhffEZA6XhLGPxVUbwSqJh7ochpaKitdPjjQ"
SHEET_GID = "88059532"
SHEET_URL = f"https://docs.google.com/spreadsheets/d/{GOOGLE_SHEET_ID}/export?format=csv&gid={SHEET_GID}"

@st.cache_data(ttl=10)
def load_data():
    try:
        return pd.read_csv(SHEET_URL, dtype=str)
    except Exception as e:
        return None

df = load_data()

student_id = st.text_input("🔑 กรอกรหัสนักศึกษาของคุณ:", placeholder="เช่น 6900115")

if student_id:
    if df is not None and not df.empty:
        search_id = str(student_id).strip()
        
        # คอลัมน์ C (Index 2) คือ รหัสนักศึกษา
        df.iloc[:, 2] = df.iloc[:, 2].astype(str).str.strip()
        
        student_row = df[df.iloc[:, 2] == search_id]
        
        if not student_row.empty:
            row = student_row.iloc[0]
            
            # ดึงข้อมูลตามลำดับคอลัมน์ A-E
            exam_room = str(row.iloc[0]).strip() if pd.notna(row.iloc[0]) else "-"    # คอลัมน์ A: ห้องสอบ
            seat_no = str(row.iloc[1]).strip() if pd.notna(row.iloc[1]) else "-"      # คอลัมน์ B: เลขที่นั่งสอบ
            student_name = str(row.iloc[3]).strip() if pd.notna(row.iloc[3]) else "-" # คอลัมน์ D: ชื่อ-นามสกุล
            sec = str(row.iloc[4]).strip() if pd.notna(row.iloc[4]) else "-"          # คอลัมน์ E: SEC
            
            st.success(f"🔓 **พบข้อมูลผู้มีสิทธิ์เข้าสอบ:** {student_name}")
            st.divider()
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric(label="🏫 ห้องสอบ", value=f"{exam_room}")
            with col2:
                st.metric(label="🪑 เลขที่นั่งสอบ", value=f"{seat_no}")
            with col3:
                st.metric(label="📌 กลุ่มเรียน (SEC)", value=f"{sec}")
            
            st.warning("⚠️ **ข้อปฏิบัติในการเข้าสอบ:** กรุณาแต่งกายด้วยชุดนักศึกษาถูกต้องตามระเบียบมหาวิทยาลัย และแสดงบัตรนักศึกษาหรือบัตรประชาชนก่อนเข้าห้องสอบ")
        else:
            st.error(f"❌ ไม่พบรหัสนักศึกษา '{search_id}' ในรายชื่อผู้มีสิทธิ์สอบปลายภาควิชานี้")
    else:
        st.error("⚠️ ไม่สามารถเชื่อมต่อฐานข้อมูลได้ กรุณาตรวจสอบการตั้งค่าแชร์ Google Sheet ให้เป็น 'ทุกคนที่มีลิงก์'")
else:
    st.caption("ℹ️ ป้อนรหัสนักศึกษาของคุณในช่องด้านบน เพื่อค้นหาห้องสอบและเลขที่นั่งสอบ")
