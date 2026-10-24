
import os
from datetime import datetime, timezone

import gradio as gr
from google import genai
from supabase import create_client

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")


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
            "password": password
        })

        if result.session and result.user:
            return (
                "Konti yakozwe neza kandi winjiye muri AgriNova AI.",
                result.session.access_token,
                str(result.user.id)
            )

        return (
            "Konti yakozwe. Reba email yawe wemeze konti, "
            "hanyuma winjire ukoresheje email n'ijambo ry'ibanga.",
            None,
            None
        )

                    type="password"
                )
                login_btn = gr.Button(
                    "Injira",
                    variant="primary"
                )
                logout_btn = gr.Button("Sohoka")

        auth_status = gr.Markdown(
            "Iyandikishe cyangwa winjire kugira ngo ukomeze."
        )

    with gr.Tab("🌾 Umujyanama w'ubuhinzi"):
        with gr.Row():
            with gr.Column(scale=6, elem_classes=["panel"]):
                gr.Markdown("## 🧑🏽‍🌾 Tubwire ikibazo cyawe")

                igihingwa = gr.Textbox(
                    label="🌿 Igihingwa",
                    placeholder="Urugero: Ibigori, ibishyimbo..."
                )
                aho = gr.Textbox(
                    label="📍 Aho uhingira",
                    placeholder="Urugero: Gatsibo, Nyagihanga"
                )
                ikibazo = gr.Textbox(
                    label="💬 Ikibazo cy'ubuhinzi",
                    placeholder="Sobanura ikibazo wabonye...",
                    lines=4
                )
                ifoto = gr.Image(
                    label="📷 Ifoto y'igihingwa (si ngombwa)",
                    type="pil"
                )
                advice_btn = gr.Button(
                    "🌱 Mpa inama",
                    variant="primary",
                    elem_classes=["primary-button"]
                )

            with gr.Column(scale=5, elem_classes=["panel"]):
                gr.Markdown("## 🌾 Inama ugenewe")
                answer_box = gr.Markdown(
                    "Inama yawe izagaragara hano."
                )

        gr.Markdown("## 💬 Ibiganiro wabitswe")
        history_box = gr.Markdown(
            "Injira muri konti yawe kugira ngo urebe ibiganiro."
        )

    signup_btn.click(
        fn=kwiyandikisha,
        inputs=[signup_email, signup_password],
        outputs=[auth_status, token_state, user_state]
    )

    login_btn.click(
        fn=kwinjira,
        inputs=[login_email, login_password],
        outputs=[
            auth_status, token_state, user_state,
            conversation_state, history_box
        ]
    )

    logout_btn.click(
        fn=gusohoka,
        inputs=[],
        outputs=[
            auth_status, token_state, user_state,
            conversation_state, history_box
        ]
    )

    advice_btn.click(
        fn=tanga_inama,
        inputs=[
            igihingwa, aho, ikibazo, ifoto,
            token_state, user_state, conversation_state, history_box
        ],
        outputs=[answer_box, history_box, conversation_state]
    )

    gr.Markdown("""
    ---
    <div style="text-align:center; color:#45634f;">
        <b>AgriNova AI</b> 🌱<br>
        Ikoranabuhanga rifasha ubuhinzi gutera imbere.
        <br><small>
        Inama zitangwa na AI zishobora kutaba zuzuye.
        Ku kibazo gikomeye, baza umuhanga mu buhinzi.
        </small>
    </div>
    """)


if __name__ == "__main__":
    app.launch(
        server_name="0.0.0.0",
        server_port=int(os.environ.get("PORT", 7860)),
        theme=gr.themes.Soft(
            primary_hue="green",
            secondary_hue="lime",
            neutral_hue="slate"
        ),
        css=CSS
    )


    try:
        client = get_supabase()
        result = client.auth.sign_in_with_password({
            "email": email.strip(),
            "password": password
        })

        token = result.session.access_token
        user_id = str(result.user.id)
        db = get_supabase(token)

        rows = (
            db.table("conversations")
            .select("id,title")
            .eq("user_id", user_id)
            .order("updated_at", desc=True)
            .limit(1)
            .execute()
        )

        conversation_id = None
        history = "Nta biganiro wabitswe urabona kuri konti yawe."

        if rows.data:
            conversation_id = rows.data[0]["id"]

            messages = (
                db.table("messages")
                .select("role,content")
                .eq("conversation_id", conversation_id)
                .eq("user_id", user_id)
                .order("created_at")
                .limit(100)
                .execute()
            )

            if messages.data:
                history = "\n\n".join(
                    ("**Wowe:** " if m["role"] == "user"
                     else "**AgriNova AI:** ") + m["content"]
                    for m in messages.data
                )

        return (
            "Winjiye neza muri AgriNova AI.",
            token,
            user_id,
            conversation_id,
            history
        )

    except Exception as e:
        print("Login error:", str(e))
        return (
            "Kwinjira ntibyashobotse. Reba email n'ijambo ry'ibanga, "
            "kandi wemeze email niba ubisabwa.",
            None, None, None, "Nta biganiro byafunguwe."
        )


