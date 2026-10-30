import os
import gradio as gr
from google import genai

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

CSS = """
.gradio-container {max-width:1100px!important;background:#f3f8f2!important}
#hero {background:linear-gradient(120deg,#103d2b,#23804d);color:white;padding:28px;border-radius:20px;margin-bottom:18px}
#hero h1 {color:white!important}
"""

SYSTEM_PROMPT = """
Uri AgriNova AI, umujyanama w'ubuhinzi ufasha abahinzi bo mu Rwanda.
Subiza mu Kinyarwanda cyumvikana, mu buryo bugufi kandi bufatika.
Tanga impamvu zishoboka gusa, ntukemeze indwara utabifitiye gihamya.
Ntuhimbe imibare, amakuru y'ikirere, ibipimo by'ubutaka cyangwa amabwiriza y'imiti.
Ntuvuge ko akarere gafite ubutaka bwa aside nyinshi utabonye ibipimo.
Niba amakuru adahagije, baza ikibazo kimwe cyangwa bibiri by'ingenzi.
Jya ukurikiza igihingwa n'akarere umukoresha yahisemo. Niba ikibazo kivuga ikindi gihingwa,
banza umubaze niba ashaka guhindura igihingwa, aho kwivanga.
Mu gisubizo, tanga: impamvu zishoboka, icyo yakora ubu, n'igihe yakwiyambaza agronome/RAB.
"""

def ganira(history, message, igihingwa, akarere, ifoto):
    history = history or []
    if not message or not message.strip():
        return history, history, ""
    if not GEMINI_API_KEY:
        history = history + [{"role":"assistant","content":"GEMINI_API_KEY ntiyashyizwe muri Render. Nyabuneka genzura Environment Variables."}]
        return history, history, ""
    try:
        client = genai.Client(api_key=GEMINI_API_KEY)
        transcript = []
        for item in history:
            role = "Umuhinzi" if item["role"] == "user" else "AgriNova AI"
            transcript.append(f"{role}: {item['content']}")
        context = "\n".join(transcript[-12:])
        prompt = f"""{SYSTEM_PROMPT}

Igihingwa cyatoranyijwe: {igihingwa}
Akarere/Umurenge: {akarere or 'Ntabwo kavuzwe'}

Amateka y'ikiganiro:
{context}

Ubutumwa bushya bw'umuhinzi:
{message}

Subiza ukurikije amateka y'ikiganiro, kandi niba wabajije umuhinzi ikibazo, koresha igisubizo aguhaye."""
        contents = [prompt]
        if ifoto is not None and not history:
            contents.append(ifoto)
        response = client.models.generate_content(
            model="gemini-3.8-flash",
            contents=contents
        )
        answer = response.text or "Ntabwo nabashije kubona igisubizo. Ongera ugerageze."
    except Exception as e:
        answer = "Habaye ikibazo mu kubona igisubizo cya AI. Ongera ugerageze. " + str(e)[:250]
    updated = history + [{"role":"user","content":message},{"role":"assistant","content":answer}]
    return updated, updated, ""

with gr.Blocks(title="AgriNova AI", theme=gr.themes.Soft(primary_hue="green"), css=CSS) as demo:
    gr.HTML("""
    <div id="hero">
      <h1>🌱 AgriNova AI</h1>
      <p>Umufasha w'umuhinzi w'u Rwanda — inama z'ubuhinzi mu Kinyarwanda.</p>
    </div>
    """)
    gr.Markdown("### Tangira ikiganiro ku kibazo ufite mu murima")
    with gr.Row():
        igihingwa = gr.Dropdown(
            ["Ibigori","Ibishyimbo","Ibirayi","Umuceri","Imyumbati","Ibindi"],
            label="Igihingwa", value="Ibigori"
        )
        akarere = gr.Textbox(label="Akarere / Umurenge", placeholder="Urugero: Huye")
    ifoto = gr.Image(label="Ifoto y'igihingwa (ushobora kuyishyiraho mbere yo gutangira)", type="pil")
    ibiganiro = gr.Chatbot(label="Ikiganiro na AgriNova AI", type="messages", height=420)
    state = gr.State([])
    ikibazo = gr.Textbox(
        label="Andika ikibazo cyangwa igisubizo ku byo AI yakubajije",
        placeholder="Urugero: Ibigori bimaze ibyumweru 5 bitewe...",
        lines=2
    )
    with gr.Row():
        button = gr.Button("Ohereza", variant="primary")
        clear = gr.Button("Tangira ikiganiro gishya")
    button.click(ganira, inputs=[state, ikibazo, igihingwa, akarere, ifoto],
                 outputs=[ibiganiro, state, ikibazo])
    ikibazo.submit(ganira, inputs=[state, ikibazo, igihingwa, akarere, ifoto],
                   outputs=[ibiganiro, state, ikibazo])
    clear.click(lambda: ([], [], ""), outputs=[ibiganiro, state, ikibazo])
    gr.Markdown(
        "Icyitonderwa: Inama za AI si isuzuma ryemejwe n'umuhanga. "
        "Ku kibazo gikomeye, ganira n'umukozi w'ubuhinzi cyangwa RAB."
    )

if __name__ == "__main__":
    port = int(os.environ.get("PORT", "10000"))
    demo.launch(server_name="0.0.0.0", server_port=port)
