import os
import gradio as gr
from google import genai

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

CSS = """
.gradio-container {max-width:1100px!important;background:#f3f8f2!important}
#hero {background:linear-gradient(120deg,#103d2b,#23804d);color:white;padding:28px;border-radius:20px;margin-bottom:18px}
#hero h1 {color:white!important}
"""

def agrinova(igihingwa, akarere, ikibazo, ifoto):
    if not ikibazo or not ikibazo.strip():
        return "Andika ikibazo ufite ku gihingwa cyawe kugira ngo ngufashe."
    if not GEMINI_API_KEY:
        return "Ikibazo: GEMINI_API_KEY ntiyashyizwe muri Render. Nyabuneka genzura Environment Variables."
    try:
        client = genai.Client(api_key=GEMINI_API_KEY)
        prompt = f"""
Uri AgriNova AI, umujyanama w'ubuhinzi ufasha abahinzi bo mu Rwanda.
Subiza mu Kinyarwanda cyumvikana, mu buryo bugufi kandi bufatika.
Igihingwa: {igihingwa}
Akarere: {akarere}
Ikibazo cy'umuhinzi: {ikibazo}

Tanga:
1. Ibisobanuro bishoboka by'ikibazo (ntuvuge ko ari isuzuma ryizewe niba bidashoboka).
2. Ibyo umuhinzi yakora ubu, mu ntambwe zoroshye.
3. Igihe agomba kugisha inama agronome cyangwa umukozi wa RAB.
Ntuhimbe imibare, amakuru y'ikirere, cyangwa amabwiriza y'imiti. Niba amakuru adahagije, baza ibibazo bisobanutse.
"""
        contents = [prompt]
        if ifoto is not None:
            contents.append(ifoto)
        response = client.models.generate_content(
            model="gemini-3.8-flash",
            contents=contents
        )
        return response.text or "Ntabwo nabashije kubona igisubizo. Ongera ugerageze."
    except Exception as e:
        return "Habaye ikibazo mu kubona igisubizo cya AI. Ongera ugerageze nyuma gato. " + str(e)[:350]

with gr.Blocks(title="AgriNova AI", theme=gr.themes.Soft(primary_hue="green"), css=CSS) as demo:
    gr.HTML("""
    <div id="hero">
      <h1>🌱 AgriNova AI</h1>
      <p>Umufasha w'umuhinzi w'u Rwanda — inama z'ubuhinzi mu Kinyarwanda.</p>
    </div>
    """)
    gr.Markdown("### Tubwire ikibazo ufite mu murima")
    with gr.Row():
        igihingwa = gr.Dropdown(
            ["Ibigori","Ibishyimbo","Ibirayi","Umuceri","Imyumbati","Ibindi"],
            label="Igihingwa", value="Ibigori"
        )
        akarere = gr.Textbox(label="Akarere / Umurenge", placeholder="Urugero: Huye")
    ikibazo = gr.Textbox(
        label="Sobanura ikibazo cyawe",
        placeholder="Urugero: Amababi y'ibigori yahindutse umuhondo...",
        lines=4
    )
    ifoto = gr.Image(label="Ongeraho ifoto y'igihingwa (si ngombwa)", type="pil")
    button = gr.Button("Shaka inama", variant="primary")
    igisubizo = gr.Markdown(label="Inama za AgriNova AI")
    button.click(agrinova, inputs=[igihingwa, akarere, ikibazo, ifoto], outputs=igisubizo)
    gr.Markdown(
        "Icyitonderwa: Inama za AI si isuzuma ryemejwe n'umuhanga. "
        "Ku kibazo gikomeye, ganira n'umukozi w'ubuhinzi cyangwa RAB."
    )

if __name__ == "__main__":
    port = int(os.environ.get("PORT", "10000"))
    demo.launch(server_name="0.0.0.0", server_port=port)
