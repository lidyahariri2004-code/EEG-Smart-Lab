import streamlit as st
import streamlit.components.v1 as components
import os

# إعداد الصفحة لتكون بملء الشاشة
st.set_page_config(page_title="EEG Smart Lab", layout="wide")

# دالة لفتح ملفات الـ HTML التي رفعتها
def load_html(file_name):
    if os.path.exists(file_name):
        with open(file_name, 'r', encoding='utf-8') as f:
            return f.read()
    return f"<h3>Fichier {file_name} introuvable</h3>"

# نظام التنقل البسيط
if 'page' not in st.session_state:
    st.session_state.page = "welcome"

# عرض الملف بناءً على الصفحة الحالية
content = load_html(f"{st.session_state.page}.html")
components.html(content, height=1000, scrolling=True)

# أزرار تحكم مخفية للتنقل (اختياري)
if st.sidebar.button("Aller au Login"):
    st.session_state.page = "login"
    st.rerun()
