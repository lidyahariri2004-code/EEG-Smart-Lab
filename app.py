import streamlit as st
import sqlite3
import pandas as pd
import numpy as np
import streamlit.components.v1 as components

# --- إعدادات الصفحة ---
st.set_page_config(page_title="EEG Core AI", layout="wide")

# --- دالة للتعامل مع قاعدة البيانات ---
def get_db():
    conn = sqlite3.connect('medical_system.db')
    return conn

# --- إدارة حالة الجلسة (Session State) ---
if 'auth' not in st.session_state:
    st.session_state['auth'] = False
if 'page' not in st.session_state:
    st.session_state['page'] = 'login'

# --- 1. واجهة تسجيل الدخول والتسجيل (Login / Sign Up) ---
if not st.session_state['auth']:
    st.markdown("<h1 style='text-align:center; color:#00f2ff;'>👨‍⚕️ Espace Médecin</h1>", unsafe_allow_html=True)
    
    choice = st.radio("خيارات الوصول", ["تسجيل الدخول", "فتح حساب جديد (Sign Up)"], horizontal=True)

    if choice == "تسجيل الدخول":
        with st.form("login_form"):
            user = st.text_input("اسم المستخدم")
            pwd = st.text_input("كلمة المرور", type="password")
            submit = st.form_submit_button("دخول")
            if submit:
                conn = get_db()
                res = conn.execute("SELECT * FROM doctor WHERE username=? AND password=?", (user, pwd)).fetchone()
                conn.close()
                if res:
                    st.session_state['auth'] = True
                    st.session_state['user_name'] = user
                    st.rerun()
                else:
                    st.error("خطأ في البيانات أو الحساب غير موجود")

    else:  # واجهة الـ Sign Up (عمر الفورم كامل)
        with st.form("signup_form"):
            st.info("يرجى ملء كافة المعلومات للتسجيل في النظام")
            new_user = st.text_input("اسم المستخدم الجديد")
            new_pwd = st.text_input("كلمة المرور", type="password")
            full_name = st.text_input("الاسم الكامل")
            specialty = st.text_input("التخصص الطبي")
            submit_signup = st.form_submit_button("إنشاء الحساب")
            
            if submit_signup:
                try:
                    conn = get_db()
                    conn.execute("INSERT INTO doctor (username, password, name, specialty) VALUES (?,?,?,?)", 
                                 (new_user, new_pwd, full_name, specialty))
                    conn.commit()
                    conn.close()
                    st.success("تم التسجيل بنجاح! يمكنك الآن تسجيل الدخول.")
                except:
                    st.error("حدث خطأ (ربما اسم المستخدم موجود مسبقاً)")

# --- 2. الواجهة الاحترافية (بعد نجاح الدخول) ---
else:
    # هنا نحطو كود الـ HTML اللي بعثتيهولي (الأسود والنيون)
    # ملاحظة: نستخدم st.components.v1.html لعرض تصميمك كما هو
    
    html_dashboard = f"""
    <style>
        :root {{ --bg-deep: #020406; --neon-blue: #00f2ff; }}
        body {{ background-color: #020406; color: white; font-family: 'Segoe UI'; }}
        .header {{ padding: 20px; border-bottom: 1px solid #161b22; display: flex; justify-content: space-between; }}
        .monitor {{ border: 2px solid #333; height: 400px; border-radius: 10px; margin-top: 20px; }}
    </style>
    <div class="header">
        <h2>🧠 EEG AI SYSTEM - Monitor</h2>
        <div style="color: #00f2ff;">Bienvenue, Dr. {st.session_state['user_name']}</div>
    </div>
    <div class="monitor">
        <h4 style="text-align:center; padding-top: 150px; color: #444;">L'oscilloscope est prêt...</h4>
    </div>
    """
    
    components.html(html_dashboard, height=600)
    
    # أزرار التحكم نتاع Streamlit
    st.sidebar.button("Déconnexion", on_click=lambda: st.session_state.update({'auth': False}))
    uploaded_file = st.file_uploader("Ajouter Séquence EEG", type=['txt'])
    if uploaded_file:
        st.line_chart(np.random.randn(50, 1))
        st.success("Analyse en cours...")
