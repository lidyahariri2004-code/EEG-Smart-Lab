import streamlit as st
import streamlit.components.v1 as components
import os
import sqlite3

# إعداد الصفحة
st.set_page_config(page_title="EEG Smart Lab", layout="wide", initial_sidebar_state="collapsed")

# دالة لقراءة ملفات HTML نتاعك
def load_html(file_name):
    if os.path.exists(file_name):
        with open(file_name, 'r', encoding='utf-8') as f:
            return f.read()
    return f"<h3>Fichier {file_name} introuvable</h3>"

# نظام التنقل
if 'page' not in st.session_state:
    st.session_state.page = "welcome"

# --- القائمة الجانبية ---
with st.sidebar:
    st.title("Menu")
    if st.button("Accueil"): st.session_state.page = "welcome"
    if st.button("Connexion"): st.session_state.page = "login"
    if st.button("Dashboard"): st.session_state.page = "dashboard"

# --- عرض الصفحات ---
# ملاحظة: استعملي أسماء الملفات كما هي في GitHub (welcome.html, login.html...)
current_file = f"{st.session_state.page}.html"
html_content = load_html(current_file)

# تنظيف واجهة Streamlit باش يبان الـ HTML نتاعك برك
st.markdown("""<style>.block-container {padding: 0;}</style>""", unsafe_allow_html=True)

components.html(html_content, height=1000, scrolling=True)
