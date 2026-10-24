import os
import gradio as gr
from google import genai
from supabase import create_client
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase = None
if SUPABASE_URL and SUPABASE_KEY:
    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

CSS = """
.gradio-container {
    max-width: 1050px !important;
    margin: auto !important;
    background: #f6f8f2 !important;
}
#hero {
    background: linear-gradient(135deg, #123d2b, #26734d);
    color: white;
    padding: 32px 26px;
    border-radius: 22px;
    text-align: center;
    margin-bottom: 18px;
}
#hero h1 {
    color: white !important;
    font-size: clamp(28px, 5vw, 42px) !important;
    margin-bottom: 8px !important;
}
#hero p {
    color: #e1f3e5 !important;
    font-size: 16px;
}
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
    min-height: 48px !important;
    font-weight: 700 !important;
}
footer { display: none !important; }
@media (max-width: 600px) {
    #hero { padding: 24px 14px; }
    .panel { padding: 12px; }
}
"""


def tanga_inama(igihingwa, aho, ikibazo, ifoto):
    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        return "### ⚠️ Habaye ikibazo\nNyir'uru rubuga agomba kugenzura GEMINI_API_KEY muri Render."

    if not ikibazo or not ikibazo.strip():
        return "### ✍️ Andika ikibazo\nSobanura ikibazo ufite ku gihingwa kugira ngo ngufashe."

    try:
        client = genai.Client(api_key=api_key)

        prompt = f"""
Uri AgriNova AI, umujyanama w'ubuhinzi ufasha abahinzi bo mu Rwanda.
Subiza mu Kinyarwanda cyumvikana, cyubaha umuhinzi kandi cyoroshye gukurikiza.

Igihingwa: {igihingwa or 'Nticyavuzwe'}
Aho umuhinzi aherereye: {aho or 'Ntihavuzwe'}
Ikibazo: {ikibazo}

Tanga igisubizo gitondetse neza:
1. Impamvu zishoboka z'ikibazo.
2. Ibyo umuhinzi yakora ubu.
3. Uburyo bwo gukumira ko ikibazo cyongera kubaho.
4. Igihe agomba kugisha inama umuhanga mu buhinzi.

Niba hari ifoto, koresha ibimenyetso bigaragara kuri yo.
Ntukemeze indwara udafitiye ibimenyetso bihagije.
Ntugire imiti cyangwa ingano yayo uhamya udafite amakuru ahagije.
Niba amakuru adahagije, baza ibibazo bisobanutse.
"""

        contents = [prompt]
        if ifoto is not None:
            contents.append(ifoto)

        response = client.models.generate_content(
            model="gemini-3.5-flash-lite",
            contents=contents
        )

        return response.text or "Ntabwo habonetse igisubizo. Ongera ugerageze."

    except Exception as e:
        print("Ikosa rya AgriNova AI:", str(e))
        return (
            "### ⚠️ Ntibyashobotse gutanga igisubizo\n"
            "Ongera ugerageze nyuma. Niba bikomeje, nyir'uru rubuga "
            "agomba kugenzura ibibazo biri muri Render Logs."
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

    gr.HTML("""
    <div id="hero">
        <div style="font-size:48px;">🌱</div>
        <h1>AgriNova AI</h1>
        <p><b>Umujyanama w'ubuhinzi mu Kinyarwanda</b></p>
        <p>
            Menya uko wafasha ibihingwa byawe.
            Andika ikibazo cyangwa wohereze ifoto kugira ngo ubone inama.
        </p>
    </div>
    """)

    with gr.Row():
        with gr.Column(scale=6, elem_classes=["panel"]):
            gr.Markdown("## 🧑🏽‍🌾 Tubwire ibijyanye n'igihingwa cyawe")
            igihingwa = gr.Textbox(
                label="🌿 Igihingwa",
                placeholder="Urugero: Ibigori, ibishyimbo, imyumbati..."
            )
            aho = gr.Textbox(
                label="📍 Aho uhingira",
                placeholder="Urugero: Gatsibo, Nyagihanga"
            )
            ikibazo = gr.Textbox(
                label="💬 Ikibazo cy'ubuhinzi",
                placeholder="Sobanura ibimenyetso cyangwa ikibazo wabonye...",
                lines=4
            )
            ifoto = gr.Image(
                label="📷 Ifoto y'igihingwa (si ngombwa)",
                type="pil"
            )
            buto = gr.Button(
                "🌱 Mpa inama",
                variant="primary",
                elem_classes=["primary-button"]
            )
            gr.Markdown(
                "🔒 Amakuru utanze akoreshwa mu kugufasha kubona inama."
            )

        with gr.Column(scale=5, elem_classes=["panel"]):
            gr.Markdown("## 🌾 Inama ugenewe")
            igisubizo = gr.Markdown(
                "Inama zawe zizagaragara hano umaze gukanda "
                "**Mpa inama**."
            )

    buto.click(
        fn=tanga_inama,
        inputs=[igihingwa, aho, ikibazo, ifoto],
        outputs=igisubizo
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
