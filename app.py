import streamlit as st
import Main_Balanco_Kuara
import Main_TRF_Kuara
import Main_TRF_Mansear

st.set_page_config(layout='wide')


# Criar um menu lateral para selecionar os aplicativos
opcao = st.sidebar.selectbox(
    "Selecione um aplicativo:", 
    ["Home", "Lançar Balanço Kuara", "Lançar Transferência Mansear", "Lançar Transferência Kuara"]
)

# Exibir a página correspondente
if opcao == "Home":
    st.title("Dashboard Principal")
    st.write("Bem-vindo ao Dashboard! Selecione um aplicativo no menu à esquerda.")
elif opcao == "Lançar Balanço Kuara":
    Main_Balanco_Kuara.Balanco_Kuara()  # Executa o script diretamente
elif opcao == "Lançar Transferência Kuara":
    Main_TRF_Kuara.TRF_Kuara()
elif opcao == "Lançar Transferência Mansear":
    Main_TRF_Mansear.TRF_Mansear()
