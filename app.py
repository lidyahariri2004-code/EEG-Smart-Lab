import streamlit as st
import sqlite3
import os
import pandas as pd
import numpy as np
import pywt
import cv2
from tensorflow.keras.models import load_model

# --- 1. إعداد قاعدة البيانات ---
conn = sqlite3.connect('medical_system.db', check_same_thread=False)
c = conn.cursor()
c.execute('CREATE TABLE IF NOT EXISTS Doctor (fname TEXT, lname TEXT, username TEXT UNIQUE, password TEXT)')
c.execute('CREATE TABLE IF NOT EXISTS Patient (nom TEXT, prenom TEXT, age INTEGER, username TEXT UNIQUE, password TEXT)')
conn.commit()

# --- 2. تحميل الموديل ---
@st.cache_resource
def get_model():
    if os.path.exists('model.keras'):
        return load_model('model.keras')
    return None

model = get_model()

# --- 3. إدارة الجلسة (Session) ---
if 'role' not in st.session_state:
    st.session_state.role = None

# --- 4. واجهة المستخدم ---
st.sidebar.title("EEG Smart Lab")

if st.session_state.role is None:
    st.title("Bienvenue sur EEG Smart Lab")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Espace Docteur"):
            st.session_state.role = 'doctor_login'
            st.rerun()
    with col2:
        if st.button("Espace Patient"):
            st.session_state.role = 'patient_login'
            st.rerun()

elif st.session_state.role == 'doctor_login':
    st.subheader("Connexion Docteur")
    user = st.text_input("Nom d'utilisateur")
    pw = st.text_input("Mot de passe", type="password")
    if st.button("Se connecter"):
        # هنا يمكنك إضافة التحقق من قاعدة البيانات
        st.session_state.role = 'doctor_dash'
        st.rerun()
    if st.button("Retour"):
        st.session_state.role = None
        st.rerun()

elif st.session_state.role == 'doctor_dash':
    st.title("Tableau de bord Docteur")
    uploaded_file = st.file_uploader("Charger le signal EEG (CSV)", type="csv")
    
    if uploaded_file and model:
        df = pd.read_csv(uploaded_file, header=None)
        # منطق المعالجة (Scalogram) يوضع هنا
        st.success("Signal chargé avec succès !")
        st.line_chart(df.iloc[:300, 0]) # عرض جزء من الإشارة
        
    if st.sidebar.button("Déconnexion"):
        st.session_state.role = None
        st.rerun()
