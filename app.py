import streamlit as st
import sqlite3
import pandas as pd
import numpy as np

# --- 1. دالة التحقق من الطبيب في القاعدة ---
def verify_doctor(username, password):
    try:
        conn = sqlite3.connect('medical_system.db')
        cur = conn.cursor()
        # هنا البحث في جدول الأطباء نتاعك
        cur.execute("SELECT * FROM doctor WHERE username=? AND password=?", (username, password))
        user_data = cur.fetchone()
        conn.close()
        return user_data
    except:
        return None

# --- 2. إدارة الحالة (Session State) ---
if 'auth_status' not in st.session_state:
    st.session_state['auth_status'] = False

# --- 3. واجهة تسجيل الدخول (الصفحة الأولى) ---
if not st.session_state['auth_status']:
    st.markdown("<h1 style='text-align: center; color: #00f2ff;'>🏥 تسجيل دخول الأطباء</h1>", unsafe_allow_html=True)
    
    with st.container():
        col1, col2, col3 = st.columns([1,2,1])
        with col2:
            u = st.text_input("اسم المستخدم (Doctor Username)")
            p = st.text_input("كلمة المرور", type="password")
            if st.button("تسجيل الدخول", use_container_width=True):
                check = verify_doctor(u, p)
                if check:
                    st.session_state['auth_status'] = True
                    st.session_state['dr_name'] = u
                    st.rerun() # إعادة التشغيل لفتح الواجهة الجديدة
                else:
                    st.error("❌ خطأ! الطبيب غير مسجل في قاعدة البيانات.")

# --- 4. الواجهة الثانية (تفتح فقط بعد الدخول الصحيح) ---
else:
    st.sidebar.success(f"مرحباً دكتور {st.session_state['dr_name']}")
    if st.sidebar.button("تسجيل الخروج"):
        st.session_state['auth_status'] = False
        st.rerun()

    st.title("🔬 واجهة تحليل إشارات EEG")
    st.write("---")
    
    # هنا نربطو المودال
    uploaded_file = st.file_uploader("ارفع ملف الإشارة (.txt) للتحليل بالمودال", type=['txt'])
    
    if uploaded_file:
        st.info("جاري معالجة الإشارة وتحويلها إلى Scalogram...")
        # رسم بياني يشبه الأوسيلوسكوب نتاعك
        chart_data = pd.DataFrame(np.random.randn(100, 1), columns=['EEG'])
        st.line_chart(chart_data)
        
        # التنبيه الأحمر في حال وجود صرع
        st.error("🚨 تنبيه: تم اكتشاف نوبة صرع (Seizure Detected)")
