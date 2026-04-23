import streamlit as st
from kerykeion import AstrologicalSubject
import random
import datetime
import requests

# -----------------------------------
# CONFIGURACIÓN DE LA PÁGINA
# -----------------------------------
st.set_page_config(page_title="Plataforma Mística", page_icon="🔮", layout="centered")

st.title("✨ Universo Interior: Astrología y Tarot")

# ==========================================
# FUNCIONES DE GEOLOCALIZACIÓN (API)
# ==========================================
@st.cache_data
def obtener_paises():
    """Obtiene la lista de países y sus códigos de 2 letras"""
    try:
        res = requests.get("https://countriesnow.space/api/v0.1/countries/iso").json()
        return {item['name']: item['Iso2'] for item in res['data']}
    except:
        return {"Mexico": "MX", "Spain": "ES", "Argentina": "AR", "Colombia": "CO", "United States": "US"}

@st.cache_data
def obtener_estados(pais):
    """Obtiene los estados de un país seleccionado"""
    try:
        res = requests.post("https://countriesnow.space/api/v0.1/countries/states", json={"country": pais}).json()
        return [estado['name'] for estado in res['data']['states']]
    except:
        return []

@st.cache_data
def obtener_ciudades(pais, estado):
    """Obtiene las ciudades de un estado seleccionado"""
    try:
        res = requests.post("https://countriesnow.space/api/v0.1/countries/state/cities", json={"country": pais, "state": estado}).json()
        return res['data']
    except:
        return []

# Creamos TRES pestañas ahora
tab1, tab2, tab3 = st.tabs(["🌌 Carta Astral", "💞 Sinastría (Big 3)", "🔮 Tarot"])

# ==========================================
# PESTAÑA 1: CARTA ASTRAL (KERYKEION)
# ==========================================
with tab1:
    st.header("Generador de Carta Natal Exacta")
    st.write("Cálculo preciso utilizando efemérides suizas y geolocalización")
    
    # 1. Datos Personales
    col1, col2 = st.columns(2)
    nombre = col1.text_input("Nombre", "Tu Nombre")
    fecha = col1.date_input("Fecha de Nacimiento", datetime.date(1998, 1, 1), min_value=datetime.date(1900, 1, 1))
    hora = col2.time_input("Hora Exacta", datetime.time(12, 0))
    
    st.divider()
    st.markdown("### 📍 Ubicación de Nacimiento")
    
    # 2. Selector de País, Estado y Ciudad en cascada
    dict_paises = obtener_paises()
    lista_paises = list(dict_paises.keys())
    index_pais = lista_paises.index("Mexico") if "Mexico" in lista_paises else 0
    
    pais_seleccionado = st.selectbox("País", lista_paises, index=index_pais)
    
    estados = obtener_estados(pais_seleccionado)
    estado_seleccionado = st.selectbox("Estado / Provincia", estados) if estados else None
    
    if estado_seleccionado:
        ciudades = obtener_ciudades(pais_seleccionado, estado_seleccionado)
        if ciudades:
            ciudad_seleccionada = st.selectbox("Ciudad", ciudades)
        else:
            ciudad_seleccionada = st.text_input("Ciudad (Escribe tu ciudad)")
    else:
        ciudad_seleccionada = st.text_input("Ciudad (Escribe tu ciudad)")
        
    st.write("") # Espaciado
    
    # Botón de envío (fuera de un form para que los selects se actualicen en tiempo real)
    if st.button("Consultar el Cielo 🌟", use_container_width=True, type="primary"):
        try:
            with st.spinner('Conectando con el cosmos...'):
                codigo_pais = dict_paises.get(pais_seleccionado, "US")
                
                sujeto = AstrologicalSubject(
                    nombre, fecha.year, fecha.month, fecha.day, 
                    hora.hour, hora.minute, ciudad_seleccionada, codigo_pais
                )
            
            st.success("¡Tu mapa ha sido trazado!")
            
            # --- IMPRESIÓN DE PLANETAS ---
            st.subheader("Tus Big 3")
            c1, c2, c3 = st.columns(3)
            c1.metric("☀️ Sol", sujeto.sun.sign)
            c2.metric("🌙 Luna", sujeto.moon.sign)
            c3.metric("⬆️ Ascendente", sujeto.first_house.sign)
            
            st.subheader("Planetas Personales")
            c4, c5, c6 = st.columns(3)
            c4.info(f"**☿️ Mercurio:** {sujeto.mercury.sign}")
            c5.info(f"**♀️ Venus:** {sujeto.venus.sign}")
            c6.info(f"**♂️ Marte:** {sujeto.mars.sign}")

            st.subheader("Planetas Sociales y Generacionales")
            c7, c8, c9 = st.columns(3)
            c7.info(f"**♃ Júpiter:** {sujeto.jupiter.sign}")
            c8.info(f"**♄ Saturno:** {sujeto.saturn.sign}")
            c9.info(f"**♅ Urano:** {sujeto.uranus.sign}")

            c10, c11, c12 = st.columns(3)
            c10.info(f"**♆ Neptuno:** {sujeto.neptune.sign}")
            c11.info(f"**♇ Plutón:** {sujeto.pluto.sign}")
            
            # Lilith
            try:
                signo_lilith = sujeto.lilith.sign
            except AttributeError:
                signo_lilith = "Actualiza tu Kerykeion"
                
            c12.info(f"**⚸ Lilith:** {signo_lilith}")
            
        except Exception as e:
            st.error(f"Hubo un problema encontrando esa ciudad o calculando los datos. (Error técnico: {e})")

