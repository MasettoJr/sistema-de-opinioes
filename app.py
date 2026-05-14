import streamlit as st
import sqlite3
from time import sleep

# Cria conexão com o banco
conexao = sqlite3.connect("banco.db")

# Mensageiro entre Python e banco
cursor = conexao.cursor()

# Define estrutura da tabela
cursor.execute("""CREATE TABLE IF NOT EXISTS avaliacoes (

                id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,

                avaliacao text NOT NULL

                    CHECK(avaliacao IN ('Ótimo', 'Bom', 'Regular', 'Ruim')),

                comentario TEXT NOT NULL

                )""")

# Widgets 

# Flag para limpar campos
if "limpar_formulario" not in st.session_state:
    st.session_state["limpar_formulario"] = False

# Flag para exibir success box
if "msg_sucesso" in st.session_state:
    st.success(st.session_state["msg_sucesso"])
    del st.session_state["msg_sucesso"]

if st.session_state["limpar_formulario"]:
    st.session_state["comentario"] = ""
    st.session_state["opcao"] = ""
    st.session_state["limpar_formulario"] = False
 
st.title("Avalie sua experiência")

# Opções
choice = st.radio("Qualidade do atendimento", ["Ruim", "Regular", "Bom", "Ótimo"], index=None, key="opcao")

# Campo de texto livre
text = st.text_area("Gostaria de deixar um comentário?", key="comentario")

clicked = st.button("Enviar")

if clicked:
    # Insere dados coletados na tabela
    cursor.execute(f"""INSERT INTO avaliacoes

                (avaliacao, comentario) VALUES

                ('{choice}', '{text}')

            """)

    # Envia para o banco
    conexao.commit() 

    st.session_state["msg_sucesso"] = "Avaliação registrada com sucesso!"
    st.session_state["limpar_formulario"] = True
    st.rerun()