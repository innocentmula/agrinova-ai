import os
import time
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
Subiza mu Kinyarwanda cyumvikana, mu buryo bugufi, busobanutse kandi bufatika.

AMATEGEKO YO KUTIHIMBIRA AMAKURU:
- Ntuhimbe imibare, igihe cy'ikura ry'igihingwa, amakuru y'ikirere, ibipimo by'ubutaka,
  indwara, udukoko cyangwa amabwiriza y'imiti.
- Ntuvuge ko akarere runaka gafite ubutaka bwa aside nyinshi cyangwa ikindi kiranga ubutaka
  utabonye ibipimo cyangwa isoko ryizewe ribyemeza.
- Ntukavuge ko amakuru rusange areba byanze bikunze akarere k'umuhinzi.
- Niba utizeye umubare cyangwa igisubizo, bivuge mu buryo bweruye aho gutanga umubare usa n'uwizewe.
- Tandukanya amakuru rusange n'amakuru yemejwe ku murima cyangwa akarere runaka.

IBIBAZO BYEREKEYE IGIHE IGIHINGWA KIMARA NGO KIYARE:
- Sobanura ko igihe cyo kwera giterwa n'ubwoko bw'imbuto, aho gihingwa, ikirere n'uko cyitaweho.
- Tanga igihe cyegeranye gusa niba ufite ubumenyi bwizewe; ugishyireho ko ari ikigereranyo,
  kandi ntukakigire umwihariko wa Huye cyangwa akarere runaka utabifitiye gihamya.
- Niba ubwoko bw'imbuto butazwi, ntutange umubare w'iminsi cyangwa amezi nk'aho wizewe.
  Banza ubaze izina ry'imbuto cyangwa usabe ifoto y'ipaki.
- Ku kibazo rusange cyo kumenya igihe ibigori bimara ngo byere, niba ubwoko bw'imbuto butatanzwe,
  subiza mu magambo make ko igihe gitandukana bitewe n'imbuto n'uko zitaweho, hanyuma ubaze
  izina ry'imbuto. Ntuhimbe intera y'iminsi cyangwa amezi.
- Ntukavuge ko umuhinzi ari i Huye cyangwa ahandi keretse yabihisemo cyangwa abyivugiye ubwe.
  Niba akarere katavuzwe, vuga ko katavuzwe.
- Ibisubizo bya AI byabanje si gihamya; ntukabisubiremo nk'ukuri keretse umuhinzi abyemeje cyangwa
  hari isoko ryizewe ribyemeza.
- Tandukanya ikibazo cyo kumenya igihe gisanzwe cyo kwera n'icyo kumenya igihe imyaka iri mu murima
  imaze; ntukibwire icyo umuhinzi yashakaga atakivuze.

UBURYO BWO GUSUBIZA:
- Ku kibazo cyoroshye, banza ugisubize mu magambo make; ntukoreshe imitwe myinshi cyangwa
  urutonde rurerure rudakenewe.
- Niba amakuru adahagije, baza ikibazo kimwe cy'ingenzi gikurikiraho.
- Jya ukurikiza igihingwa n'akarere umukoresha yahisemo. Niba ikibazo kivuga ikindi gihingwa,
  banza umubaze niba ashaka guhindura igihingwa, aho kwivanga.
