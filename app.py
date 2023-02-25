import streamlit as st
import re
import smtplib
import pandas as pd

# Função para enviar email com os dados preenchidos
def enviar_email(email, nome, sobrenome, matricula, serie, turma, curso):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login("nome@gmail.com", "senha")
    msg = f"Olá {nome} {sobrenome},\n\nSegue abaixo os dados preenchidos no formulário:\n\nNome: {nome}\nSobrenome: {sobrenome}\nMatrícula: {matricula}\nSérie: {serie}\nTurma: {turma}\nCurso selecionado: {curso}\n\nObrigado por se inscrever no Colégio Estadual Cora Coralina."
    server.sendmail("seu_email@gmail.com", email, msg)
    server.quit()

# Função para validar o formato do email
def validar_email(email):
    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        st.warning('O e-mail inserido é inválido')
        return False
    return True

# Criação de um dataframe para armazenar os dados
df = pd.DataFrame(columns=['Nome', 'Sobrenome', 'Matrícula', 'E-mail', 'Série', 'Turma', 'Curso'])

col1, col2 = st.columns([1, 0.4,])
with col1:
    st.title('Formulário de Cadastro')
    st.subheader('Colégio Estadual Cora Coralina')
with col2:
    st.image('logo_cora.png', width=60)


# Campos para entrada de dados
with st.form('my_form'):
    col1, col2 = st.columns(2)
    with col1:
        nome = st.text_input('Nome')
        sobrenome = st.text_input('Sobrenome')
        matricula = st.text_input('Matrícula')
        email = st.text_input('E-mail')
        serie = st.text_input('Série')
        turma = st.text_input('Turma')
    with col2:
        st.subheader('Curso')
        cursos = ['Auxiliar Financeiro', 'Auxiliar Administrativo',
                  'Auxiliar Agroecologia', 'Auxiliar Agropecuária',
                  'Assistente de Logística', 'Vendedor']
        curso_selecionado = st.radio('Selecione um curso:', cursos)
    # Botão de envio
    submit_button = st.form_submit_button(label='Enviar')


# Impressão das informações inseridas pelo usuário e armazenamento no dataframe
if submit_button:
    if validar_email(email):
        st.write('Nome:', nome)
        st.write('Sobrenome:', sobrenome)
        st.write('Matrícula:', matricula)
        st.write('E-mail:', email)
        st.write('Série:', serie)
        st.write('Turma:', turma)
        st.write('Curso selecionado:', curso_selecionado)

        #enviar_email(email, nome, sobrenome, matricula, serie, turma, curso_selecionado)

        # Adiciona as informações no dataframe
        novo_registro = {'Nome': nome, 'Sobrenome': sobrenome, 'Matrícula': matricula, 'E-mail': email, 'Série': serie, 'Turma': turma, 'Curso': curso_selecionado}
        df = df.append(novo_registro, ignore_index=True)

        # Salva os dados do DataFrame em um arquivo Excel
        df.to_excel('dados.xlsx', index=False)
        
        # Adiciona botão para download da tabela
        output = base64.b64encode(df.to_excel(index=False, encoding='utf-8')).decode('utf-8')
        download_button_str = f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{output}" download="dados.xlsx">Download Tabela</a>'
        st.markdown(download_button_str, unsafe_allow_html=True)
