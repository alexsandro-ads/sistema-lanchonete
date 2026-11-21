from pedido import criar_resumo_pedido

CARDAPIO = {
    1: {"nome": "X-Burger", "preco": 18.00},
    2: {"nome": "X-Bacon", "preco": 22.00},
    3: {"nome": "Batata Frita", "preco": 12.00},
    4: {"nome": "Refrigerante Lata", "preco": 6.00},
}


def mostrar_cardapio():
    print("\n=== CARDÁPIO ===")
    for codigo, item in CARDAPIO.items():
        print(f"{codigo} - {item['nome']} (R$ {item['preco']:.2f})")


def montar_pedido():
    mostrar_cardapio()
    itens = []

    while True:
        escolha = input("\nDigite o número do lancheitem (ou 'fim' para encerrar): ").strip().lower()
        if escolha == "fim":
            break
        if not escolha.isdigit() or int(escolha) not in CARDAPIO:
            print("Opção inválida. Tente novamente.")
            continue

        item = CARDAPIO[int(escolha)]
        qtd_texto = input(f"Quantidade de {item['nome']}: ").strip()
        if not qtd_texto.isdigit() or int(qtd_texto) <= 0:
            print("Quantidade inválida.")
            continue

        itens.append({"nome": item["nome"], "preco": item["preco"], "qtd": int(qtd_texto)})
        print(f"Adicionado: {qtd_texto}x {item['nome']}")

    if not itens:
        print("Nenhum item selecionado. Pedido cancelado.")
        return

    endereco_loja = input("\nEndereço da lanchonete: ").strip()
    endereco_cliente = input("Endereço de entrega do cliente: ").strip()

    print("\nFormas de pagamento: Pix | Cartao | Dinheiro")
    forma_pagamento = input("Escolha a forma de pagamento: ").strip()

    troco_para = None
    if forma_pagamento.lower() == "dinheiro":
        troco_texto = input("Precisa de troco para quanto? (ex: 50.00 ou deixe vazio): ").strip()
        if troco_texto:
            troco_para = float(troco_texto.replace(",", "."))

    resumo = criar_resumo_pedido(
        itens=itens,
        endereco_loja=endereco_loja,
        endereco_cliente=endereco_cliente,
        forma_pagamento=forma_pagamento,
        troco_para=troco_para,
    )

    if "erro" in resumo:
        print(f"\nErro ao calcular entrega: {resumo['erro']}")
        return

    print("\n=== RESUMO DO PEDIDO ===")
    for item in itens:
        total_item = item["preco"] * item["qtd"]
        print(f"- {item['qtd']}x {item['nome']}: R$ {total_item:.2f}")

    print(f"Subtotal dos itens: R$ {resumo['subtotal']:.2f}")
    print(f"Distância estimada: {resumo['distancia_km']} km")
    print(f"Valor da entrega: R$ {resumo['frete']:.2f}")
    print(f"Total a pagar: R$ {resumo['total']:.2f}")
    print(f"Forma de pagamento: {resumo['pagamento']}")

    if resumo["troco"] is not None:
        print(f"Troco a levar: R$ {resumo['troco']:.2f}")

    print(f"Abrir mapa para entrega: {resumo['link_mapa']}")


if __name__ == "__main__":
    montar_pedido()
