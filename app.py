import streamlit as st
import streamlit.components.v1 as components

# إعداد الصفحة
st.set_page_config(page_title="EEG AI Monitor", layout="wide")

# هنا نحطو الـ HTML والـ CSS نتاعك كامل داخل متغير
html_code = """
<!DOCTYPE html>
<html lang="fr">
<head>
    <style>
        :root { --bg-deep: #020406; --neon-blue: #00f2ff; --neon-red: #ff0044; }
        body { background-color: var(--bg-deep); color: #e2e8f0; font-family: sans-serif; }
        .sidebar { width: 300px; background: #0d1117; padding: 20px; border-right: 2px solid #161b22; }
        /* راني لخصت برك، بصح نتي تقدري تحطي كودك كامل هنا */
    </style>
</head>
<body>
    <div style="display: flex; height: 100vh;">
        <div class="sidebar">
            <h4 style="color: #00f2ff;">🧠 EEG AI SYSTEM</h4>
            <p>Bienvenue, Dr. Lydia</p>
            <hr style="border-color: #30363d;">
            <button style="width: 100%; padding: 10px; background: #00f2ff; border: none; border-radius: 5px;">AJOUTER SÉQUENCES</button>
        </div>
        <div style="flex-grow: 1; padding: 20px; background: #000;">
            <h2 style="letter-spacing: 2px;">OSCILLOSCOPE TEMPS RÉEL</h2>
            <div style="height: 400px; border: 2px solid #333; position: relative; background: #000;">
                 <p style="text-align: center; color: #444; margin-top: 150px;">L'analyseur est prêt...</p>
            </div>
        </div>
    </div>
</body>
</html>
"""

# تشغيل الـ HTML نتاعك داخل تطبيق Streamlit
components.html(html_code, height=800, scrolling=True)
