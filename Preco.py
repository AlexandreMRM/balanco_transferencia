import requests
import pandas as pd
import streamlit as st

def BuscaPreco (Cod, Data):

    url = "https://app.omie.com.br/api/v1/estoque/resumo/"

    payload = {
        "call": "ObterEstoqueProduto",
        "app_key": "4292462707533",
        "app_secret": "281e971011633384d72e052936906c57",
        "param": [
            {
                "cCodigo": Cod,
                "dDia": Data
            }
        ]
    }

    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.post(url, headers=headers, json=payload)

    if response.status_code != 200:
        st.write(f"Erro na requisição: {response.status_code}")
    
    data = response.json()
    cCodigo = data.get('cCodigo', '')
    cDescricao = data.get('cDescricao', '')
    listaEstoque = data.get('listaEstoque', [])

    Preco = None
        
    for local in listaEstoque:
        if local.get('cDescricaoLocal') == 'Estoque da Sede':
            cDescricaoLocal = local.get('cDescricaoLocal', '')
            nPrecoUltComp = local.get('nPrecoUltComp', 0)
            resultado = {
                'Cod': cCodigo,
                'Descricao': cDescricao,
                'Estoque': cDescricaoLocal,
                'Preco': nPrecoUltComp
            }
            df = pd.DataFrame([resultado])
            Preco = float(df['Preco'].iloc[0])
            break

    return Preco if Preco is not None else 0


    