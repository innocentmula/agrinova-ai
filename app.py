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
.gradio-container {
    max-width: 1050px !important;
    margin: auto !important;
    background: #f6f8f2 !important;
}
#hero {
    background: linear-gradient(135deg, #123d2b, #26734d);
    color: white;
    padding: 30px 22px;
    border-radius: 22px;
    text-align: center;
    margin-bottom: 18px;
}
#hero h1 {
    color: white !important;
    font-size: clamp(28px, 5vw, 42px) !important;
}
#hero p { color: #e1f3e5 !important; }
.panel {
    background: white;
    border: 1px solid #e0e9dc;
    border-radius: 18px;
    padding: 18px;
}
.primary-button {
    background: #247447 !important;
    color: white !important;
    border-radius: 12px !important;
    min-height: 46px !important;
    font-weight: 700 !important;
}
footer { display: none !important; }
@media (max-width: 600px) {
    #hero { padding: 22px 12px; }
    .panel { padding: 12px; }
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
            None,
            None,
        )
    except Exception as e:
        print("Signup error:", str(e))
        return (
            "Kwiyandikisha ntibyashobotse. Reba email yawe cyangwa "
            "igenamiterere rya Supabase.",
            None,
