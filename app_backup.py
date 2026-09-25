import streamlit as st
import requests
import base64

BACKEND_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="Bharat Smart Platform", page_icon="🌐", layout="wide", initial_sidebar_state="expanded")

if "active_mode" not in st.session_state:
    st.session_state.active_mode = "home"
if "history_view_data" not in st.session_state:
    st.session_state.history_view_data = None
if "theme_mode" not in st.session_state:
    st.session_state.theme_mode = "Dark Mode" 

translations = {
    "English": {
        "search_title": "BHARAT SEARCH", "search_desc": "Quantum-speed multi-modal search matrix.",
        "ai_title": "BHARAT AI", "ai_desc": "Neural-net reasoning and intelligence core.",
        "lok_title": "LOK-SEVAK", "lok_desc": "Next-gen public welfare & grievance portal.",
        "input_label": "Enter command or initialize voice input...", "upload_label": "Scan Document (Image/PDF)",
        "btn_run": "INITIALIZE SEQUENCE ⚡"
    },
    "हिन्दी": {
        "search_title": "भारत सर्च", "search_desc": "क्वांटम-स्पीड मल्टी-मोडल सर्च मैट्रिक्स।",
        "ai_title": "भारत एआई", "ai_desc": "न्यूरल-नेट तर्क और बुद्धिमत्ता कोर।",
        "lok_title": "लोक-सेवक", "lok_desc": "नेक्स्ट-जेन जन कल्याण और शिकायत पोर्टल।",
        "input_label": "कमांड दर्ज करें या वॉयस इनपुट प्रारंभ करें...", "upload_label": "दस्तावेज़ स्कैन करें (छवि/पीडीएफ)",
        "btn_run": "प्रारंभ करें ⚡"
    }
}

with st.sidebar:
    st.markdown("### 💠 CORE CONTROL")
    st.session_state.theme_mode = st.radio("UI THEME", ["Dark Mode", "Light Mode"], index=0 if st.session_state.theme_mode == "Dark Mode" else 1, label_visibility="collapsed")
    app_language = st.selectbox("SYSTEM LANGUAGE", ["English", "हिन्दी"])
    t = translations[app_language]
    
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("⬛ MAIN DASHBOARD", use_container_width=True):
        st.session_state.active_mode = "home"
        st.rerun()

    st.markdown("---")
    st.markdown("🛰️ **DATA LOGS:**")
    try:
        hist_res = requests.get(f"{BACKEND_URL}/api/v1/history")
        if hist_res.status_code == 200:
            for h in hist_res.json():
                if st.button(f"⏱️ {h['query'][:20]}...", key=f"hist_{h['id']}", use_container_width=True):
                    st.session_state.history_view_data = h
                    st.session_state.active_mode = "history_view"
                    st.rerun()
    except:
        st.caption("Uplink Offline.")

if st.session_state.theme_mode == "Dark Mode":
    bg_color = "radial-gradient(circle at top left, #0a0f1c, #02040a)"
    glass_bg = "rgba(16, 24, 43, 0.6)"
    text_color = "#e2e8f0"
    neon_glow = "0 0 20px rgba(255, 153, 51, 0.3)"
    btn_grad = "linear-gradient(45deg, #FF9933, #ff4500)"
    border_color = "rgba(255, 153, 51, 0.2)"
else:
    bg_color = "radial-gradient(circle at top left, #f8fafc, #e2e8f0)"
    glass_bg = "rgba(255, 255, 255, 0.7)"
    text_color = "#0f172a"
    neon_glow = "0 10px 30px rgba(0, 0, 0, 0.1)"
    btn_grad = "linear-gradient(45deg, #FF9933, #ff6600)"
    border_color = "rgba(255, 153, 51, 0.4)"

