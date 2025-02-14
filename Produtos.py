import requests
import pandas as pd
import time
import streamlit as st

def Prod(Codigo, max_tentativas=3, delay=5):
    url = "https://app.omie.com.br/api/v1/geral/produtos/"

    nPagina = 1
    nRegPorPagina = 100
    total_pages = 1
    filtered_data = []

    while nPagina <= total_pages:
        tentativa = 0
        sucesso = False

        while tentativa < max_tentativas and not sucesso:
            try:
                payload = {
                    "call": "ListarProdutos",
                    "app_key": "4292462707533",
                    "app_secret": "281e971011633384d72e052936906c57",
                    "param": [
                        {
                            "pagina": nPagina,
                            "registros_por_pagina": nRegPorPagina,
                            "apenas_importado_api": "N",
                            "filtrar_apenas_omiepdv": "N"
                        }
                    ]
                }

                headers = {
                    'Content-Type': 'application/json'
                }

                response = requests.post(url, headers=headers, json=payload)

                if response.status_code == 200:
                    data = response.json()

                    if nPagina == 1:
                        total_registros = data.get('total_de_registros', 0)
                        total_pages = (total_registros // nRegPorPagina) + (1 if total_registros % nRegPorPagina > 0 else 0)

                    titulos = data.get('produto_servico_cadastro', [])
                    
                    for titulo in titulos:
                        if titulo['codigo'] == Codigo:
                            filtered_data.append({
                                'Codigo': titulo.get('codigo'),
                                'CodigoOMIE': titulo.get('codigo_produto'),
                                'Descricao': titulo.get('descricao')
                            })
                    sucesso = True
                else:
                    st.write(f"Tentativa {tentativa + 1} falhou com status {response.status_code}. Tentando novamente em {delay} segundos...")
                    tentativa += 1
                    time.sleep(delay)
            except requests.exceptions.ConnectionError:
                st.write(f"Erro de Conexão com OMIE. Tentativa {tentativa + 1} de {max_tentativas}...")
                tentativa += 1
                time.sleep(delay)
            except requests.exceptions.Timeout:
                st.write(f"Servidor OMIE demorou muito")
                tentativa += 1
                time.sleep(delay)
            except Exception as e:
                st.write(f"Erro Inesperado: {e}")
                return None
            
        if not sucesso:
            st.write(f"Falha ao tentar executar a pagina {nPagina} após varias tentativas. ERRO CONEXAO")
            break

        nPagina += 1
    if filtered_data:
        df = pd.DataFrame(filtered_data)
        Cod = int(df['CodigoOMIE'].iloc[0])
        return Cod
    else:
        st.write('Nenhum Codigo encontrado, FAVOR VERIFICAR CADASTRO NO OMIE')
        return None