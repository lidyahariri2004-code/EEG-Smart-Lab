import streamlit as st
import streamlit.components.v1 as components
import os

# إعداد الصفحة
st.set_page_config(page_title="EEG Smart Lab", layout="wide")

# دالة ذكية تقرأ أي ملف HTML عندك في GitHub
def load_page(file_name):
    if os.path.exists(file_name):
        with open(file_name, 'r', encoding='utf-8') as f:
            return f.read()
    return f"<h3>Fichier {file_name} introuvable</h3>"

# نظام التنقل (Navigation)
if 'active_page' not in st.session_state:
    st.session_state.active_page = "welcome"

# --- القائمة الجانبية للتحكم ---
st.sidebar.title("🎮 Navigation")
if st.sidebar.button("🏠 Accueil"):
    st.session_state.active_page = "welcome"
    st.rerun()

if st.sidebar.button("👤 Connexion"):
    st.session_state.active_page = "login"
    st.rerun()

if st.sidebar.button("📊 Dashboard EEG"):
    st.session_state.active_page = "dashboard"
    st.rerun()

# --- عرض الصفحات ---
if st.session_state.active_page == "welcome":
    # يعرض الملف اللي شفتو في تصويرتك (welcome.html)
    content = load_page("welcome.html")
    components.html(content, height=1000, scrolling=True)

elif st.session_state.active_page == "login":
    # يعرض صفحة الدخول (login.html)
    content = load_page("login.html")
    components.html(content, height=1000, scrolling=True)

elif st.session_state.active_page == "dashboard":
    # يعرض الواجهة السوداء (dashboard.html)
    content = load_page("dashboard.html")
    components.html(content, height=1000, scrolling=True)
