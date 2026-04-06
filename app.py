import streamlit as st

# إعدادات الصفحة
st.set_page_config(page_title="EEG Smart Lab", page_icon="🧠")

st.title("🧠 EEG Smart Lab")
st.write("---")
st.success("مرحباً بكِ أستاذة. النظام جاهز وفي انتظار المودال النهائي.")

# خانة لرفع الملفات
uploaded_file = st.file_uploader("📂 ارفعي ملف إشارة EEG (.txt)", type=['txt'])

if uploaded_file:
    st.info("✅ تم استقبال الإشارة بنجاح. المودال قيد التحميل للتحليل...") 
