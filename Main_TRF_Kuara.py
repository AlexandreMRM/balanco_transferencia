import Preco
import Produtos
import Lancar_TRF_Kuara as Lancar_TRF_Kuara
import pandas as pd
from datetime import datetime
import streamlit as st
import xlwings as xl
import tempfile
import openpyxl
import planilha_sheet

def TRF_Kuara():
    #st.set_page_config(layout='wide')
    st.markdown('<h1 style="font-size:50px;">Transferencia Kuara</h1>', unsafe_allow_html=True)
    st.markdown("""
                    <style>
                    .stApp{
                        background-color: #D2B48C;
                    }
                    h1{
                        font-size: 20pt;
                        color: #8B4513;

                    h2, h3, .stMarkdown, .stRadio label, .stSelectbox label{
                        font-size: 10pt;
                        color: #8B4513;
                    }
                    .stDateInput label {
                        font-size: 20pt;
                        color: #8B4513;
                    }
                    <style>
        """, unsafe_allow_html=True)

    if 'df' not in st.session_state:
        st.session_state.df = None

    if 'df_editado' not in st.session_state:
        st.session_state.df_editado = None

    Data = st.date_input('Informe a Data da Transferencia', "today", format= "DD/MM/YYYY", key='inp_data_01')
    Nome_Transferencia = 'Kuara'

    Data = Data.strftime('%d/%m/%Y')

    if st.button('Carregar Dados da Planilha', key='inp_button_01'):
        st.session_state.df = planilha_sheet.planilha()

    if st.session_state.df is not None:
        df_editado = st.data_editor(st.session_state.df, use_container_width=True, hide_index=True, key='editar_planilha03')
        st.session_state.df_editado = df_editado

    if st.session_state.df_editado is not None and st.button('Lançar', key='inp_nome_05'):
        df = st.session_state.df_editado

        status_placeholder = st.empty()
        df_placeholder = st.empty()
                
        for i in range(len(df)):
            cod = str(df['Cod'][i])

            status_placeholder.write(f"Lançando {cod} - Descrição {df['Descricao'][i]}...")
            CodOmie = Produtos.Prod(cod)

            if CodOmie == None:
                st.warning(f"Produto {df['Descricao'][i]} não encontrado no Omie")
                df.loc[i, 'Status'] = 'Erro'
                continue
            else:
                Qtde = str(df['Quantidade'][i])
                Obs = Nome_Transferencia
                Valor = Preco.BuscaPreco(cod, Data)
                Resultado = Lancar_TRF_Kuara.Lancamento(CodOmie, Data, Qtde, Obs, Valor)
                if Resultado:    
                    st.success(f"STATUS - OK -{cod} - {df['Descricao'][i]} - Valor - {Valor}")
                    df.loc[i, 'Status'] = 'Lançado'

                else:
                    st.warning(f"Lançamento Codigo - {cod} Falhou")
                    df.loc[i, 'Status'] = 'Erro'
                    
                df_placeholder.dataframe(df, hide_index=True, use_container_width=True)
                planilha_sheet.salvar_planilha(df)

                st.session_state.df = df

        st.success("Processo Finalizado - VERIFICAR LANÇAMENTOS")
            
