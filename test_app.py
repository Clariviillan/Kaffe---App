
from app import app

def test_inicio():
    cliente = app.test_client()
    respuesta = cliente.get("/")
    assert respuesta.status_code == 200

def test_registro_muestra_avatares_de_cafe_sin_fotos_externas():
    cliente = app.test_client()
    pagina = cliente.get("/").get_data(as_text=True)
    selector = pagina.split(
        '<div class="avatar-selector" id="avatar-selector">', 1
    )[1].split("\n                </div>", 1)[0]

    assert "profile-coffee.svg" in selector
    assert "profile-beans.svg" in selector
    assert "profile-latte.svg" in selector
    assert "unsplash" not in selector

def test_explorar_incluye_tres_barras_de_matcha():
    cliente = app.test_client()
    pagina = cliente.get("/").get_data(as_text=True)

    assert "Te Quiero Matcha" in pagina
    assert "Unnies Matcha" in pagina
    assert "Luckycha Matcha" in pagina
    assert "ANd9GcT2g73oKRRR6hmYjNUlqXszqleufFPCAGUBMLeWP3DZ1w" in pagina
    assert "ANd9GcT_MB_DcP_apbwl-mK2aIBzi0VBHg3Z5dzAJITuGfyAiw" in pagina
    assert "ANd9GcQms0u6expGfb7ktmtgozlAef4oqFlW2xA-nVk-FuuHEw" in pagina

def test_explorar_incluye_mmmatcha_y_antidoto_en_sus_zonas():
    pagina = app.test_client().get("/").get_data(as_text=True)

    assert "Mmmatcha Delivery" in pagina
    assert "zone: 'Agua Caliente'" in pagina
    assert "Antidoto Matcha Lab" in pagina
    assert "zone: 'Col. Cacho'" in pagina
    assert "specialty: 'Matcha/Té'" in pagina
    assert '<option value="Agua Caliente"' in pagina
    assert "Menú por confirmar" in pagina
    assert "ANd9GcSW0cIZt1eCdRIj8xCszKcfB6jElh5H9jUNjjjBGSdc4g" in pagina
    assert "ANd9GcTKUm570TEPdLSbpNfRsK20HrllCU44Ppy2nTQsks0GMA" in pagina

def test_filtros_de_zona_y_precio_sin_emojis():
    pagina = app.test_client().get("/").get_data(as_text=True)

    assert "Zona: Todas" in pagina
    assert "Precio: Todos" in pagina
    assert "Mejor rankeado" in pagina
    assert "Peor rankeado" in pagina
    assert "Menor precio" not in pagina
    assert "📍 Zona: Todas" not in pagina
    assert "💲 Precio: Todos" not in pagina
    assert "💲 Menor precio" not in pagina

def test_titulo_mapa_sin_en_vivo():
    pagina = app.test_client().get("/").get_data(as_text=True)

    assert "<h3>Mapa de Tijuana</h3>" in pagina
    assert "Mapa de Tijuana en Vivo" not in pagina
    assert "Toca un granito" not in pagina

def test_top_semana_sin_boton_de_mejor_rankeados():
    pagina = app.test_client().get("/").get_data(as_text=True)

    assert "<h3>Top Semana</h3>" in pagina
    assert "Mejor Rankeados" not in pagina
    assert "${cafe.reviews.length} reseñas verificadas" not in pagina

def test_encabezado_de_app_sin_subtitulo_ni_logo():
    pagina = app.test_client().get("/").get_data(as_text=True)
    encabezado = pagina.split('<header class="top-header">', 1)[1].split("</header>", 1)[0]

    assert "Tijuana • Explora y recoge" not in pagina
    assert "header-subtitle" not in encabezado
    assert 'class="header-logo-pill"' not in encabezado

def test_acceso_cafeteria_solo_indica_administrador():
    pagina = app.test_client().get("/").get_data(as_text=True)

    assert "Acceso para Administrador" in pagina
    assert "Acceso para Cafetería / Administrador" not in pagina

def test_acceso_cliente_solo_indica_cliente():
    pagina = app.test_client().get("/").get_data(as_text=True)

    assert "<span>Acceso para Cliente</span>" in pagina
    assert "Acceso para Cliente • Explora, ordena y sella tu pasaporte" not in pagina

