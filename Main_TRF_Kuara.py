import Preco
import Produtos
import Lancar_TRF_Kuara as Lancar_TRF_Kuara
import pandas as pd
from datetime import datetime
import streamlit as st
import xlwings as xl
import tempfile
import openpyxl

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

    if Plan is not None:
        try:
            xls = pd.ExcelFile(Plan)
            Sheet = pd.read_excel(xls, sheet_name="Planilha1") 
            
            Data = st.date_input('Informe a Data da Transferencia', "today", format= "DD/MM/YYYY", key='inp_data_01')
            Nome_Transferencia = 'Kuara'

            Data = datetime.strftime(Data, '%d/%m/%Y')

            if 'df' not in st.session_state:
                st.session_state.df = None

            if st.button('Carregar Dados da Planilha', key='inp_button_01'):
                #xls = pd.ExcelFile(Plan)
                df = pd.read_excel(xls, sheet_name="Planilha1", usecols=['Cod', 'Descricao', 'Unidade', 'Quantidade'], header=0) 
                st.session_state.df = df
                
        except Exception as e:
            st.error(f'Erro ao Carregar Planilha: {e}')
    else:
        st.warning('Anexe o arquivo da Transferencia')

    if st.session_state.df is not None:
        df_editado = st.data_editor(st.session_state.df, use_container_width=True, hide_index=True, key='editar_planilha01')
        if st.button('Lançar', key='inp_nome_06'):
            df = df_editado

            with tempfile.NamedTemporaryFile(delete=False, suffix="xlsx") as temp_file:
                #temp_file.write(Plan.getvalue())
                temp_file_path = temp_file.name
                with open(temp_file_path, 'wb') as f:
                    f.write(Plan.getvalue())
            
            try:
                #plan_usuario = xl.Book(temp_file_path)
                plan_usuario = openpyxl.load_workbook(temp_file_path)
                #Aba = plan_usuario.sheets[0]
                Aba = plan_usuario.active

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
                    
                    df_placeholder.dataframe(df, hide_index=True)
                    #Aba.range("A2:D1000").clear_contents()
                    #Aba.range("A2").value = df.to_numpy()
                    for row_idx, row in enumerate(df.itertuples(index=False, name=None), start=2):
                        for col_idx, value in enumerate(row, start=1):
                            Aba.cell(row=row_idx, column=col_idx, value=value)

                st.session_state.df = df

                st.success("Processo Finalizado - VERIFICAR LANÇAMENTOS")
            except Exception as e:
                st.error(f'Erro {e} - Planilha não carregada')
