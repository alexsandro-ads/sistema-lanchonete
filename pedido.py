cat << 'EOF' > pedido.py
from entrega import calcular_entrega


def criar_resumo_pedido(itens, endereco_loja, endereco_cliente, forma_pagamento, troco_para=None):
    subtotal = sum(item["preco"] * item["qtd"] for item in itens)
    distancia, frete, link_mapa = calcular_entrega(endereco_loja, endereco_cliente)

    if frete is None:
        return {"erro": link_mapa}

    total = round(subtotal + frete, 2)
    troco = None
    if forma_pagamento.lower() == "dinheiro" and troco_para is not None:
        troco = round(float(troco_para) - total, 2)

    return {
        "subtotal": subtotal,
        "distancia_km": distancia,
        "frete": frete,
        "total": total,
        "pagamento": forma_pagamento,
        "troco": troco,
        "link_mapa": link_mapa,
    }
EOF