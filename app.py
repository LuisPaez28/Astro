import streamlit as st
from kerykeion import AstrologicalSubject
import random
import datetime

# -----------------------------------
# CONFIGURACIÓN DE LA PÁGINA
# -----------------------------------
st.set_page_config(page_title="Plataforma Mística", page_icon="🔮", layout="centered")

st.title("✨ Universo Interior: Astrología y Tarot")
st.markdown("Descubre tu mapa cósmico y recibe la guía de los Arcanos.")

# Creamos pestañas para separar las herramientas
tab1, tab2 = st.tabs(["🌌 Carta Astral", "🔮 Oráculo del Tarot"])

# ==========================================
# PESTAÑA 1: CARTA ASTRAL (KERYKEION)
# ==========================================
with tab1:
    st.header("Generador de Carta Natal Exacta")
    st.write("Cálculo preciso utilizando efemérides suizas y geolocalización real.")
    
    with st.form("astrology_form"):
        col1, col2 = st.columns(2)
        
        nombre = col1.text_input("Nombre", "Tu Nombre")
        fecha = col1.date_input("Fecha de Nacimiento", datetime.date(1990, 1, 1), min_value=datetime.date(1900, 1, 1))
        hora = col2.time_input("Hora Exacta", datetime.time(12, 0))
        
        ciudad = col1.text_input("Ciudad de Nacimiento", "Mexico City")
        pais = col2.text_input("Código de País (ej. MX, ES, AR)", "MX")
        
        submit = st.form_submit_button("Consultar el Cielo 🌟")
        
    if submit:
        try:
            with st.spinner('Conectando con el cosmos...'):
                # Magia de Kerykeion: Calcula lat/lon y posiciones exactas
                sujeto = AstrologicalSubject(
                    nombre, fecha.year, fecha.month, fecha.day, 
                    hora.hour, hora.minute, ciudad, pais
                )
            
            st.success("¡Tu mapa ha sido trazado!")
            
            st.subheader("Tus Big 3")
            c1, c2, c3 = st.columns(3)
            c1.metric("☀️ Sol (Esencia)", sujeto.sun.sign)
            c2.metric("🌙 Luna (Emociones)", sujeto.moon.sign)
            c3.metric("⬆️ Ascendente (Exterior)", sujeto.first_house.sign)
            
            st.subheader("Otros Planetas Personales")
            c4, c5, c6 = st.columns(3)
            c4.info(f"**☿️ Mercurio:** {sujeto.mercury.sign}")
            c5.info(f"**♀️ Venus:** {sujeto.venus.sign}")
            c6.info(f"**♂️ Marte:** {sujeto.mars.sign}")
            
        except Exception as e:
            st.error(f"Hubo un problema encontrando esa ciudad o calculando los datos. Asegúrate de escribir el código de país correctamente. (Error técnico: {e})")

# ==========================================
# PESTAÑA 2: TAROT
# ==========================================
with tab2:
    st.header("Lectura de Arcanos Mayores")
    
    # Base de datos del Tarot
    arcanos = [
        {"n": "0. El Loco", "d": "Nuevos comienzos, aventura, salto de fe.", "i": "Imprudencia, riesgos innecesarios."},
        {"n": "I. El Mago", "d": "Manifestación, poder personal, recursos.", "i": "Manipulación, talentos ocultos."},
        {"n": "II. La Sacerdotisa", "d": "Intuición, misterio, voz interior.", "i": "Secretos, desconexión intuitiva."},
        {"n": "III. La Emperatriz", "d": "Abundancia, fertilidad, naturaleza.", "i": "Dependencia, bloqueo creativo."},
        {"n": "IV. El Emperador", "d": "Estructura, autoridad, estabilidad.", "i": "Tiranía, rigidez."},
        {"n": "V. El Hierofante", "d": "Tradición, creencias, educación.", "i": "Rebelión, creencias restrictivas."},
        {"n": "VI. Los Enamorados", "d": "Amor, elecciones, armonía.", "i": "Desequilibrio, malas decisiones."},
        {"n": "VII. El Carro", "d": "Fuerza de voluntad, éxito, control.", "i": "Falta de dirección, obstáculos."},
        {"n": "VIII. La Fuerza", "d": "Coraje, compasión, control interno.", "i": "Inseguridad, duda de uno mismo."},
        {"n": "IX. El Ermitaño", "d": "Introspección, soledad, guía interna.", "i": "Aislamiento, rechazo al mundo."},
        {"n": "X. Rueda de la Fortuna", "d": "Ciclos, destino, suerte.", "i": "Resistencia al cambio."},
        {"n": "XI. La Justicia", "d": "Verdad, ley, causa y efecto.", "i": "Deshonestidad, injusticia."},
        {"n": "XII. El Colgado", "d": "Pausa, nuevas perspectivas, soltar.", "i": "Estancamiento, indecisión."},
        {"n": "XIII. La Muerte", "d": "Finales, transformación, liberación.", "i": "Miedo al cambio, aferrarse al pasado."},
        {"n": "XIV. La Templanza", "d": "Equilibrio, moderación, propósito.", "i": "Excesos, desequilibrio."},
        {"n": "XV. El Diablo", "d": "Sombra, apegos, materialismo.", "i": "Liberación, desapego."},
        {"n": "XVI. La Torre", "d": "Cambio repentino, caos, despertar.", "i": "Miedo al sufrimiento."},
        {"n": "XVII. La Estrella", "d": "Esperanza, fe, renovación.", "i": "Desesperación, desconexión."},
        {"n": "XVIII. La Luna", "d": "Ilusiones, miedos, subconsciente.", "i": "Miedos revelados, claridad."},
        {"n": "XIX. El Sol", "d": "Éxito, vitalidad, alegría.", "i": "Pesimismo, falta de claridad."},
        {"n": "XX. El Juicio", "d": "Renacimiento, llamado interior.", "i": "Dudas, ignorar el llamado."},
        {"n": "XX1. El Mundo", "d": "Finalización, integración, logros.", "i": "Estancamiento, falta de cierre."}
    ]

    layouts = {
        "1 Carta (El Mensaje del Día)": ["Mensaje Central"],
        "3 Cartas (Pasado, Presente, Futuro)": ["Pasado", "Presente", "Futuro"],
        "5 Cartas (La Cruz Simple)": ["Situación", "Reto", "Consejo", "Oculto", "Resultado"]
    }

    tipo_tirada = st.selectbox("Selecciona tu tirada:", list(layouts.keys()))
    
    if st.button("Mezclar y Tirar las Cartas 🔮"):
        posiciones = layouts[tipo_tirada]
        num_cartas = len(posiciones)
        
        # Mezclar (sample toma elementos únicos)
        cartas_sacadas = random.sample(arcanos, num_cartas)
        
        # Mostrar las cartas en columnas dinámicas
        cols = st.columns(num_cartas)
        
        for i, col in enumerate(cols):
            carta = cartas_sacadas[i]
            invertida = random.random() < 0.2
            estado = "↓ Invertida" if invertida else "↑ Al derecho"
            significado = carta["i"] if invertida else carta["d"]
            color = "red" if invertida else "green"
            
            with col:
                st.markdown(f"**{posiciones[i].upper()}**")
                st.markdown(f"### {carta['n']}")
                st.markdown(f"*{estado}*")
                st.info(significado)