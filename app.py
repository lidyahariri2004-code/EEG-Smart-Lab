import streamlit as st
import streamlit.components.v1 as components
import os

# إعداد الصفحة
st.set_page_config(page_title="EEG Smart Lab", layout="wide", initial_sidebar_state="collapsed")

# دالة لقراءة ملفات الـ HTML اللي رفعتيها
def load_page(file_name):
    if os.path.exists(file_name):
        with open(file_name, 'r', encoding='utf-8') as f:
            return f.read()
    return f"<h3>Fichier {file_name} introuvable</h3>"

# نظام التنقل (Navigation)
if 'active_page' not in st.session_state:
    st.session_state.active_page = "welcome"

# عرض الصفحة المطلوبة بناءً على الملفات اللي في GitHub
current_file = f"{st.session_state.active_page}.html"
html_content = load_page(current_file)

# تنظيف الفراغات نتاع Streamlit
st.markdown("<style>.block-container {padding: 0;}</style>", unsafe_allow_html=True)

# عرض المحتوى (هنا يظهر Welcome أو Dashboard)
components.html(html_content, height=1000, scrolling=True)

# أزرار بسيطة في الجنب للتنقل حتى نربطو الأزرار الداخلية
with st.sidebar:
    if st.button("Accueil"): st.session_state.active_page = "welcome"
    if st.button("Connexion"): st.session_state.active_page = "login"
    if st.button("Dashboard"): st.session_state.active_page = "dashboard"
