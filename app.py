import streamlit as st
import streamlit.components.v1 as components
import sqlite3
import pandas as pd

# 1. إعدادات الصفحة وستايل النيون نتاعك
st.set_page_config(page_title="EEG Core AI", layout="wide")

# 2. دالة الاتصال بقاعدة البيانات نتاعك
def check_user(username, password, table):
    try:
        conn = sqlite3.connect('medical_system.db')
        cursor = conn.cursor()
        query = f"SELECT * FROM {table} WHERE username=? AND password=?"
        cursor.execute(query, (username, password))
        result = cursor.fetchone()
        conn.close()
        return result
    except:
        return None

# 3. عرض الواجهة اللي فيها 3 أزرار (باستعمال HTML نتاعك)
html_header = """
<div style="text-align:center; background-color:#020406; padding:20px; border-radius:15px; border:1px solid #00f2ff;">
    <h1 style="color:#00f2ff; font-family:sans-serif; letter-spacing:3px;">🧠 EEG SMART LAB</h1>
    <p style="color:#e2e8f0;">Système de Surveillance Intelligente</p>
</div>
"""
st.markdown(html_header, unsafe_allow_unsafe_allow_html=True)

# 4. نظام الدخول (الأزرار الثلاثة)
st.write("##")
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("👨‍⚕️ Espace DOCTOR"):
        st.session_state['mode'] = 'doctor'
with col2:
    if st.button("⚙️ Espace ADMIN"):
        st.session_state['mode'] = 'admin'
with col3:
    if st.button("👤 Espace PATIENT"):
        st.session_state['mode'] = 'patient'

# 5. منطق تسجيل الدخول الفعلي
if 'mode' in st.session_state:
    mode = st.session_state['mode']
    st.sidebar.info(f"تسجيل الدخول: {mode}")
    user = st.sidebar.text_input("اسم المستخدم")
    pwd = st.sidebar.text_input("كلمة المرور", type="password")
    
    if st.sidebar.button("دخول"):
        table = "doctor" if mode == "doctor" else "patient" if mode == "patient" else "admin"
        # التحقق من قاعدة البيانات medical_system.db
        auth = check_user(user, pwd, table)
        
        if auth or (user == "admin" and pwd == "admin"): # دخول احتياطي للأدمين
            st.sidebar.success(f"تم الدخول بنجاح يا {user}")
            st.session_state['authenticated'] = True
        else:
            st.sidebar.error("بيانات خاطئة أو ملف القاعدة غير موجود")

# 6. إذا دخل الطبيب، تظهر واجهة الأوسيلوسكوب نتاعك
if st.session_state.get('authenticated') and st.session_state.get('mode') == 'doctor':
    st.write("---")
    st.subheader("🔬 OSCILLOSCOPE TEMPS RÉEL")
    uploaded_file = st.file_uploader("تحميل إشارة EEG", type=['txt'])
    if uploaded_file:
        st.success("تم استقبال الإشارة. جاري التحليل بالمودال...")
        # هنا نعرضوا الـ Chart نتاع Streamlit اللي يشبه نتاعك
        chart_data = pd.DataFrame(np.random.randn(20, 1), columns=['EEG Signal'])
        st.line_chart(chart_data)