# ==========================================
# PESTAÑA 2: SINASTRÍA (COMPARADOR BIG 3)
# ==========================================
with tab2:
    st.header("Compatibilidad de Almas")
    st.write("Descubre la afinidad energética basándote en los elementos de los signos.")

    signos_lista = [
        "Aries", "Tauro", "Géminis", "Cáncer", "Leo", "Virgo", 
        "Libra", "Escorpio", "Sagitario", "Capricornio", "Acuario", "Piscis"
    ]

    elementos_zodiaco = {
        "Aries": "fuego", "Tauro": "tierra", "Géminis": "aire", "Cáncer": "agua",
        "Leo": "fuego", "Virgo": "tierra", "Libra": "aire", "Escorpio": "agua",
        "Sagitario": "fuego", "Capricornio": "tierra", "Acuario": "aire", "Piscis": "agua"
    }

    def analizar_compatibilidad(signo1, signo2):
        e1, e2 = elementos_zodiaco[signo1], elementos_zodiaco[signo2]
        if e1 == e2:
            return 3, "Fluyen naturalmente. Tienen una vibración muy similar."
        
        complementarios = {'fuego': 'aire', 'aire': 'fuego', 'tierra': 'agua', 'agua': 'tierra'}
        if complementarios.get(e1) == e2:
            return 2, "Se complementan hermoso. Uno alimenta la energía del otro."
            
        return 1, "Tienen un reto kármico aquí. Sus energías son distintas y requerirán paciencia."

    col_p1, col_p2 = st.columns(2)
    
    with col_p1:
        st.subheader("Persona 1")
        sol1 = st.selectbox("☀️ Sol (P1)", signos_lista, key="s1")
        luna1 = st.selectbox("🌙 Luna (P1)", signos_lista, key="l1")
        asc1 = st.selectbox("⬆️ Ascendente (P1)", signos_lista, key="a1")

    with col_p2:
        st.subheader("Persona 2")
        sol2 = st.selectbox("☀️ Sol (P2)", signos_lista, index=6, key="s2")
        luna2 = st.selectbox("🌙 Luna (P2)", signos_lista, index=3, key="l2")
        asc2 = st.selectbox("⬆️ Ascendente (P2)", signos_lista, index=8, key="a2")

    if st.button("Calcular Sinastría 💞"):
        score_sol, texto_sol = analizar_compatibilidad(sol1, sol2)
        score_luna, texto_luna = analizar_compatibilidad(luna1, luna2)
        score_asc, texto_asc = analizar_compatibilidad(asc1, asc2)
        
        puntaje_total = score_sol + score_luna + score_asc
        porcentaje = round((puntaje_total / 9) * 100)

        if porcentaje >= 80:
            mensaje = "¡Almas gemelas a la vista! Tienen una afinidad cósmica muy fuerte."
            color = "success"
        elif porcentaje >= 50:
            mensaje = "Hay potencial. Tienen fluidez en algunas áreas y trabajo que hacer en otras."
            color = "warning"
        else:
            mensaje = "Conexión desafiante. Viene a enseñarles lecciones. ¡Requerirá madurez emocional!"
            color = "error"

        st.divider()
        st.markdown(f"<h3 style='text-align: center;'>Compatibilidad Cósmica: {porcentaje}%</h3>", unsafe_allow_html=True)
        
        if color == "success": st.success(mensaje)
        elif color == "warning": st.warning(mensaje)
        else: st.error(mensaje)

        st.write(f"**☀️ Sol (Esencia):** {texto_sol}")
        st.write(f"**🌙 Luna (Emociones):** {texto_luna}")
        st.write(f"**⬆️ Ascendente (Atracción):** {texto_asc}")

# ==========================================
# PESTAÑA 3: TAROT
# ==========================================
with tab3:
    st.header("Lectura de Arcanos Mayores")
    
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
        {"n": "XXI. El Mundo", "d": "Finalización, integración, logros.", "i": "Estancamiento, falta de cierre."}
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
        
        cartas_sacadas = random.sample(arcanos, num_cartas)
        cols = st.columns(num_cartas)
        
        for i, col in enumerate(cols):
            carta = cartas_sacadas[i]
            invertida = random.random() < 0.2
            estado = "↓ Invertida" if invertida else "↑ Al derecho"
            significado = carta["i"] if invertida else carta["d"]
            
            with col:
                st.markdown(f"**{posiciones[i].upper()}**")
                st.markdown(f"### {carta['n']}")
                st.markdown(f"*{estado}*")
                st.info(significado)