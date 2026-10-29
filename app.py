                "conversation_id": conversation_id,
                "user_id": user_id,
                "role": "assistant",
                "content": answer,
            },
        ]).execute()

        db.table("conversations").update({
            "updated_at": datetime.now(timezone.utc).isoformat(),
        }).eq(
            "id", conversation_id
        ).eq(
            "user_id", user_id
        ).execute()

        new_history = history + (
            f"\n\n**Wowe:** {ikibazo.strip()}"
            f"\n\n**AgriNova AI:** {answer}"
        )
        return answer, new_history, conversation_id

    except Exception as e:
        print("AgriNova error:", str(e))
        return (
            "### ⚠️ Habaye ikibazo\n"
            "Igisubizo nticyabashije gutangwa cyangwa kubikwa. "
            "Ongera ugerageze. Niba bikomeje, reba Logs muri Render.",
            history,
            conversation_id,
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
    token_state = gr.State(None)
    user_state = gr.State(None)
    conversation_state = gr.State(None)

    gr.HTML("""
    <div id="hero">
      <div class="hero-inner">
        <div class="brand-mark">🌱</div>
        <div>
          <div class="eyebrow">IKORANABUHANGA RY'UBUHINZI</div>
          <h1>AgriNova AI</h1>
          <p><b>Umujyanama wawe w'ubuhinzi, aho uri hose.</b></p>
          <p>Baza ikibazo mu Kinyarwanda, ubone inama zifasha gufata icyemezo.</p>
          <span class="hero-chip">🌦️ Inama z'ubuhinzi · 💬 Ibiganiro bibikwa · 🇷🇼 Rwanda</span>
        </div>
      </div>
    </div>
    """)
    gr.Markdown("""
    <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(190px,1fr));gap:12px;margin:0 0 20px;">
      <div style="background:white;border:1px solid #e1eae0;border-radius:16px;padding:14px 16px;">
        <div style="font-size:22px">🌱</div><b style="color:#173d2b">Inama z'ubuhinzi</b><div style="font-size:12px;color:#657a69">Sobanura ikibazo cy'igihingwa cyawe</div>
      </div>
      <div style="background:white;border:1px solid #e1eae0;border-radius:16px;padding:14px 16px;">
        <div style="font-size:22px">📷</div><b style="color:#173d2b">Ohereza ifoto</b><div style="font-size:12px;color:#657a69">Ifoto ni uburyo bw'inyongera, si itegeko</div>
      </div>
      <div style="background:white;border:1px solid #e1eae0;border-radius:16px;padding:14px 16px;">
        <div style="font-size:22px">🔐</div><b style="color:#173d2b">Konti yawe</b><div style="font-size:12px;color:#657a69">Ibiganiro byawe bibikwa kuri konti</div>
      </div>
    </div>
    """)

    with gr.Tab("🔐 Konti yanjye"):
        with gr.Row():
            with gr.Column(elem_classes=["panel"]):
                gr.Markdown("## Kwiyandikisha")
                signup_email = gr.Textbox(label="Email")
                signup_password = gr.Textbox(
                    label="Ijambo ry'ibanga",
                    type="password",
                )
                signup_btn = gr.Button(
                    "Fungura konti",
                    variant="primary",
                )

            with gr.Column(elem_classes=["panel"]):
                gr.Markdown("## Kwinjira")
                login_email = gr.Textbox(label="Email")
                login_password = gr.Textbox(
                    label="Ijambo ry'ibanga",
                    type="password",
                )
                login_btn = gr.Button(
                    "Injira",
                    variant="primary",
                )
                logout_btn = gr.Button("Sohoka")

        auth_status = gr.Markdown(
            "**Murakaza neza!** Iyandikishe cyangwa winjire kugira ngo ukoreshe umujyanama w'ubuhinzi.",
            elem_id="auth-status",
        )

    with gr.Tab("🌾 Umujyanama w'ubuhinzi"):
        with gr.Row():
            with gr.Column(scale=6, elem_classes=["panel"]):
                gr.Markdown("## 🧑🏽‍🌾 Tubwire ikibazo cyawe")
                gr.Markdown("Andika amakuru make asobanutse kugira ngo inama irusheho kukugirira akamaro.")
                igihingwa = gr.Textbox(
                    label="🌿 Igihingwa",
                    placeholder="Urugero: Ibigori, ibishyimbo...",
                )
                aho = gr.Textbox(
                    label="📍 Aho uhingira",
                    placeholder="Urugero: Gatsibo, Nyagihanga",
                )
                ikibazo = gr.Textbox(
                    label="💬 Ikibazo cy'ubuhinzi",
                    placeholder="Sobanura ikibazo wabonye...",
                    lines=4,
                )
                ifoto = gr.Image(
                    label="📷 Ifoto y'igihingwa (si ngombwa)",
                    type="pil",
                )
                advice_btn = gr.Button(
                    "🌱 Mpa inama",
                    variant="primary",
                    elem_classes=["primary-button"],
                )

            with gr.Column(scale=5, elem_classes=["panel"], elem_id="answer-panel"):
                gr.Markdown("## 🌾 Inama ugenewe")
                gr.Markdown("Igisubizo kizagaragara hano umaze kohereza ikibazo.")
                answer_box = gr.Markdown("**Uriteguye?** Andika ikibazo cyawe hanyuma ukande *Mpa inama*.")

        gr.Markdown("## 💬 Ibiganiro wabitswe")
        history_box = gr.Markdown(
            "Injira muri konti yawe kugira ngo urebe ibiganiro.",
            elem_id="history-panel",
        )

    signup_btn.click(
        fn=kwiyandikisha,
        inputs=[signup_email, signup_password],
        outputs=[auth_status, token_state, user_state],
    )

    login_btn.click(
        fn=kwinjira,
        inputs=[login_email, login_password],
        outputs=[
            auth_status, token_state, user_state,
            conversation_state, history_box,
        ],
    )

    logout_btn.click(