def gusohoka():
    return (
        "Wasohotse muri konti yawe.",
        None, None, None,
        "Injira nanone kugira ngo ubone ibiganiro byawe."
    )


def tanga_inama(
    igihingwa, aho, ikibazo, ifoto,
    token, user_id, conversation_id, history
):
    if not token or not user_id:
        return (
            "### 🔐 Banza winjire muri konti yawe.",
            history or "",
            conversation_id
        )

    if not ikibazo or not ikibazo.strip():
        return (
            "### ✍️ Andika ikibazo cy'ubuhinzi.",
            history or "",
            conversation_id
        )

    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        return (
            "Serivisi ya AI ntirashyirwaho neza. Reba Render settings.",
            history or "",
            conversation_id
        )

    try:
        ai = genai.Client(api_key=api_key)

        prompt = f"""
Uri AgriNova AI, umujyanama w'ubuhinzi ufasha abahinzi bo mu Rwanda.
Subiza mu Kinyarwanda cyumvikana kandi cyoroshye gukurikiza.

Igihingwa: {igihingwa or 'Nticyavuzwe'}
Aho umuhinzi aherereye: {aho or 'Ntihavuzwe'}
Ikibazo: {ikibazo}

Tanga igisubizo gitondetse:
1. Impamvu zishoboka.
2. Ibyo umuhinzi yakora ubu.
3. Uko yakwirinda ko ikibazo cyongera kubaho.
4. Igihe yakwiyambaza umuhanga mu buhinzi.

Niba hari ifoto, koresha ibimenyetso bigaragara kuri yo.
Ntukemeze indwara udafitiye ibimenyetso bihagije.
Ntugire imiti cyangwa ingano yayo uhamya udafite amakuru ahagije.
Niba amakuru adahagije, baza ibibazo bisobanutse.
"""

        contents = [prompt]
        if ifoto is not None:
            contents.append(ifoto)

        response = ai.models.generate_content(
            model="gemini-3.5-flash-lite",
            contents=contents
        )

        answer = response.text or "Ntabwo habonetse igisubizo."

        # Bika ubutumwa ukoresheje uburenganzira bw'uyu mukoresha.
        db = get_supabase(token)

        if not conversation_id:
            created = (
                db.table("conversations")
                .insert({
                    "user_id": user_id,
                    "title": ikibazo.strip()[:80]
                })
                .execute()
            )

            if not created.data:
                raise ValueError("Ikiganiro nticyabashije kubikwa.")

            conversation_id = created.data[0]["id"]

        db.table("messages").insert([
            {
                "conversation_id": conversation_id,
                "user_id": user_id,
                "role": "user",
                "content": ikibazo.strip()
            },
            {
                "conversation_id": conversation_id,
                "user_id": user_id,
                "role": "assistant",
                "content": answer
            }
        ]).execute()

        db.table("conversations").update({
            "updated_at": datetime.now(timezone.utc).isoformat()
        }).eq(
            "id", conversation_id
        ).eq(
            "user_id", user_id
        ).execute()

        new_history = (history or "")
        new_history += (
            f"\n\n**Wowe:** {ikibazo.strip()}"
            f"\n\n**AgriNova AI:** {answer}"
        )

        return answer, new_history, conversation_id

    except Exception as e:
        print("AgriNova error:", str(e))
        return (
            "### ⚠️ Habaye ikibazo\n"
            "Igisubizo nticyabashije gutangwa cyangwa kubikwa. "
            "Ongera ugerageze.",
            history or "",
            conversation_id
        )


