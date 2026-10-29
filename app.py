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
        fn=gusohoka,
        inputs=[],
        outputs=[
            auth_status, token_state, user_state,
            conversation_state, history_box,
        ],
    )

    advice_btn.click(
        fn=tanga_inama,
        inputs=[
            igihingwa, aho, ikibazo, ifoto,
            token_state, user_state, conversation_state, history_box,
        ],
        outputs=[answer_box, history_box, conversation_state],
    )

    gr.Markdown("""
    <div id="footer-note">
      <b>AgriNova AI 🌱</b><br>
      Ikoranabuhanga rifasha ubuhinzi gutera imbere.<br>
      Inama zitangwa na AI zishobora kutaba zuzuye; ku kibazo gikomeye, baza umuhanga mu buhinzi.
    </div>
    """)


if __name__ == "__main__":
    app.launch(
        server_name="0.0.0.0",
        server_port=int(os.environ.get("PORT", 7860)),
    )
