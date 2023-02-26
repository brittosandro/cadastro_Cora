import sqlite3
import streamlit as st
import pandas as pd
import csv
import re
import base64


# Função para validar o formato do email
def validar_email(email):
    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        st.warning('O e-mail inserido é inválido')
        return False
    return True

# Cria uma conexão com o banco de dados
conn = sqlite3.connect('usuarios.db')

# Cria uma tabela para armazenar os dados do usuário
conn.execute('''CREATE TABLE IF NOT EXISTS usuarios
                (nome TEXT, sobrenome TEXT, matricula TEXT,
                email TEXT, serie TEXT, turma TEXT, curso TEXT, situação TEXT)''')

col1, col2 = st.columns([1, 0.4,])
with col1:
    st.title('Formulário de Cadastro')
    st.subheader('Colégio Estadual Cora Coralina')
with col2:
    st.image('logo_cora.png', width=190)

# Campos para entrada de dados
with st.form('my_form'):
    col1, col2 = st.columns(2)
    with col1:
        nome = st.text_input('Nome')
        sobrenome = st.text_input('Sobrenome')
        matricula = st.text_input('Matrícula')
        email = st.text_input('E-mail')
    with col2:
        serie = st.text_input('Série')
        turma = st.text_input('Turma')
        st.subheader('Curso')
        cursos = ['Auxiliar Financeiro', 'Auxiliar Administrativo',
                  'Auxiliar Agroecologia', 'Auxiliar Agropecuária',
                  'Assistente de Logística', 'Vendedor']
        curso_selecionado = st.radio('Selecione um curso:', cursos)
    # Botão de envio
    submit_button = st.form_submit_button(label='Enviar')

# Insere os dados do usuário no banco de dados
if submit_button:
    if validar_email(email):
        conn.execute("INSERT INTO usuarios VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                    (nome, sobrenome, matricula, email, serie,
                    turma, curso_selecionado, 'cadastrado'))
        conn.commit()
        st.success('Dados enviados com sucesso!')

        # Ler os dados do banco de dados usando pandas
        df = pd.read_sql_query("SELECT * from usuarios", conn)

        # Exibir os dados em uma tabela
        st.write(df)

        # Botão para baixar os dados como um arquivo CSV
        def download_csv(df):
            csvfile = df.to_csv(index=False)
            b64 = base64.b64encode(csvfile.encode()).decode()
            href = f'<a href="data:file/csv;base64,{b64}" download="usuarios.csv">Download CSV</a>'
            st.markdown(href, unsafe_allow_html=True)

        download_csv(df)

        # Fecha a conexão com o banco de dados
        conn.close()
