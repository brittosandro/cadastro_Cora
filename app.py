import sqlite3
import streamlit as st
import re

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
                (nome TEXT, sobrenome TEXT, matricula TEXT, email TEXT, serie TEXT, turma TEXT, curso TEXT)''')

# Título do aplicativo
st.title('Formulário de Inscrição')

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
        cursos = ['Curso 1', 'Curso 2', 'Curso 3', 'Curso 4', 'Curso 5', 'Curso 6']
        curso_selecionado = st.radio('Selecione um curso:', cursos)
    # Botão de envio
    submit_button = st.form_submit_button(label='Enviar')

# Insere os dados do usuário no banco de dados
if submit_button:
    if validar_email(email):
        conn.execute("INSERT INTO usuarios VALUES (?, ?, ?, ?, ?, ?, ?)",
                    (nome, sobrenome, matricula, email, serie, turma, curso_selecionado))
        conn.commit()
        st.success('Dados enviados com sucesso!')

# Fecha a conexão com o banco de dados
conn.close()
