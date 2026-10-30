import os
import time
import json
import gradio as gr
from google import genai

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

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
- Tanga ingamba zidateje ibyago: kugenzura niba ibimenyetso biri ku biti byinshi, no kwegera agronome/RAB niba ikibazo gikomeje gukwira.

AMATEGEKO YO KUGARAGAZA INKOMOKO N'URWEGO RW'ICYIZERE:
- Buri gisubizo kigomba kurangira n'agace gato gafite imitwe itatu:
  "Inkomoko y'amakuru:", "Urwego rw'amakuru:", na "Icyitonderwa:".
- Mu "Inkomoko y'amakuru", vuga gusa inyandiko iri muri KNOWLEDGE BASE koko kandi ifitanye isano n'igisubizo. Tanga izina ry'inyandiko n'umuryango wayitangaje. Ntuhimbe URL, umutwe w'inyandiko cyangwa ngo uvuge ko RAB/NISR yemeje ikintu kitanditse mu isoko.
- Niba nta nyandiko yihariye muri KNOWLEDGE BASE ishyigikira igisubizo, andika neza uti: "Nta nyandiko yihariye ya RAB/NISR yemeza iki gisubizo muri data dufite; ni inama rusange yatanzwe na AI."
- "Urwego rw'amakuru" ntirube amanota cyangwa ijanisha rihimbwe. Koresha kimwe muri ibi:
  "Rishingiye ku nyandiko yemewe yavuzwe" cyangwa "Ruracyakeneye kugenzurwa n'umukozi w'ubuhinzi".