def test_carrito_a_la_derecha_y_salir_antes_de_mi_perfil_cliente():
    pagina = app.test_client().get("/").get_data(as_text=True)
    encabezado = pagina.split('<header class="top-header">', 1)[1].split("</header>", 1)[0]

    assert encabezado.index('id="header-logout-btn"') < encabezado.index('id="header-cart-btn"')
    assert '<span>Salir</span>' not in pagina

def test_carrito_vacio_sin_ilustracion():
    pagina = app.test_client().get("/").get_data(as_text=True)

    assert "Tu bolsa está vacía" in pagina
    assert '<i class="fa-solid fa-mug-hot" style="font-size: 2.2rem; color: var(--coffee-warm); margin-bottom: 10px;"></i>' not in pagina

def test_carrito_no_muestra_cero_encima_del_icono():
    pagina = app.test_client().get("/").get_data(as_text=True)

    assert 'id="cart-count" class="cart-badge hidden">0</span>' in pagina
    assert "badge.classList.toggle('hidden', count === 0)" in pagina

def test_acceso_sin_mensaje_de_bienvenida():
    pagina = app.test_client().get("/").get_data(as_text=True)

    assert '<span id="toast-msg"></span>' in pagina
    assert "¡Bienvenido a Kaffe Tijuana," not in pagina

def test_cerrar_sesion_sin_aviso_emergente():
    pagina = app.test_client().get("/").get_data(as_text=True)

    assert "Has cerrado sesión" not in pagina

def test_acceso_cafeteria_sin_aviso_de_panel_activo():
    pagina = app.test_client().get("/").get_data(as_text=True)

    assert "Panel ${cafe.name} • Membresía Activa" not in pagina

def test_pedidos_de_cafeteria_sin_nombre_de_negocio():
    pagina = app.test_client().get("/").get_data(as_text=True)

    assert "<h3>Mis pedidos</h3>" in pagina
    assert "Pedidos Recibidos • ${cafe.name}" not in pagina
    assert '<span>Mis pedidos</span>' in pagina

def test_recibos_sin_rfc_junto_al_titulo():
    pagina = app.test_client().get("/").get_data(as_text=True)

    assert "<h3>Recibos</h3>" in pagina
    assert "Recibos y Facturación" not in pagina
    assert 'color: var(--mocha);">RFC ${cafe.rfc}</span>' not in pagina

def test_perfil_cambia_bebidas_por_redes_sociales_editables():
    pagina = app.test_client().get("/").get_data(as_text=True)

    assert "Bebidas que ya has probado" not in pagina
    assert "profile-social-links" in pagina
    assert "Instagram_logo_2022.svg/1280px-Instagram_logo_2022.svg.png" in pagina
    assert "fa-brands fa-facebook-f" in pagina
    assert 'id="edit-profile-facebook"' in pagina
    assert "function getInstagramProfileUrl" in pagina
    assert "function getFacebookProfileUrl" in pagina

def test_perfil_muestra_nombre_sin_boton_de_nivel():
    pagina = app.test_client().get("/").get_data(as_text=True)

    assert '<h2 class="font-serif" style="font-size: 1.42rem;">${user.name}</h2>' in pagina
    assert "${user.level}" not in pagina

def test_resena_sin_texto_url_opcional():
    pagina = app.test_client().get("/").get_data(as_text=True)

    assert "<label>Foto de tu bebida</label>" in pagina
    assert "URL opcional" not in pagina

def test_titulo_pin_en_mapa_sin_real_de_tijuana():
    pagina = app.test_client().get("/").get_data(as_text=True)

    assert ">Pin en Mapa</h4>" in pagina
    assert "Pin en Mapa Real de Tijuana" not in pagina

def test_edicion_de_cafeteria_incluye_indicaciones_y_pin_preciso():
    pagina = app.test_client().get("/").get_data(as_text=True)

    assert 'id="cafe-address-input"' in pagina
    assert "Ubicación e indicaciones para llegar" in pagina
    assert 'id="cafe-pin-coordinates"' in pagina
    assert "function updateCafePinCoordinates(cafe)" in pagina
    assert "Descripción de la cafetería (visible para los clientes)" not in pagina
    assert "Toca en el mapa o arrastra el granito de café para ajustar tu ubicación exacta." not in pagina
    assert "Foto y Descripción de la Cafetería" in pagina
    assert 'fa-image" style="color: var(--coffee-warm);"></i> Foto y Descripción de la Cafetería' not in pagina

