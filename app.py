import streamlit as st
import pandas as pd
import numpy as np
import os
from datetime import datetime

# --- إعدادات الواجهة ---
st.set_page_config(page_title="EEG Smart Lab Pro", layout="wide")

# --- محاكاة قاعدة البيانات (Database Simulation) ---
# ملاحظة: في Streamlit Cloud، يفضل استعمال ملفات CSV أو SQLite بسيطة
if 'db_patients' not in st.session_state:
    st.session_state['db_patients'] = pd.DataFrame(columns=['ID', 'Nom', 'Prenom', 'Age', 'Status'])
if 'logs' not in st.session_state:
    st.session_state['logs'] = []

# --- القائمة الجانبية (تسجيل الدخول) ---
st.sidebar.title("🔐 نظام الدخول الطبي")
role = st.sidebar.selectbox("الدخول كـ:", ["اختر الدور", "طبيب (Doctor)", "أدمين (Admin)", "مريض (Patient)"])

# --- 1. واجهة الأدمين (Admin) ---
if role == "أدمين (Admin)":
    st.title("⚙️ لوحة تحكم الأدمين")
    st.write("مراقب النظام: يمكنك رؤية كل النشاطات هنا.")
    
    col1, col2, col3 = st.columns(3)
    col1.metric("عدد الأطباء", "12")
    col2.metric("إجمالي المرضى", len(st.session_state['db_patients']))
    col3.metric("المودال النشط", "VGG16 (96%)")
    
    st.subheader("📋 سجل التحليلات الأخير (Logs)")
    if st.session_state['logs']:
        st.table(st.session_state['logs'])
    else:
        st.info("لا توجد سجلات حالياً.")

# --- 2. واجهة الطبيب (Doctor) ---
elif role == "طبيب (Doctor)":
    st.title("👨‍⚕️ بوابة الطبيب المختص")
    
    menu = st.tabs(["إضافة مريض", "فحص إشارة EEG", "سجلات المرضى"])
    
    with menu[0]:
        st.subheader("📝 تسجيل مريض جديد")
        with st.form("patient_form"):
            nom = st.text_input("لقب المريض")
            prenom = st.text_input("اسم المريض")
            age = st.number_input("العمر", min_value=1, max_value=100)
            if st.form_submit_button("حفظ في قاعدة البيانات"):
                new_data = {"ID": len(st.session_state['db_patients'])+1, "Nom": nom, "Prenom": prenom, "Age": age, "Status": "Active"}
                st.session_state['db_patients'] = pd.concat([st.session_state['db_patients'], pd.DataFrame([new_data])], ignore_index=True)
                st.success("تم تسجيل المريض بنجاح!")

    with menu[1]:
        st.subheader("🔬 تحليل الإشارة بالمودال")
        patient_to_test = st.selectbox("اختر المريض", st.session_state['db_patients']['Nom'].tolist() if not st.session_state['db_patients'].empty else ["لا يوجد مرضى"])
        file = st.file_uploader("ارفع ملف EEG (.txt)", type=['txt'])
        
        if file:
            st.info("🔄 جاري المعالجة (Wavelet Transform)...")
            # محاكاة عمل المودال model.keras
            st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/c/cd/EEG_skull_grid.png/220px-EEG_skull_grid.png", width=200)
            
            # نتيجة تجريبية (تنبيه باللون الأحمر كما طلبتِ)
            prediction = "Seizure Detected (Focal)" 
            st.error(f"🚨 النتيجة: {prediction}")
            st.session_state['logs'].append({"Time": datetime.now(), "Patient": patient_to_test, "Result": prediction})

    with menu[2]:
        st.subheader("📂 قاعدة بيانات المرضى")
        st.dataframe(st.session_state['db_patients'])

# --- 3. واجهة المريض (Patient) ---
elif role == "مريض (Patient)":
    st.title("👤 بوابة المريض")
    st.write("مرحباً بك. هنا يمكنك رؤية نتائج فحوصاتك الأخيرة.")
    # عرض سجل المريض فقط
    st.info("لا توجد نتائج جديدة مبعوثة من الطبيب حالياً.")

else:
    st.title("🧠 EEG Smart Lab")
    st.write("---")
    st.header("مرحباً بك في المنصة الطبية")
    st.info("يرجى اختيار دورك من القائمة الجانبية للبدء.")
    st.image("https://static.streamlit.io/examples/dog.jpg", caption="صورة توضيحية للنظام") # يمكنك تغييرها بصورة طبية