- Niba isoko rivuga gusa ko RAB ikora ubushakashatsi ku ngingo, ntukaryerekane nk'aho ryemeje ibimenyetso cyangwa umuti wihariye.
- "Icyitonderwa" gisobanure niba ari amakuru rusange, niba atari isuzuma ry'umurima, cyangwa niba bikwiye kugisha inama agronome.
- Ntukagaragaze Gemini nk'isoko ry'ubumenyi; Gemini ni ikoranabuhanga ryatanze igisubizo, si isoko y'ukuri.
"""

# Soma ubumenyi bw'ubuhinzi bwashyizwe muri knowledge_base.json.
KNOWLEDGE_BASE = {}
try:
    with open("knowledge_base.json", "r", encoding="utf-8") as kb_file:
        KNOWLEDGE_BASE = json.load(kb_file)
except Exception as kb_error:
    print(f"AgriNova knowledge base load warning: {kb_error}")

def get_knowledge_context():
    """Tegura incamake y'ubumenyi n'amasoko yayo yo guha Gemini."""
    if not KNOWLEDGE_BASE:
        return "Nta knowledge base yabonetse; ntuhimbe amakuru yihariye."
    lines = [KNOWLEDGE_BASE.get("title", "AgriNova agriculture knowledge")]
    lines.append(KNOWLEDGE_BASE.get("notice", ""))
    for source in KNOWLEDGE_BASE.get("sources", []):
        lines.append(f"ISOKO: {source.get('organization', 'RAB')} — {source.get('title', '')}")
        lines.append(f"URL: {source.get('url', '')}")
        for fact in source.get("facts", []):
            lines.append(f"- {fact}")
        if source.get("limits"):
            lines.append(f"IMBOGAMIZI: {source['limits']}")
    lines.append("AMATEGEKO: " + " | ".join(KNOWLEDGE_BASE.get("assistant_rules", [])))
    return "\n".join(line for line in lines if line)

def ganira(history, message, igihingwa, akarere, ifoto):
    history = history or []
    if not message or not message.strip():
        return history, history, ""

    # Igisubizo cy'ibanze ku muhinzi utaramenya igihingwa yahinga.
    ikibazo_gito = message.lower().strip()
    amagambo_yo_guhitamo = (
        "sinzi icyo nahinga", "ntazi icyo nahinga", "sinzi icyo nahinga", 
        "sinzi ngo nahinga", "ntazi ngo nahinga", "ndashaka guhinga gusa",
        "nahinga iki", "igihingwa nahinga", "icyo nahinga"
    )
    if any(ijambo in ikibazo_gito for ijambo in amagambo_yo_guhitamo):
        answer = (
            "Ni byiza kubanza guhitamo igihingwa gihuye n'ubutaka bwawe, amazi ufite, "
            "igihembwe cy'ihinga n'isoko ryo kugurishaho. Ntibikwiye kuguhitiramo igihingwa "
            "ntaramenya aho uhinga.\n\n"
            "Urugero, ibigori, ibishyimbo, ibirayi, imboga cyangwa imyumbati bishobora kuba "
            "amahitamo bitewe n'imiterere y'aho uhinga; si ukuvuga ko byose bikwiriye aho uri.\n\n"
            "**Tubanze tumenye aho uhinga:** Uri mu kihe karere n'umurenge? Numbwira aho uhinga, "
            "tuzareba amahitamo ashoboka n'ibyo tugomba kubanza kugenzura.\n\n"
            "**Inkomoko y'amakuru:** Nta nyandiko yihariye ya RAB/NISR muri data dufite yemeza "
            "igihingwa gikwiye umurima wawe; ni ubuyobozi rusange.\n"
            "**Urwego rw'amakuru:** Ruracyakeneye kugenzurwa n'umukozi w'ubuhinzi.\n"
            "**Icyitonderwa:** Ntugure imbuto cyangwa ngo uhitemo igihingwa ushingiye kuri aya makuru gusa; "
            "hakenewe kumenya ubutaka, amazi n'isoko ryo kugurishaho."
        )
        updated = history + [{"role":"user","content":message},{"role":"assistant","content":answer}]
        return updated, updated, ""

    # Igisubizo gihamye ku kibazo rusange cy'igihe ibigori bimara ngo byere.
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
            "Waba uzi izina ry'imbuto wateye, cyangwa ufite ifoto y'ipaki yayo?\n\n"
            "**Inkomoko y'amakuru:** Nta nyandiko yihariye ya RAB/NISR yemeza iki gisubizo muri data dufite; ni inama rusange yatanzwe na AI.\n"
            "**Urwego rw'amakuru:** Ruracyakeneye kugenzurwa n'umukozi w'ubuhinzi.\n"
            "**Icyitonderwa:** Igihe cyo kwera gitandukana bitewe n'ubwoko bw'imbuto n'imiterere y'aho zihingwa."
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

UBUMENYI BWEMEJWE N'AMASOKO YA RAB (koresha gusa ibikenewe ku kibazo):
{get_knowledge_context()}

Igihingwa cyatoranyijwe: {igihingwa}
Akarere/Umurenge: {akarere or 'Ntabwo kavuzwe'}

Amateka y'ikiganiro:
{context}

Ubutumwa bushya bw'umuhinzi:
{message}

Subiza ukurikije amateka y'ikiganiro, kandi niba wabajije umuhinzi ikibazo, koresha igisubizo aguhaye.
Ibisubizo bya AI byabanje bishobora kuba birimo amakosa; ntukabifate nk'amakuru y'ukuri.
Niba ikibazo ari ukumenya igihe ibigori bimara ngo byere kandi ubwoko bw'imbuto butavuzwe,
ntutange umubare. Baza izina ry'imbuto cyangwa usabe ifoto y'ipaki yayo.
Wibuke kurangiza igisubizo n'imitwe itatu isabwa: Inkomoko y'amakuru, Urwego rw'amakuru, Icyitonderwa."""

        contents = [prompt]
        # Ohereza ifoto igihe cyose iriho, n'iyo ikiganiro cyaba cyaratangiye.
        # Ibi bituma umuhinzi ashobora kongeramo ifoto mu butumwa bukurikiyeho.
        if ifoto is not None:
            contents.append(ifoto)
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

