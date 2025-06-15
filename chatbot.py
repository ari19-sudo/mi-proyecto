import streamlit as st
from groq import Groq

modelos = ["llama3-8b-8192", "llama3-70b-8192", "mixtral-8x7b-32768"]
modelo_elegido = st.sidebar.selectbox("seleccionar un modelo", modelos)

def crear_usuario_groq():
    clave_secreta = st.secrets["CLAVE_API"]
    return Groq(api_key = clave_secreta)

def configurar_modelo(cliente, modelos, mensajeDeEntrada):
    return cliente.chat.completions.create(
        model = modelos,
        messages = [{"role": "user", "content": mensajeDeEntrada}],
        stream = True
        )

def inicializar_estado():
    if "mensajes" not in st.session_state:
        st.session_state.mensajes = []

def actualizar_historial(rol, contenido, avatar):
    st.session_state.mensajes.append({"role": rol, "content": contenido, "avatar": avatar}) 

def mostrar_historial():
    for mensaje in st.session_state.mensajes:
        with st.chat_message(mensaje["role"], avatar = mensaje["avatar"]): st.markdown(mensaje["content"])

def area_chat():
    contenedorChat = st.container(height = 400, border = True)
    with contenedorChat: mostrar_historial()

def main():
    clienteUsuario = crear_usuario_groq()
    inicializar_estado()
    area_chat()
    respuesta_completa()
    mensaje_respuesta()
    
    mensaje = st.chat_input("escribi mensaje")
    if mensaje:
        actualizar_historial("user", mensaje, "")
        with st.chat_message("assistant", avatar = ""):
            mensaje_respuesta = st.empty
            respuesta_completa = ""
            respuesta_stream = clienteUsuario.chat.completions.create(
                model = modelo_elegido,
                messages = [{"role": "user", "content": mensaje}],
                stream = True
            )
            for frase in respuesta_stream:
                if frase.choices[0].delta.content:
                    texto_nuevo = frase.choices[0].delta.content
                    respuesta_completa += frase.choices[0].delta.content
                    st.markdown(respuesta_completa)
                    actualizar_historial("assistant", respuesta_completa, "")
                    st.rerun()
                    main()