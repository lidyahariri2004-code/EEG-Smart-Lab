import streamlit as st
import sqlite3
import streamlit.components.v1 as components

# --- إعدادات الصفحة الأساسية ---
st.set_page_config(page_title="EEG Smart Lab", layout="wide", initial_sidebar_state="collapsed")

# --- دالة الاتصال بقاعدة البيانات ---
def get_db_connection():
    conn = sqlite3.connect('medical_system.db')
    conn.row_factory = sqlite3.Row
    return conn

# --- إدارة التنقل (Session State) ---
if 'role' not in st.session_state:
    st.session_state.role = None
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

# --- 1. الصفحة الرئيسية (الأزرار الثلاثة بالفرنسية) ---
if st.session_state.role is None:
    st.markdown("""
        <style>
        .main-title { text-align: center; color: #1e3a8a; font-weight: 800; margin-top: 50px; }
        .btn-container { display: flex; justify-content: center; gap: 20px; margin-top: 30px; flex-wrap: wrap; }
        .role-btn { 
            padding: 20px 40px; font-size: 20px; font-weight: bold; border-radius: 15px; 
            border: none; cursor: pointer; transition: 0.3s; width: 250px;
        }
        .btn-doctor { background: #1e3a8a; color: white; }
        .btn-patient { background: #00f2ff; color: #020406; }
        .btn-admin { background: #64748b; color: white; }
        </style>
        <h1 class="main-title">BIENVENUE AU EEG SMART LAB</h1>
        <p style="text-align:center; color:#64748b;">Veuillez choisir votre espace pour continuer</p>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("👨‍⚕️ ESPACE DOCTEUR", use_container_width=True):
            st.session_state.role = 'doctor'
            st.rerun()
    with col2:
        if st.button("👤 ESPACE PATIENT", use_container_width=True):
            st.session_state.role = 'patient'
            st.rerun()
    with col3:
        if st.button("⚙️ ESPACE ADMIN", use_container_width=True):
            st.session_state.role = 'admin'
            st.rerun()

# --- 2. واجهة الطبيب (Login & Register) ---
elif st.session_state.role == 'doctor' and not st.session_state.logged_in:
    if st.button("← Retour"): st.session_state.role = None; st.rerun()
    
    tab_log, tab_reg = st.tabs(["Connexion", "Inscription"])
    
    with tab_log:
        st.subheader("Accéder à mon compte")
        user = st.text_input("Utilisateur")
        pwd = st.text_input("Mot de passe", type="password")
        if st.button("SE CONNECTER"):
            conn = get_db_connection()
            auth = conn.execute("SELECT * FROM doctor WHERE username=? AND password=?", (user, pwd)).fetchone()
            if auth:
                st.session_state.logged_in = True
                st.session_state.user_name = user
                st.rerun()
            else: st.error("Identifiants incorrects")

    with tab_reg:
        # هنا نعرضوا الفورم نتاعك اللي بعثتيه
        st.markdown("""<h2 style='color:#1e3a8a'>Inscription Professionnelle</h2>""", unsafe_allow_html=True)
        with st.form("doc_reg"):
            f_name = st.text_input("Prénom")
            l_name = st.text_input("Nom")
            email = st.text_input("Email")
            u_name = st.text_input("Utilisateur")
            p_word = st.text_input("Mot de passe", type="password")
            if st.form_submit_button("CRÉER LE COMPTE"):
                conn = get_db_connection()
                conn.execute("INSERT INTO doctor (username, password, name) VALUES (?,?,?)", (u_name, p_word, f"{f_name} {l_name}"))
                conn.commit()
                st.success("Compte créé avec succès!")

# --- 3. واجهة المريض (التصميم اللي بعثتيه) ---
elif st.session_state.role == 'patient' and not st.session_state.logged_in:
    if st.button("← Retour"): st.session_state.role = None; st.rerun()
    
    # دمج الـ HTML نتاع المريض اللي بعثتيه مع منطق تسجيل الدخول
    st.info("Interface Patient Active")
    # (هنا نضع منطق التحقق من المريض في القاعدة بنفس طريقة الطبيب)
    p_user = st.text_input("Identifiant Patient")
    p_pass = st.text_input("Mot de passe", type="password")
    if st.button("Ouvrir la session"):
        # التحقق من قاعدة البيانات
        st.session_state.logged_in = True
        st.rerun()

# --- 4. واجهة الأدمين (عرض الجداول) ---
elif st.session_state.role == 'admin':
    st.title("⚙️ Administration du Système")
    if st.button("Déconnexion"): st.session_state.role = None; st.rerun()
    
    conn = get_db_connection()
    st.subheader("📋 Liste des Docteurs")
    df_docs = pd.read_sql_query("SELECT id, username, name FROM doctor", conn)
    st.table(df_docs)
    
    st.subheader("📋 Liste des Patients")
    # نفترض وجود جدول مريض
    try:
        df_pats = pd.read_sql_query("SELECT * FROM patient", conn)
        st.table(df_pats)
    except:
        st.warning("Table 'patient' non trouvée.")
    conn.close()

# --- 5. الواجهة النهائية للطبيب (بعد الدخول - الأوسيلوسكوب) ---
elif st.session_state.logged_in:
    st.sidebar.title(f"Dr. {st.session_state.get('user_name')}")
    if st.sidebar.button("Déconnexion"):
        st.session_state.logged_in = False
        st.rerun()
    st.success("Dashboard Analyse IA en ligne")
    # هنا تحطي كود الأوسيلوسكوب والتحليل
