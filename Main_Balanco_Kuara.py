import Preco
import Produtos
import Lancar_Balanco as Lancar_Balanco
import pandas as pd
from datetime import datetime
import streamlit as st

def Balanco_Kuara():
    #st.set_page_config(layout='wide')
    st.markdown('<h1 style="font-size:50px;">Balanco Kuara</h1>', unsafe_allow_html=True)
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

    Plan = st.file_uploader('Favor inserir a planilha do Excel', type='xlsx', key='inp_file_01')

    if Plan is not None:
        xls = pd.ExcelFile(Plan)
        df = pd.read_excel(xls, sheet_name='Planilha1')
    else:
        st.warning('Favor Carregar a planilha')

    Data = st.date_input('Informe a Data do Balanço', "today", format= "DD/MM/YYYY", key='inp_data_01')
    Nome_Balanco = st.text_input('Informe o Codigo do Balanço - Ex. K01012025')

    Data = datetime.strftime(Data, '%d/%m/%Y')

    if 'df' not in st.session_state:
        st.session_state.df = None

    if st.button('Carregar Dados da Planilha', key='inp_button_01'):
        #df = pd.read_excel(xls, sheet_name='Planilha1')
        #df = pd.read_excel('Balanco_Kuara.xlsx', usecols=['Cod', 'Descricao', 'Unidade', 'Quantidade'], sheet_name=0, header=0)
        st.session_state.df = df
        df['Cod'] = df['Cod'].astype(str)
        st.dataframe(df, hide_index=True)

    if st.session_state.df is not None:
        if st.button('Lançar', key='inp_nome_lancar'):
            df = st.session_state.df
            for i in range(len(df)):
                cod = str(df['Cod'][i])
                st.write("Lançando ", cod, " - ", df['Descricao'][i], "Aguarde...")
                CodOmie = Produtos.Prod(cod)
                if CodOmie == None:
                    st.warning("Produto não encontrado no Omie")
                    continue
                else:
                    Qtde = str(df['Quantidade'][i])
                    Obs = Nome_Balanco
                    Valor = Preco.BuscaPreco(cod, Data)
                    resultado = Lancar_Balanco.Lancamento(CodOmie, Data, Qtde, Obs, Valor)
                    if resultado:
                        st.success(f"STATUS - OK {cod} - {df['Descricao'][i]} Lançado com Sucesso")
                    else:
                        st.warning(f"Lançamento Código - {cod} Falhou")

            st.success("Lançamentos Realizado com Sucesso")





#codigoProd = 815
#codigoProdStr = str(codigoProd)

#imp = Preco.BuscaPreco(codigoProd, "10/07/2024")
#prod = Produtos.Prod(codigoProdStr)
#print(imp.Preco)
#print(prod)