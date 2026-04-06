import streamlit as st
import streamlit.components.v1 as components
import os

# 1. إعداد الصفحة (هادي ديريها مرة وحدة برك في الكود كامل)
st.set_page_config(page_title="EEG Smart Lab", layout="wide", initial_sidebar_state="collapsed")

# 2. دالة قراءة الملفات
def load_page(file_name):
    if os.path.exists(file_name):
        with open(file_name, 'r', encoding='utf-8') as f:
            return f.read()
    return f"<h3>Fichier {file_name} introuvable</h3>"

# 3. إدارة التنقل (Navigation)
if 'active_page' not in st.session_state:
    st.session_state.active_page = "welcome"

# 4. الـ Sidebar (نظفتو باش يجي باهي)
with st.sidebar:
    st.markdown("## 🎮 Menu")
    if st.button("🏠 Accueil", use_container_width=True):
        st.session_state.active_page = "welcome"
    if st.button("👤 Connexion", use_container_width=True):
        st.session_state.active_page = "login"
    if st.button("📊 Dashboard EEG", use_container_width=True):
        st.session_state.active_page = "dashboard"

# 5. عرض الصفحة المختارة (بدون تكرار)
page_to_load = f"{st.session_state.active_page}.html"
content = load_page(page_to_load)

# حقن CSS بسيط باش نحيو الفراغات الزايدة نتاع Streamlit
st.markdown("""
    <style>
    .block-container { padding-top: 0rem; padding-bottom: 0rem; }
    iframe { border: none; }
    </style>
""", unsafe_allow_html=True)

# عرض المحتوى
components.html(content, height=900, scrolling=True)
