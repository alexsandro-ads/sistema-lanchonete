import streamlit as st
from pedido import criar_resumo_pedido

st.set_page_config(page_title="Lanchonete Express", page_icon="🍔", layout="wide")

CARDAPIO = [
    {"id": 1, "nome": "X-Burger", "desc": "Pão brioche, hambúrguer artesanal, queijo e molho especial.", "preco": 18.00},
    {"id": 2, "nome": "X-Bacon", "desc": "Pão brioche, hambúrguer, queijo cheddar e bacon crocante.", "preco": 22.00},
    {"id": 3, "nome": "Batata Frita", "desc": "Porção dourada e crocante com tempero da casa.", "preco": 12.00},
    {"id": 4, "nome": "Refrigerante Lata", "desc": "Lata 350ml bem gelada.", "preco": 6.00},
]

if "carrinho" not in st.session_state:
    st.session_state.carrinho = {item["id"]: 0 for item in CARDAPIO}

st.markdown(
    """
    <style>
    .card-lanche {
        background: #ffffff;
        border: 1px solid #eceff4;
        border-radius: 14px;
        padding: 16px;
        margin-bottom: 12px;
        box-shadow: 0 2px 8px rgba(15, 23, 42, 0.04);
    }
    .preco-tag {
        color: #16a34a;
        font-weight: 700;
        font-size: 1.05rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("🍔 Lanchonete Express")
st.caption("Monte o pedido, calcule a entrega por distância, escolha o pagamento e abra o mapa para o entregador.")

col_menu, col_resumo = st.columns([1.45, 1], gap="large")

with col_menu:
    st.subheader("Cardápio")
    for item in CARDAPIO:
        item_id = item["id"]
        with st.container():
            st.markdown(
                f"""
                <div class="card-lanche">
                    <strong>{item["nome"]}</strong> <span class="preco-tag">— R$ {item["preco"]:.2f}</span><br>
                    <small style="color:#64748b;">{item["desc"]}</small>
                </div>
                """,
                unsafe_allow_html=True,
            )
            c1, c2, c3 = st.columns([1, 1, 2])
            with c1:
                if st.button("➖", key=f"minus_{item_id}", use_container_width=True):
                    st.session_state.carrinho[item_id] = max(0, st.session_state.carrinho[item_id] - 1)
                    st.rerun()
            with c2:
                st.markdown(
                    f"<div style='text-align:center;padding-top:6px;font-weight:600;'>Qtd: {st.session_state.carrinho[item_id]}</div>",
                    unsafe_allow_html=True,
                )
            with c3:
                if st.button("➕ Adicionar", key=f"plus_{item_id}", use_container_width=True):
                    st.session_state.carrinho[item_id] += 1
                    st.rerun()

with col_resumo:
    st.subheader("Entrega e Pagamento")

    itens_selecionados = []
    for item in CARDAPIO:
        qtd = st.session_state.carrinho[item["id"]]
        if qtd > 0:
            itens_selecionados.append({"nome": item["nome"], "preco": item["preco"], "qtd": qtd})

    if itens_selecionados:
        for it in itens_selecionados:
            st.write(f"• **{it['qtd']}x** {it['nome']} — R$ {it['preco'] * it['qtd']:.2f}")
    else:
        st.info("Adicione pelo menos um item do cardápio.")

    endereco_loja = st.text_input("Endereço da lanchonete", placeholder="Ex.: Centro, Paudalho, PE")
    endereco_cliente = st.text_input("Endereço de entrega do cliente", placeholder="Ex.: Alto Dois Irmãos, Paudalho, PE")

    forma_pagamento = st.selectbox("Forma de pagamento", ["Pix", "Cartao", "Dinheiro"])

    troco_para = None
    if forma_pagamento == "Dinheiro":
        troco_input = st.text_input("Troco para quanto? (R$)", placeholder="Ex.: 50.00")
        if troco_input.strip():
            try:
                troco_para = float(troco_input.replace(",", "."))
            except ValueError:
                st.warning("Digite um valor numérico válido para o troco.")

    if st.button("Calcular Pedido e Gerar Rota", type="primary", use_container_width=True):
        if not itens_selecionados:
            st.error("Selecione ao menos um item antes de calcular.")
        elif not endereco_loja.strip() or not endereco_cliente.strip():
            st.error("Preencha o endereço da lanchonete e o do cliente.")
        else:
            with st.spinner("Calculando distância e frete..."):
                resumo = criar_resumo_pedido(
                    itens=itens_selecionados,
                    endereco_loja=endereco_loja.strip(),
                    endereco_cliente=endereco_cliente.strip(),
                    forma_pagamento=forma_pagamento,
                    troco_para=troco_para,
                )

            if "erro" in resumo:
                st.error(resumo["erro"])
            else:
                st.success("Pedido calculado com sucesso!")
                m1, m2, m3 = st.columns(3)
                m1.metric("Distância", f"{resumo['distancia_km']} km")
                m2.metric("Frete", f"R$ {resumo['frete']:.2f}")
                m3.metric("Total", f"R$ {resumo['total']:.2f}")

                st.write(f"**Pagamento:** {resumo['pagamento']}")
                if resumo["troco"] is not None:
                    st.write(f"**Troco a levar:** R$ {resumo['troco']:.2f}")

                st.link_button("🗺️ Abrir Mapa para Entrega", resumo["link_mapa"], use_container_width=True)