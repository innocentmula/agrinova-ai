import os
from datetime import datetime, timezone

import gradio as gr
from google import genai
from supabase import create_client


SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")


def get_supabase(token=None):
    if not SUPABASE_URL or not SUPABASE_KEY:
        raise ValueError("Supabase ntirashyirwaho neza muri Render.")

    client = create_client(SUPABASE_URL, SUPABASE_KEY)
    if token:
        client.postgrest.auth(token)
    return client


CSS = """
:root { --agri-green: #176b45; --agri-dark: #103d2b; --agri-mint: #eaf6ed; }
.gradio-container {
    max-width: 1220px !important; margin: auto !important;
    background: #f4f8f3 !important; font-family: Inter, ui-sans-serif, system-ui, sans-serif !important;
}
body { background: #f4f8f3 !important; }
#hero {
    background: radial-gradient(circle at 85% 15%, rgba(188,235,145,.25), transparent 30%),
                linear-gradient(125deg, #103d2b 0%, #176b45 58%, #328454 100%);
    color: #fff; padding: 34px 30px; border-radius: 26px; text-align: left;
    margin: 8px 0 22px; box-shadow: 0 14px 36px rgba(16,61,43,.15); overflow: hidden;
}
#hero .hero-inner { display:flex; align-items:center; gap:20px; max-width:100%; }
#hero .brand-mark { display:flex; align-items:center; justify-content:center; width:76px; height:76px;
    border-radius:22px; background:rgba(255,255,255,.14); border:1px solid rgba(255,255,255,.24); font-size:42px; flex-shrink:0; }
#hero h1 { color:#fff !important; font-size:clamp(30px,4vw,46px) !important; line-height:1.05 !important; margin:0 0 9px !important; letter-spacing:-1px; }
#hero p { color:#e4f5e8 !important; margin:5px 0 !important; font-size:15px; }
#hero .eyebrow { color:#c5ef9e; text-transform:uppercase; letter-spacing:2px; font-size:11px; font-weight:800; margin-bottom:8px; }
#hero .hero-chip { display:inline-block; margin-top:11px; border:1px solid rgba(255,255,255,.24); background:rgba(255,255,255,.1); padding:7px 11px; border-radius:999px; font-size:12px; }
.panel {
    background:#fff !important; border:1px solid #e1eae0 !important; border-radius:20px !important;
    padding:20px !important; box-shadow:0 5px 18px rgba(28,70,42,.045);
}
.section-title { color:#173d2b; font-weight:800; letter-spacing:-.3px; }
.gradio-container .tab-nav { gap:8px; border-bottom:1px solid #dfe9df; margin-bottom:18px; }
.gradio-container .tab-nav button { border-radius:12px 12px 0 0 !important; font-weight:700 !important; }
.gradio-container input, .gradio-container textarea, .gradio-container select {
    border-radius:12px !important; border-color:#dbe6da !important; background:#fcfefc !important;
}
.gradio-container input:focus, .gradio-container textarea:focus { border-color:#58a477 !important; box-shadow:0 0 0 3px rgba(46,139,87,.1) !important; }
.gradio-container button { border-radius:12px !important; font-weight:700 !important; }
.primary-button { background:linear-gradient(135deg,#176b45,#2c8a55) !important; color:#fff !important; border:0 !important; min-height:48px !important; box-shadow:0 5px 12px rgba(23,107,69,.18); }
.primary-button:hover { filter:brightness(1.04); }
#auth-status { background:#eff8ef; border:1px solid #d7ead8; border-radius:14px; padding:12px 15px; }
#answer-panel { background:linear-gradient(180deg,#fff 0%,#fbfefb 100%) !important; border:1px solid #dce9dc !important; border-radius:20px !important; padding:22px !important; min-height:260px; }
#history-panel { background:#fff !important; border:1px solid #e1eae0 !important; border-radius:18px !important; padding:18px !important; }
#footer-note { color:#647b69; text-align:center; font-size:12px; padding:16px 10px 4px; }
footer { display:none !important; }
@media (max-width: 650px) {
    #hero { padding:22px 17px; border-radius:20px; }
    #hero .hero-inner { align-items:flex-start; gap:13px; }
    #hero .brand-mark { width:54px; height:54px; border-radius:16px; font-size:30px; }
    #hero p { font-size:13px; }
    .panel { padding:14px !important; }
}
"""


def kwiyandikisha(email, password):
    if not email or not email.strip() or not password:
        return "Andika email n'ijambo ry'ibanga.", None, None

    if len(password) < 8:
        return "Ijambo ry'ibanga rigomba kugira nibura inyuguti 8.", None, None

    try:
        client = get_supabase()
        result = client.auth.sign_up({
            "email": email.strip(),
            "password": password,
        })

        if result.session and result.user:
            return (
                "Konti yakozwe neza kandi winjiye muri AgriNova AI.",
                result.session.access_token,
                str(result.user.id),
            )

        return (
            "Konti yakozwe. Reba email yawe wemeze konti, "
            "hanyuma winjire ukoresheje email n'ijambo ry'ibanga.",
