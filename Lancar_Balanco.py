import requests
import time
import streamlit as st


def Lancamento (CodOmie, Data, Qtde, Obs, Valor, max_tentativas=3, delay=5):
    url = "https://app.omie.com.br/api/v1/estoque/ajuste/"

    payload = {
        "call": "IncluirAjusteEstoque",
        "app_key": "4292462707533",
        "app_secret": "281e971011633384d72e052936906c57",
        "param":[
            {
            "codigo_local_estoque": 9516494176, #9516494176, #Sede
            "id_prod": CodOmie, #Codigo Produto
            "data": Data,
            "quan": Qtde,
            "obs": Obs,
            "origem": "AJU",
            # AJU - Ajuste Manual (Mansear / Kuara Local)
            "tipo": "SLD",
            # TRF - Transferencia de Estoque (Kuara Sede >> KUara Local)
            # SLD - Balanco Kuara (Kuara Local)
            # SAI - Transferencia da Sede para os Barcos
            #"codigo_local_estoque_destino": 9516494176, #Local - Colocar no script das transferencias do Kuara
            "motivo": "INV",
            # TRF - Transferencia entre locais (Kuara Local)
            # INV - Ajuste por Inventario (Mansear e Kuara Local)
            "valor": Valor #Só insere valor quanto é SAI - quando é TRF pode retirar o valor
            }
        ]
    }

    headers = {
                'Content-Type': 'application/json'
            }
    tentativas = 0
    while tentativas < max_tentativas:
        response = requests.post(url, headers=headers, json=payload)

        if response.status_code == 200:
            data = response.json()
            return data
        else:
            print(f"Tentativa {tentativas + 1} falhou com status {response.status_code}. Tentando novamente em {delay} segundos...")
            tentativas += 1
            time.sleep(delay)
            
    st.warning("Erro ao realizar Lancamento após várias tentativas, TENTE NOVAMENTE")
    return None
            