with gr.Blocks(
    title="AgriNova AI | Umujyanama w'Ubuhinzi",
    theme=gr.themes.Soft(
        primary_hue="green",
        secondary_hue="lime",
        neutral_hue="slate"
    ),
    css=CSS
) as app:

    token_state = gr.State(None)
    user_state = gr.State(None)
    conversation_state = gr.State(None)

    gr.HTML("""
    <div id="hero">
        <div style="font-size:46px;">🌱</div>
        <h1>AgriNova AI</h1>
        <p><b>Umujyanama w'ubuhinzi mu Kinyarwanda</b></p>
        <p>Inama z'ubuhinzi n'ibiganiro bibikwa muri konti yawe.</p>
    </div>
    """)

    with gr.Tab("🔐 Konti yanjye"):
        with gr.Row():
            with gr.Column(elem_classes=["panel"]):
                gr.Markdown("## Kwiyandikisha")
                signup_email = gr.Textbox(label="Email")
                signup_password = gr.Textbox(
                    label="Ijambo ry'ibanga",
                    type="password"
                )
                signup_btn = gr.Button(
                    "Fungura konti",
                    variant="primary"
                )

            with gr.Column(elem_classes=["panel"]):
                gr.Markdown("## Kwinjira")
                login_email = gr.Textbox(label="Email")
                login_password = gr.Textbox(
                    label="Ijambo ry'ibanga",
                    type="password"
                )
                login_btn = gr.Button(
                    "Injira",
                    variant="primary"
                )
                logout_btn = gr.Button("Sohoka")

        auth_status = gr.Markdown(
            "Iyandikishe cyangwa winjire kugira ngo ukomeze."
        )

    with gr.Tab("🌾 Umujyanama w'ubuhinzi"):
        with gr.Row():
            with gr.Column(scale=6, elem_classes=["panel"]):
                gr.Markdown("## 🧑🏽‍🌾 Tubwire ikibazo cyawe")

                igihingwa = gr.Textbox(
                    label="🌿 Igihingwa",
                    placeholder="Urugero: Ibigori, ibishyimbo..."
                )
                aho = gr.Textbox(
                    label="📍 Aho uhingira",
                    placeholder="Urugero: Gatsibo, Nyagihanga"
                )
                ikibazo = gr.Textbox(
                    label="💬 Ikibazo cy'ubuhinzi",
                    placeholder="Sobanura ikibazo wabonye...",
                    lines=4
                )
                ifoto = gr.Image(
                    label="📷 Ifoto y'igihingwa (si ngombwa)",
                    type="pil"
                )
                advice_btn = gr.Button(
                    "🌱 Mpa inama",
                    variant="primary",
                    elem_classes=["primary-button"]
                )

            with gr.Column(scale=5, elem_classes=["panel"]):
                gr.Markdown("## 🌾 Inama ugenewe")
                answer_box = gr.Markdown(
                    "Inama yawe izagaragara hano."
                )

        gr.Markdown("## 💬 Ibiganiro wabitswe")
        history_box = gr.Markdown(
            "Injira muri konti yawe kugira ngo urebe ibiganiro."
        )

    signup_btn.click(
        fn=kwiyandikisha,
        inputs=[signup_email, signup_password],
        outputs=[auth_status, token_state, user_state]
    )

    login_btn.click(
        fn=kwinjira,
        inputs=[login_email, login_password],
        outputs=[
            auth_status, token_state, user_state,
            conversation_state, history_box
        ]
    )

    logout_btn.click(
        fn=gusohoka,
        inputs=[],
        outputs=[
            auth_status, token_state, user_state,
            conversation_state, history_box
        ]
    )

    advice_btn.click(
        fn=tanga_inama,
        inputs=[
            igihingwa, aho, ikibazo, ifoto,
            token_state, user_state, conversation_state, history_box
        ],
        outputs=[answer_box, history_box, conversation_state]
    )

    gr.Markdown("""
    ---
    <div style="text-align:center; color:#45634f;">
        <b>AgriNova AI</b> 🌱<br>
        Ikoranabuhanga rifasha ubuhinzi gutera imbere.
        <br><small>
        Inama zitangwa na AI zishobora kutaba zuzuye.
        Ku kibazo gikomeye, baza umuhanga mu buhinzi.
        </small>
    </div>
    """)


if __name__ == "__main__":
    app.launch(
        server_name="0.0.0.0",
        server_port=int(os.environ.get("PORT", 7860))
    )