st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;600;700&display=swap');
    
    .stApp {{
        background: {bg_color};
        color: {text_color};
        font-family: 'Space Grotesk', sans-serif;
    }}
    
    .hero-banner {{
        background: {glass_bg};
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border: 1px solid {border_color};
        border-radius: 20px;
        padding: 50px;
        text-align: center;
        box-shadow: {neon_glow};
        margin-bottom: 40px;
        animation: pulse 4s infinite alternate;
    }}
    
    @keyframes pulse {{
        0% {{ box-shadow: 0 0 15px rgba(255, 153, 51, 0.2); }}
        100% {{ box-shadow: 0 0 35px rgba(255, 153, 51, 0.5); transform: translateY(-2px); }}
    }}

    .app-title {{
        font-size: 3.5rem; 
        font-weight: 700; 
        margin-bottom: 10px;
        background: -webkit-linear-gradient(45deg, #FF9933, #3b82f6, #138808);
        -webkit-background-clip: text; 
        -webkit-text-fill-color: transparent;
        letter-spacing: 2px;
    }}

    .stButton>button {{
        background: {btn_grad};
        color: white; 
        border: 1px solid rgba(255,255,255,0.2); 
        font-weight: 700;
        letter-spacing: 1.5px;
        border-radius: 8px; 
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        text-transform: uppercase;
        padding: 12px 24px;
    }}
    .stButton>button:hover {{ 
        transform: scale(1.05);
        box-shadow: 0 0 20px rgba(255, 153, 51, 0.7);
        border: 1px solid #fff;
    }}

    .stTextInput input, .stTextArea textarea {{
        background: {glass_bg} !important;
        color: {text_color} !important;
        border: 1px solid {border_color} !important;
        border-radius: 10px !important;
        padding: 15px !important;
        font-family: 'Space Grotesk', sans-serif !important;
    }}
    
    .module-card {{
        background: {glass_bg};
        backdrop-filter: blur(10px);
        border: 1px solid {border_color};
        border-radius: 15px;
        padding: 30px;
        height: 100%;
        transition: all 0.3s ease;
    }}
    .module-card:hover {{
        transform: translateY(-10px);
        border-color: #FF9933;
        box-shadow: 0 10px 30px rgba(255, 153, 51, 0.2);
    }}
    .module-icon {{ font-size: 3rem; margin-bottom: 15px; }}
    .module-title {{ font-size: 1.5rem; font-weight: 700; margin-bottom: 10px; color: #FF9933; }}
    .module-desc {{ font-size: 0.9rem; opacity: 0.8; margin-bottom: 20px; }}
</style>
""", unsafe_allow_html=True)

def play_audio(text, lang):
    try:
        res = requests.post(f"{BACKEND_URL}/api/v1/tts", data={"prompt": text, "language": lang})
        if res.status_code == 200:
            st.audio(base64.b64decode(res.json().get("audio_base64")), format="audio/mp3")
    except:
        pass

def render_multimodal_interface(mode_id, header_title, header_desc):
    st.button("⏏️ RETURN TO TERMINAL", on_click=lambda: st.session_state.update({"active_mode": "home"}))
    st.markdown(f"""
    <div style="background: {glass_bg}; backdrop-filter: blur(10px); border: 1px solid {border_color}; border-radius: 15px; padding: 25px; margin-bottom: 30px;">
        <h2 style="margin:0; color:#FF9933;">{header_title}</h2>
        <p style="margin:5px 0 0 0; opacity:0.8;">{header_desc}</p>
    </div>
    """, unsafe_allow_html=True)
    
    query_text = st.text_input(t["input_label"])
    uploaded_file = st.file_uploader(t["upload_label"], type=["png", "jpg", "jpeg", "pdf"])
    
    if st.button(t["btn_run"]):
        if not query_text and not uploaded_file:
            st.warning("⚠️ Awaiting input parameters...")
            return
            
        with st.spinner("Processing Quantum Data..."):
            data = {"prompt": query_text if query_text else "Analyze this document", "language": app_language, "mode": mode_id}
            files = {"file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)} if uploaded_file else {}
            
            try:
                res = requests.post(f"{BACKEND_URL}/api/v1/query", data=data, files=files if files else None)
                if res.status_code == 200:
                    reply = res.json().get("response")
                    st.markdown(f"""
                    <div style="background: rgba(19, 136, 8, 0.1); border-left: 4px solid #138808; padding: 20px; border-radius: 0 10px 10px 0; margin-top: 20px;">
                        <h4 style="color: #138808; margin-top:0;">✅ DATA DECRYPTED</h4>
                        {reply}
                    </div>
                    """, unsafe_allow_html=True)
                    play_audio(reply[:500], app_language)
                else:
                    st.error(f"SYSTEM ERROR: {res.text}")
            except Exception as e:
                st.error(f"LINK SEVERED: {str(e)}")

if st.session_state.active_mode == "history_view" and st.session_state.history_view_data:
    st.button("⏏️ RETURN TO TERMINAL", on_click=lambda: st.session_state.update({"active_mode": "home"}))
    data = st.session_state.history_view_data
    st.markdown(f"### 📂 ARCHIVED LOG ({data['mode'].upper()})")
    st.info(f"**USER COMMAND:** {data['query']}")
    st.success(data['response'])
    play_audio(data['response'][:500], app_language)

elif st.session_state.active_mode == "home":
    st.markdown(f"""
    <div class="hero-banner">
        <h1 class="app-title">BHARAT NEXUS</h1>
        <p style="color: #FF9933; font-weight: 600; font-size: 1.2rem; letter-spacing: 1px;">"Empowering every citizen with Artificial Intelligence."</p>
    </div>
    """, unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    
    with c1:
        st.markdown(f"""<div class="module-card"><div class="module-icon">🌐</div><div class="module-title">{t['search_title']}</div><div class="module-desc">{t['search_desc']}</div></div>""", unsafe_allow_html=True)
        if st.button("ACCESS SEARCH", key="btn_s"): st.session_state.active_mode = "search"; st.rerun()
    with c2:
        st.markdown(f"""<div class="module-card"><div class="module-icon">🧠</div><div class="module-title">{t['ai_title']}</div><div class="module-desc">{t['ai_desc']}</div></div>""", unsafe_allow_html=True)
        if st.button("ACCESS AI", key="btn_a"): st.session_state.active_mode = "ai"; st.rerun()
    with c3:
        st.markdown(f"""<div class="module-card"><div class="module-icon">🏛️</div><div class="module-title">{t['lok_title']}</div><div class="module-desc">{t['lok_desc']}</div></div>""", unsafe_allow_html=True)
        if st.button("ACCESS LOK-SEVAK", key="btn_l"): st.session_state.active_mode = "lok"; st.rerun()

elif st.session_state.active_mode == "search":
    render_multimodal_interface("search", f"🌐 {t['search_title']}", t['search_desc'])

elif st.session_state.active_mode == "ai":
    render_multimodal_interface("ai", f"🧠 {t['ai_title']}", t['ai_desc'])

elif st.session_state.active_mode == "lok":
    render_multimodal_interface("lok", f"🏛️ {t['lok_title']}", t['lok_desc'])