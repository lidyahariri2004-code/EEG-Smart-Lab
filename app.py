import streamlit as st

# إعدادات الصفحة لتظهر بشكل جميل
st.set_page_config(page_title="EEG Smart Lab - Pro", page_icon="🧠", layout="centered")

# --- واجهة تسجيل الدخول الوهمية (simulation) ---
st.sidebar.header("🔑 تسجيل الدخول")
username = st.sidebar.text_input("اسم المستخدم")
password = st.sidebar.text_input("كلمة المرور", type="password")
login_button = st.sidebar.button("دخول")

if login_button:
    # محاكاة للأدوار (سنغير هذا لقاعدة بيانات حقيقية لاحقاً)
    if username == "admin" and password == "admin123":
        st.session_state['role'] = 'admin'
        st.sidebar.success("تم الدخول كأدمين.")
    elif username == "doctor1" and password == "doc123":
        st.session_state['role'] = 'doctor'
        st.sidebar.success("تم الدخول كطبيب.")
    else:
        st.sidebar.error("خطأ في البيانات.")

# --- واجهة التطبيق الرئيسية حسب الدور ---
if 'role' in st.session_state:
    st.title("🧠 EEG Smart Lab - Dashboard")
    st.write("---")

    if st.session_state['role'] == 'admin':
        st.header("🏢 لوحة تحكم الأدمين")
        st.write("🔧 إدارة المستخدمين | 📊 الإحصائيات العامة")
        col1, col2 = st.columns(2)
        with col1:
            st.button("➕ إضافة طبيب جديد")
        with col2:
            st.button("📄 تقارير النظام")

    elif st.session_state['role'] == 'doctor':
        st.header("👨‍⚕️ لوحة تحكم الطبيب")
        st.write("📂 ملفات المرضى | 🔬 تحليل الإشارات")
        
        selected_patient = st.selectbox("اختار المريض", ["محمد", "علي", "فاطمة"])
        st.write(f"تحليل إشارة EEG للمريض: **{selected_patient}**")
        
        # واجهة رفع الملف القديمة نتاعك
        uploaded_file = st.file_uploader("📂 ارفعي ملف إشارة EEG (.txt)", type=['txt'])
        
        if uploaded_file:
            st.info("✅ تم استقبال الإشارة بنجاح. المودال بانتظار التحليل...")

else:
    st.title("🧠 EEG Smart Lab")
    st.write("---")
    st.warning("يرجى تسجيل الدخول من القائمة الجانبية للوصول إلى لوحة التحكم.")
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/c/cd/EEG_skull_grid.png/220px-EEG_skull_grid.png", caption="EEG System")