- Ku kibazo cy'indwara cyangwa ibyonnyi, tanga impamvu zishoboka gusa; ntukemeze isuzuma utabifitiye gihamya.
- Ku isesengura ry'ifoto, banza uvuge gusa ibimenyetso bigaragara koko: ibara, imiterere, aho biri ku kibabi n'uko bikwirakwijwe. Ntukavuge ko wabonye ikintu kitagaragara.
- Tandukanya ibyo ubona ku ifoto n'indwara ushobora gukeka. Tanga indwara 1-3 zishoboka gusa, usobanure ko bidahagije kwemeza indwara ukoresheje ifoto imwe.
- Ntukitiranye indwara zisa. Niba ibimenyetso bidahagije, saba ifoto isobanutse y'ikibabi cyose n'iyegereye ibikomere, cyangwa ubaze ikibazo kimwe gifasha gutandukanya indwara.
- Koresha ijambo 'imiyege' cyangwa 'indwara ziterwa n'imiyege' aho gukoresha 'ubuhumyi' mu gusobanura fungal diseases.
- Ntukavuge akarere cyangwa umurenge utavuzwe n'umuhinzi cyangwa utatoranyijwe muri porogaramu. Niba akarere katavuzwe, vuga ko katavuzwe; ntukihimbire Huye.
- Ntugire inama rusange yo gutwika amababi cyangwa ibisigazwa by'ibihingwa. Saba kubanza kugisha inama agronome ku buryo bwizewe bwo kubikuraho no kubijugunya.
- Ntugire inama yo gukoresha fungicide, pesticide cyangwa ifumbire runaka utabanje kumenya neza ikibazo n'amabwiriza yemewe. Ntutange urugero rw'umuti nk'aho ari wo ukwiye.
- Tanga ingamba zidateje ibyago: kugenzura niba ibimenyetso biri ku biti byinshi, kwirinda gukorera mu murima igihe amababi atose, no kwegera agronome/RAB niba ikibazo gikomeje gukwira.
- Tanga icyo umuhinzi yakora ubu n'igihe yakwiyambaza agronome/RAB igihe ari ngombwa.
"""

def ganira(history, message, igihingwa, akarere, ifoto):
    history = history or []
    if not message or not message.strip():
        return history, history, ""

    # Igisubizo gihamye ku kibazo rusange cy'igihe ibigori bimara ngo byere.
    # Ibi birinda Gemini gutanga imibare idafite isoko cyangwa kwihimbira akarere.
    ikibazo_gito = message.lower()
    amagambo_yigihe = ("bimara igihe", "igihe bimara", "ngo byere", "igihe ibigori", "byera ryari")
    ni_ikibazo_cyigihe = any(ijambo in ikibazo_gito for ijambo in amagambo_yigihe)
    ni_ibigori = (igihingwa == "Ibigori") or any(x in ikibazo_gito for x in ("ibigori", "ikigori"))
    niba_nta_mateka = len(history) == 0
    niba_nta_bwoko_bwimbuto = not any(x in ikibazo_gito for x in ("hybrid", "imbuto ya", "izina ry'imbuto"))
    if ni_ikibazo_cyigihe and ni_ibigori and niba_nta_mateka and niba_nta_bwoko_bwimbuto:
        answer = (
            "Ibigori ntibyera mu gihe kimwe byose. Igihe bimara giterwa n'ubwoko bw'imbuto, "
            "ikirere n'uko byitaweho. Sinakwemeza umubare w'iminsi cyangwa amezi ntazi ubwoko "
            "bw'imbuto wateye.\n\n"
            "Waba uzi izina ry'imbuto wateye, cyangwa ufite ifoto y'ipaki yayo?"
        )
        updated = history + [{"role":"user","content":message},{"role":"assistant","content":answer}]
        return updated, updated, ""
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

Subiza ukurikije amateka y'ikiganiro, kandi niba wabajije umuhinzi ikibazo, koresha igisubizo aguhaye.
Ibisubizo bya AI byabanje bishobora kuba birimo amakosa; ntukabifate nk'amakuru y'ukuri.
Niba ikibazo ari ukumenya igihe ibigori bimara ngo byere kandi ubwoko bw'imbuto butavuzwe,
ntutange umubare. Baza izina ry'imbuto cyangwa usabe ifoto y'ipaki yayo."""
        contents = [prompt]
        if ifoto is not None and not history:
            contents.append(ifoto)
        # Ongera ugerageze mu gihe Gemini ihuye n'ubwinshi bw'abayikoresha.
        # Gutegereza 1, 2, na 4 seconds bigabanya gusubiramo request nyinshi icyarimwe.
        response = None
        last_error = None
        for attempt in range(4):
            try:
                response = client.models.generate_content(
                    model="gemini-3.8-flash",
                    contents=contents
                )
                last_error = None
                break
            except Exception as e:
                last_error = e
                error_text = str(e).lower()
                temporary_error = any(term in error_text for term in (
                    "503", "unavailable", "high demand",
                    "429", "resource_exhausted", "rate limit",
                    "500", "502", "504", "temporarily"
                ))
                if not temporary_error or attempt == 3:
                    raise
                time.sleep(2 ** attempt)

        if last_error is not None:
            raise last_error
        answer = response.text or "Ntabwo nabashije kubona igisubizo. Ongera ugerageze."
    except Exception as e:
        print(f"AgriNova Gemini error: {type(e).__name__}: {e}")
        error_text = str(e).lower()
        temporary_error = any(term in error_text for term in (
            "503", "unavailable", "high demand",
            "429", "resource_exhausted", "rate limit",
            "500", "502", "504", "temporarily"
        ))
        if temporary_error:
            answer = (
                "Serivisi ya AI iri kwakira ibyifuzo byinshi muri aka kanya. "
                "Nagerageje kongera kohereza ikibazo ariko ntibyashobotse. "
                "Tegereza akanya gato wongere ugerageze; ntukeneye gutangira ikiganiro bundi bushya."
            )
        else:
            answer = (
                "Habaye ikibazo mu kubona igisubizo cya AI. "
                "Ongera ugerageze nyuma y'akanya. Niba bikomeje, tubimenyeshe."
            )
    updated = history + [{"role":"user","content":message},{"role":"assistant","content":answer}]
    return updated, updated, ""

with gr.Blocks(title="AgriNova AI") as demo:
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
    ibiganiro = gr.Chatbot(label="Ikiganiro na AgriNova AI", height=420)
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
    demo.launch(server_name="0.0.0.0", server_port=port, theme=gr.themes.Soft(primary_hue="green"), css=CSS)
