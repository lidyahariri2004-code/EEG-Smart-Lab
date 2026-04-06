import streamlit as st
import sqlite3
import pandas as pd
import numpy as np

# إعداد الصفحة
st.set_page_config(page_title="EEG Smart Lab", layout="wide")

# دالة لجلب البيانات من ملفك medical_system.db
def login_check(user, pwd, table):
    try:
        conn = sqlite3.connect('medical_system.db')
        cur = conn.cursor()
        cur.execute(f"SELECT * FROM {table} WHERE username=? AND password=?", (user, pwd))
        res = cur.fetchone()
        conn.close()
        return res
    except:
        return None

# --- واجهة الأزرار الثلاثة (بالستايل نتاعك) ---
st.markdown("<h1 style='text-align: center; color: #00f2ff;'>🧠 EEG SMART LAB</h1>", unsafe_allow_html=True)
st.write("---")

col1, col2, col3 = st.columns(3)
with col1:
    if st.button("👨‍⚕️ Espace DOCTOR", use_container_width=True):
        st.session_state['role'] = 'doctor'
with col2:
    if st.button("⚙️ Espace ADMIN", use_container_width=True):
        st.session_state['role'] = 'admin'
with col3:
    if st.button("👤 Espace PATIENT", use_container_width=True):
        st.session_state['role'] = 'patient'

# --- منطق تسجيل الدخول ---
if 'role' in st.session_state:
    st.sidebar.title(f"Login: {st.session_state['role']}")
    u = st.sidebar.text_input("Username")
    p = st.sidebar.text_input("Password", type="password")
    
    if st.sidebar.button("Se Connecter"):
        table_name = "doctor" if st.session_state['role'] == "doctor" else "patient"
        # إذا كان أدمين يدخل بـ admin/admin أو من القاعدة
        if (st.session_state['role'] == "admin" and u == "admin" and p == "admin") or login_check(u, p, table_name):
            st.session_state['user'] = u
            st.success(f"Bienvenue {u}!")
        else:
            st.error("Identifiants incorrects أو ملف .db غير موجود")

# --- واجهة الطبيب (الأوسيلوسكوب) ---
if 'user' in st.session_state and st.session_state['role'] == 'doctor':
    st.header("🔬 Oscilloscope en Temps Réel")
    file = st.file_uploader("Upload EEG Signal (.txt)", type=['txt'])
    if file:
        st.line_chart(np.random.randn(50, 1)) # محاكاة للإشارة
        st.error("🚨 Alerte: Crise Détectée!") # التنبيه الأحمر اللي تحبيه