CSS = """
.gradio-container {max-width:1500px!important;background:#f7f9f7!important;padding:0!important}
body {background:#f7f9f7!important}
#app-shell {gap:0!important;min-height:95vh}
#sidebar {background:#123d2b!important;color:#fff!important;padding:22px!important;border-radius:0!important;min-height:95vh}
#sidebar h1,#sidebar h2,#sidebar p,#sidebar label {color:#fff!important}
#brand-mark {font-size:30px;font-weight:800;letter-spacing:-1px;color:#fff;margin-bottom:4px}
#brand-sub {color:#d5e9dc;font-size:13px;line-height:1.5;margin-bottom:18px}
#new-chat button {background:#ffffff!important;color:#17452f!important;border:0!important;font-weight:700!important}
#main-panel {padding:24px 4%!important;max-width:1100px!important;margin:0 auto!important}
#topbar {border-bottom:1px solid #e3e9e4;padding-bottom:14px;margin-bottom:16px}
#topbar h2 {margin:0!important;color:#183d2b!important}
#chat-area {background:transparent!important;border:0!important}
#chatbot {border:0!important;background:transparent!important}
#composer {border:1px solid #dce5de!important;border-radius:18px!important;background:white!important;padding:8px!important;box-shadow:0 5px 22px rgba(20,60,38,.06)!important}
#composer textarea {border:0!important;box-shadow:none!important;background:transparent!important}
#send-btn button {background:#176b43!important;color:white!important;border-radius:12px!important}
#hint {color:#718078!important;font-size:12px!important;text-align:center!important}
footer {display:none!important}
@media (max-width: 760px) {
 #sidebar {min-height:auto!important;padding:14px!important}
 #main-panel {padding:14px 10px!important}
 #app-shell {min-height:auto!important}
}
"""


with gr.Blocks(title="AgriNova AI — Umufasha w'Ubuhinzi", theme=gr.themes.Soft(primary_hue="green"), css=CSS) as demo:
    with gr.Row(elem_id="app-shell"):
        with gr.Column(scale=1, min_width=245, elem_id="sidebar"):
            gr.HTML("""
            <div id="brand-mark">🌱 AgriNova AI</div>
            <div id="brand-sub">Umufasha w'umuhinzi w'u Rwanda.<br>Ibibazo by'ubuhinzi, amafoto n'inama zishingiye ku makuru yizewe.</div>
            """)
            clear = gr.Button("＋  Tangira ikiganiro gishya", elem_id="new-chat")
            gr.Markdown("### Ibyo urimo guhinga")
            igihingwa = gr.Dropdown(
                ["Ibigori","Ibishyimbo","Ibirayi","Umuceri","Imyumbati","Ibindi"],
                label="Igihingwa", value="Ibigori"
            )
            akarere = gr.Textbox(
                label="Akarere / Umurenge",
                placeholder="Urugero: Huye (si ngombwa)"
            )
            gr.Markdown("### Ifoto y'igihingwa")
            ifoto = gr.Image(
                label="Ongeraho ifoto yo gusesengura",
                type="pil",
                height=190
            )
            gr.Markdown(
                "<div style='font-size:12px;color:#d5e9dc;line-height:1.5'>"
                "Inama za AI zifasha gufata icyemezo, ariko ntizisimbura isuzuma ry'umukozi w'ubuhinzi."
                "</div>"
            )
        with gr.Column(scale=4, min_width=320, elem_id="main-panel"):
            gr.HTML("""
            <div id="topbar">
              <h2>Ikiganiro cy'ubuhinzi</h2>
              <div style="color:#718078;font-size:13px;margin-top:5px">
                Baza ikibazo icyo ari cyo cyose kijyanye n'igihingwa cyawe.
              </div>
            </div>
            """)
            ibiganiro = gr.Chatbot(
                label="",
                height=540,
                elem_id="chatbot",
                placeholder="🌱 Muraho! Ndi AgriNova AI. Mbwira ikibazo ufite mu murima cyangwa shyiraho ifoto y'igihingwa."
            )
            state = gr.State([])
            with gr.Row(elem_id="composer"):
                ikibazo = gr.Textbox(
                    label="",
                    placeholder="Andika ubutumwa bwawe hano...",
                    lines=2,
                    max_lines=5,
                    scale=8,
                    container=False
                )
                button = gr.Button("Ohereza  ➤", variant="primary", elem_id="send-btn", scale=1)
            gr.HTML("<div id='hint'>AgriNova AI • Ikoranabuhanga rifasha ubuhinzi bw'u Rwanda</div>")
    button.click(
        ganira,
        inputs=[state, ikibazo, igihingwa, akarere, ifoto],
        outputs=[ibiganiro, state, ikibazo]
    )
    ikibazo.submit(
        ganira,
        inputs=[state, ikibazo, igihingwa, akarere, ifoto],
        outputs=[ibiganiro, state, ikibazo]
    )
    clear.click(
        lambda: ([], [], ""),
        outputs=[ibiganiro, state, ikibazo]
    )

if __name__ == "__main__":
    port = int(os.environ.get("PORT", "10000"))
    demo.launch(server_name="0.0.0.0", server_port=port)
