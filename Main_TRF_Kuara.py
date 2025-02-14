import Preco
import Produtos
import Lancar_TRF_Kuara as Lancar_TRF_Kuara
import pandas as pd
from datetime import datetime
import streamlit as st


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

    Plan = st.file_uploader('Favor inserir a planilha do Excel', type='xlsx', key='inp_file_01')
    #Plan = pl.load_workbook('Transferencia.xlsx')
    #Sheet = Plan['Planilha1']
    #Data = Sheet['G2'].value

    if Plan is not None:
        try:
            xls = pd.ExcelFile(Plan)
            Sheet = pd.read_excel(xls, sheet_name="Planilha1") 
            #Data = datetime.strftime(Data, '%d/%m/%Y')
            Data = st.date_input('Informe a Data da Transferencia', "today", format= "DD/MM/YYYY", key='inp_data_01')
            Nome_Transferencia = 'Kuara'
            Data = datetime.strftime(Data, '%d/%m/%Y')

            if 'df' not in st.session_state:
                st.session_state.df = None

            if st.button('Carregar Dados da Planilha', key='inp_button_01'):
                xls = pd.ExcelFile(Plan)
                df = pd.read_excel(xls, sheet_name="Planilha1", usecols=['Cod', 'Descricao', 'Unidade', 'Quantidade'], header=0) 
                #df = pd.read_excel('Transferencia.xlsx', usecols=['Cod', 'Descricao', 'Unidade', 'Quantidade', 'Num_Transf'], sheet_name=0, header=0)
                st.session_state.df = df
                st.dataframe(df, hide_index=True)
        except Exception as e:
            st.error(f'Erro ao Carregar Planilha: {e}')
    else:
        st.warning('Anexe o arquivo da Transferencia')

    if st.session_state.df is not None:
        if st.button('Lançar', key='inp_nome_04'):
            df = st.session_state.df
            for i in range(len(df)):
                cod = str(df['Cod'][i])
                st.write("Transferindo", cod, " - ", df['Descricao'][i], "- Aguarde...")
                CodOmie = Produtos.Prod(cod)
                if CodOmie == None:
                    st.warning(f"Produto {df['Descricao'][i]} não encontrado no Omie")
                    continue
                else:
                    Qtde = str(df['Quantidade'][i])
                    Obs = Nome_Transferencia
                    Valor = Preco.BuscaPreco(cod, Data)
                    Resultado = Lancar_TRF_Kuara.Lancamento(CodOmie, Data, Qtde, Obs, Valor)
                    if Resultado:    
                        st.success(f"STATUS - OK -{cod} - {df['Descricao'][i]} - Valor - {Valor}")
                    else:
                        st.warning(f"Lançamento Codigo - {cod} Falhou")

            st.success("Lançamentos Realizado com Sucesso")
