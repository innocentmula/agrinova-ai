import os
import gradio as gr
from google import genai

def tanga_inama(igihingwa, aho, ikibazo, ifoto):
    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        return "Habaye ikibazo: GEMINI_API_KEY ntiyashyizwe muri settings za seriveri."

    if not ikibazo or not ikibazo.strip():
        return "Andika ikibazo ushaka ko tugufashaho."

    try:
        client = genai.Client(api_key=api_key)

        prompt = f"""
Uri AgriNova AI, umujyanama w'ubuhinzi ufasha abahinzi bo mu Rwanda.
Subiza mu Kinyarwanda cyumvikana kandi cyiza.

Igihingwa: {igihingwa or 'Nticyavuzwe'}
Aho umuhinzi aherereye: {aho or 'Ntihavuzwe'}
Ikibazo: {ikibazo}

Tanga:
1. Impamvu zishoboka z'ikibazo.
2. Ibyo umuhinzi yakora ubu.
3. Uburyo bwo gukumira ko ikibazo cyongera kubaho.
4. Igihe agomba kugisha inama umuhanga mu buhinzi.

Ntukemeze indwara udafitiye ibimenyetso bihagije.
Ntugire imiti cyangwa ingano yayo uhamya udafite amakuru ahagije.
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
        print("Ikosa:", str(e))
        return "Habaye ikibazo mu gutanga inama. Ongera ugerageze nyuma."

with gr.Blocks(title="AgriNova AI") as app:
    gr.Markdown("""
    # 🌱 AgriNova AI
    ### Umujyanama w'ubuhinzi mu Kinyarwanda

    Andika ikibazo ufite cyangwa wohereze ifoto
    y'igihingwa kugira ngo ubone inama.
    """)

    igihingwa = gr.Textbox(
        label="Igihingwa",
        placeholder="Urugero: Ibigori, ibishyimbo, imyumbati..."
    )

    aho = gr.Textbox(
        label="Aho uhingira",
        placeholder="Urugero: Gatsibo, Nyagihanga..."
    )

    ikibazo = gr.Textbox(
        label="Ikibazo cy'ubuhinzi",
        placeholder="Sobanura ikibazo ufite...",
        lines=4
    )

    ifoto = gr.Image(
        label="Ifoto y'igihingwa (ushobora kuyisiga ubusa)",
        type="pil"
    )

    buto = gr.Button("Mpa inama", variant="primary")
    igisubizo = gr.Markdown()

    buto.click(
        fn=tanga_inama,
        inputs=[igihingwa, aho, ikibazo, ifoto],
        outputs=igisubizo
    )

if __name__ == "__main__":
    app.launch(
        server_name="0.0.0.0",
        server_port=int(os.environ.get("PORT", 7860))
    )
