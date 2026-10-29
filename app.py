import os

import gradio as gr
from google import genai

CSS = """
.gradio-container {
    max-width: 1120px !important;
    margin: auto !important;
    background: #f4f8f2 !important;
    font-family: Inter, system-ui, sans-serif !important;
}
#hero {
    background: linear-gradient(125deg, #103d2b, #26734d);
    color: white;
    padding: 30px 24px;
    border-radius: 22px;
    text-align: center;
    margin: 8px 0 20px;
}
#hero h1 { color: white !important; font-size: clamp(30px, 5vw, 44px) !important; }
#hero p { color: #e5f3e8 !important; }
.panel {
    background: white !important;
    border: 1px solid #dce8da !important;
    border-radius: 18px !important;
    padding: 18px !important;
}
.primary-button {
    background: #247447 !important;
    color: white !important;
    border-radius: 12px !important;
    min-height: 50px !important;
    font-weight: 700 !important;
}
footer { display: none !important; }
"""

def tanga_inama(igihingwa, aho, ikibazo, ifoto):
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        return (
            "### ⚠️ Gemini API key ntiyabonetse\n"
            "Shyira GEMINI_API_KEY muri Environment Variables za Render."
        )

    if not ikibazo or not ikibazo.strip():
        return "### ✍️ Andika ikibazo\nSobanura ikibazo wabonye ku gihingwa cyawe."

    try:
        client = genai.Client(api_key=api_key)
        prompt = f"""
Uri AgriNova AI, umujyanama w'ubuhinzi ufasha abahinzi bo mu Rwanda.
Subiza mu Kinyarwanda cyumvikana kandi cyoroshye gukurikiza.

Amakuru y'umuhinzi:
- Igihingwa: {igihingwa.strip() if igihingwa else 'Nticyavuzwe'}
- Aho aherereye: {aho.strip() if aho else 'Ntihavuzwe'}
- Ikibazo: {ikibazo.strip()}

Tanga igisubizo gitondetse:
1. Impamvu zishoboka z'ikibazo.
2. Ibyo umuhinzi yakora ubu.
3. Uburyo bwo gukumira ko ikibazo cyongera kubaho.
4. Igihe agomba kugisha inama umuhanga mu buhinzi.

Ntukemeze indwara udafitiye ibimenyetso bihagije.
Ntugire umuti cyangwa ingano yawo uhamya udafite amakuru ahagije.
Niba amakuru adahagije, baza ibibazo bisobanutse.
Niba hari ifoto, sobanura gusa ibimenyetso bigaragara kuri yo.
Ntuhimbe amakuru ya NISR cyangwa RAB.
"""
        contents = [prompt]
        if ifoto is not None:
            contents.append(ifoto)

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=contents,
        )
        answer = getattr(response, "text", None)
        if answer and answer.strip():
            return answer.strip()
        return "Ntabwo habonetse igisubizo. Ongera ugerageze."
    except Exception as error:
        print("AgriNova AI error:", repr(error))
        return (
            "### ⚠️ Habaye ikibazo mu gutanga inama\n"
            "Ongera ugerageze nyuma gato. Niba bikomeje, genzura GEMINI_API_KEY "
            "n'uko Gemini API iri gukora."
        )


with gr.Blocks(
    title="AgriNova AI | Umujyanama w'Ubuhinzi",
    theme=gr.themes.Soft(
        primary_hue="green",
        secondary_hue="lime",
        neutral_hue="slate",
    ),
    css=CSS,
) as app:
    gr.HTML(
        """
        <div id="hero">
            <div style="font-size:46px;">🌱</div>
            <h1>AgriNova AI</h1>
            <p><b>Umujyanama w'ubuhinzi mu Kinyarwanda</b></p>
            <p>Andika ikibazo cyangwa wohereze ifoto y'igihingwa kugira ngo ubone ubufasha.</p>
        </div>
        """
    )

    with gr.Row():
        with gr.Column(scale=6, elem_classes=["panel"]):
            gr.Markdown("## 🧑🏽‍🌾 Tubwire ibijyanye n'igihingwa cyawe")
            igihingwa = gr.Textbox(
                label="🌿 Igihingwa",
                placeholder="Urugero: Ibigori, ibishyimbo, imyumbati...",
            )
            aho = gr.Textbox(
                label="📍 Aho uhingira",
                placeholder="Urugero: Huye, Gatsibo, Nyagihanga...",
            )
            ikibazo = gr.Textbox(
                label="💬 Ikibazo cy'ubuhinzi",
                placeholder="Sobanura ibimenyetso wabonye n'igihe byatangiriye...",
                lines=5,
            )
            ifoto = gr.Image(
                label="📷 Ifoto y'igihingwa (si ngombwa)",
                type="pil",
            )
            buto = gr.Button(
                "🌱 Mpa inama",
                variant="primary",
                elem_classes=["primary-button"],
            )
            gr.Markdown("<small>Ifoto si ngombwa. Ntushyiremo amakuru y'ibanga.</small>")

        with gr.Column(scale=5, elem_classes=["panel"]):
            gr.Markdown("## 🌾 Inama ugenewe")
            igisubizo = gr.Markdown(
                "Inama zawe zizagaragara hano umaze gukanda **Mpa inama**."
            )

    buto.click(
        fn=tanga_inama,
        inputs=[igihingwa, aho, ikibazo, ifoto],
        outputs=igisubizo,
    )

    gr.Markdown(
        """
        ---
        <div style="text-align:center; color:#45634f;">
            <b>AgriNova AI</b> 🌱<br>
            Ikoranabuhanga rifasha ubuhinzi gutera imbere.
            <br><small>Inama za AI zishobora kutaba zuzuye kandi si isuzuma ryemewe.
            Ku kibazo gikomeye, baza umuhanga mu buhinzi.</small>
        </div>
        """
    )

if __name__ == "__main__":
    app.launch(
        server_name="0.0.0.0",
        server_port=int(os.environ.get("PORT", 7860)),
    )