def test_cafeterias_pueden_agregar_postres_y_panaderia():
    pagina = app.test_client().get("/").get_data(as_text=True)

    assert "Agregar Producto al Menú" in pagina
    assert '<option value="Panadería">Panadería</option>' in pagina
    assert '<option value="Postres">Postres</option>' in pagina
    assert "new-item-image" in pagina
    assert '<label>Foto del producto</label>' in pagina
    assert 'id="new-item-image" class="input-control" placeholder="https://..." required' in pagina
    assert "Foto del producto (opcional)" not in pagina
    assert "'Postres'].map(cat" in pagina
    assert '<h3>Información, Catálogo y Ubicación</h3>' in pagina
    assert '<span class="badge badge-coffee">${cafe.zone}</span>' not in pagina

def test_perfil_de_cafeteria_muestra_resenas_recibidas():
    pagina = app.test_client().get("/").get_data(as_text=True)

    assert "Reseñas de clientes" in pagina
    assert "cafe.reviews.map(review" in pagina
    assert "Aún no tienes reseñas." in pagina

def test_perfil_negocio_muestra_nombre_y_rfc_en_blanco():
    pagina = app.test_client().get("/").get_data(as_text=True)
    perfil = pagina.split("<!-- Cabecera de Cafetería -->", 1)[1]

    nombre_pos = perfil.index('<h2 class="font-serif" style="font-size: 1.35rem; line-height: 1.2;">${cafe.name}</h2>')
    rfc_pos = perfil.index('color: var(--beige-200); margin-top: 3px;">RFC: ${cafe.rfc}</p>')
    direccion_pos = perfil.index('<i class="fa-solid fa-location-dot"></i> ${cafe.address}')
    assert nombre_pos < rfc_pos < direccion_pos
    assert 'class="badge badge-coffee" style="margin-bottom: 4px;">RFC:' not in perfil

def test_cafeteria_tiene_vista_mi_menu_con_todos_sus_productos():
    pagina = app.test_client().get("/").get_data(as_text=True)

    assert 'id="nav-menu" onclick="switchTab(\'menu\')"' in pagina
    assert "function renderCafeMenu(container)" in pagina
    assert "incluidos los productos pausados" in pagina
    assert "Administrar catálogo" in pagina

def test_personalizacion_de_bebidas_y_costo_extra():
    pagina = app.test_client().get("/").get_data(as_text=True)

    assert "const DRINK_EXTRA_PRICE = 15;" in pagina
    assert "function saveCafeCustomizationOptions" in pagina
    assert "function calculateCustomizationFee" in pagina
    assert "drink-milk" in pagina
    assert "drink-shots" in pagina
    assert "drink-matcha-grams" in pagina
    assert "Activa lo que ofrece tu cafetería." not in pagina
    assert "la primera disponible se incluye; cambiarla cuesta" not in pagina

def test_edicion_cafeteria_sin_galeria_de_portada():
    pagina = app.test_client().get("/").get_data(as_text=True)

    assert "Galería rápida de barra" not in pagina
    assert "selectPresetCafeCover" not in pagina

def test_horario_de_negocio_configurable_y_visible():
    pagina = app.test_client().get("/").get_data(as_text=True)

    assert "function saveCafeBusinessHours" in pagina
    assert "function renderCafeBusinessHours" in pagina
    assert "Horario por confirmar" in pagina
    assert "Guardar horario" in pagina
    assert "Marca cada día que abres y define la hora de apertura y cierre." not in pagina

def test_estado():
    cliente = app.test_client()
    respuesta = cliente.get("/estado")
    assert respuesta.status_code == 200
def test_proteccion_sql_injection():
    cliente = app.test_client()

    respuesta = cliente.get(
        "/buscar?nombre=' OR 1=1 --"
    )

    assert respuesta.status_code == 200
    assert respuesta.json["resultados"] == []