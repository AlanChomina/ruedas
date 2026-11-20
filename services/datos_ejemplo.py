"""
DATOS DE EJEMPLO - TEMPORALES.

Estos carros, agencias y alertas son ficticios. Se usan en el "modo de ejemplo"
(cuando .env no tiene Supabase configurado).
No contienen datos personales reales.

El campo "foto" es el nombre de un archivo dentro de static/images/carros/.
Si el archivo no existe, la página muestra un marcador ilustrado en su lugar.
"""

CARROS = [
    {"id": 1, "nombre": "Toyota Camry 2019", "carroceria": "sedán", "version": "LE Híbrido", "kilometraje": "68,000 km",
     "tamano": "mediano", "transmision": "automática", "combustible": "híbrido", "zona": "Playas de Tijuana",
     "estado": "disponible", "unico_dueno": True, "servicios_al_dia": True, "foto": "camry.jpg",
     "detalles": "Muy cuidado, cómodo en carretera y rinde muchísimo en ciudad."},
    {"id": 2, "nombre": "Suzuki Jimny 2021", "carroceria": "camioneta", "version": "GLX 4x4", "kilometraje": "24,000 km",
     "tamano": "compacto", "transmision": "manual", "combustible": "gasolina", "zona": "Zona Río",
     "estado": "disponible", "unico_dueno": True, "servicios_al_dia": True, "foto": "jimny.jpg",
     "detalles": "Ágil y divertida. Ideal para la ciudad y para salir a la terracería."},
    {"id": 3, "nombre": "Volkswagen Passat 2013", "carroceria": "sedán", "version": "TDI", "kilometraje": "182,000 km",
     "tamano": "grande", "transmision": "manual", "combustible": "diésel", "zona": "Otay",
     "estado": "urgente", "unico_dueno": False, "servicios_al_dia": True, "foto": "passat.jpg",
     "detalles": "Noble y rendidor. Su dueño se muda de ciudad y necesita venderlo pronto."},
    {"id": 4, "nombre": "Honda HR-V 2020", "carroceria": "camioneta", "version": "No especificada", "kilometraje": "41,000 km",
     "tamano": "compacto", "transmision": "automática", "combustible": "gasolina", "zona": "La Mesa",
     "estado": "en_proceso", "unico_dueno": True, "servicios_al_dia": True, "foto": "hrv.jpg",
     "detalles": "Discreta por fuera, muy amplia por dentro. Ya tiene un trato en curso."},
    {"id": 5, "nombre": "Mini Cooper 2016", "carroceria": "hatchback", "version": "Pepper", "kilometraje": "95,000 km",
     "tamano": "compacto", "transmision": "manual", "combustible": "gasolina", "zona": "Chapultepec",
     "estado": "en_consignacion", "unico_dueno": False, "servicios_al_dia": False, "foto": "mini.jpg",
     "detalles": "Divertido de manejar. Le toca el servicio mayor."},
    {"id": 6, "nombre": "Nissan Versa 2018", "carroceria": "sedán", "version": "Sense", "kilometraje": "88,000 km",
     "tamano": "compacto", "transmision": "manual", "combustible": "gasolina", "zona": "Cacho",
     "estado": "en_taller", "unico_dueno": True, "servicios_al_dia": True, "foto": "versa.jpg",
     "detalles": "Económico y confiable. Está en el taller por cambio de clutch."},
    {"id": 7, "nombre": "Ford Maverick 2022", "carroceria": "pickup", "version": "XLT Híbrida", "kilometraje": "30,000 km",
     "tamano": "compacto", "transmision": "automática", "combustible": "híbrido", "zona": "Hipódromo",
     "estado": "disponible", "unico_dueno": False, "servicios_al_dia": False, "foto": "maverick.jpg",
     "detalles": "Muy práctica: carga como pickup y gasta como compacto."},
    {"id": 8, "nombre": "Mazda 3 2021", "carroceria": "sedán", "version": "No especificada", "kilometraje": "35,000 km",
     "tamano": "mediano", "transmision": "automática", "combustible": "gasolina", "zona": "Santa Fe",
     "estado": "disponible", "unico_dueno": True, "servicios_al_dia": True, "foto": "mazda3.jpg",
     "detalles": "Deportivo y bien equipado, ideal para quien maneja a diario."},
    # --- Robados y recuperados (NO se muestran en el catálogo de compra) ---
    {"id": 9, "nombre": "Nissan Kicks 2019", "carroceria": "camioneta", "version": "Advance", "kilometraje": "57,000 km",
     "tamano": "compacto", "transmision": "automática", "combustible": "gasolina", "zona": "Colonia Cacho",
     "estado": "robado", "unico_dueno": True, "servicios_al_dia": True, "foto": "kicks.jpg",
     "detalles": "Visto por última vez estacionado cerca de un parque de la colonia."},
    {"id": 10, "nombre": "Sin identificar", "carroceria": "sedán", "version": "No especificada", "kilometraje": "Kilometraje desconocido",
     "tamano": "mediano", "transmision": "manual", "combustible": "gasolina", "zona": "Playas de Tijuana",
     "estado": "recuperado", "unico_dueno": False, "servicios_al_dia": False, "foto": "recuperado1.jpg",
     "detalles": "Recuperado sin placas, con un golpe en la defensa trasera. Está resguardado."},
]

AGENCIAS = [
    {"id": 1, "nombre": "Autos Otay Seminuevos (ejemplo)", "zona": "Otay", "verificado": True,
     "carros": 34, "descripcion": "Compra, venta y consignación de seminuevos revisados mecánicamente."},
    {"id": 2, "nombre": "Lote La Mesa Motors (ejemplo)", "zona": "La Mesa", "verificado": False,
     "carros": 12, "descripcion": "Lote familiar dedicado a compactos y carros económicos."},
    {"id": 3, "nombre": "Camionetas del Pacífico (ejemplo)", "zona": "Playas de Tijuana", "verificado": False,
     "carros": 21, "descripcion": "Pickups y camionetas con historial de servicio comprobable."},
]

PUBLICACIONES = [
    {"autor": "Autos Otay Seminuevos (ejemplo)", "tipo": "Historia de éxito", "icono": "bi-stars",
     "texto": "¡El Tsuru 2015 encontró dueña! Después de 8 meses en el lote ya rueda todos los días a la universidad.",
     "tiempo": "hace 2 horas", "me_gusta": 128, "comentarios": 14},
    {"autor": "Lote La Mesa Motors (ejemplo)", "tipo": "Jornada de revisión", "icono": "bi-calendar-check",
     "texto": "Este sábado tendremos jornada de diagnóstico por escáner a bajo costo. Cupo limitado.",
     "tiempo": "hace 5 horas", "me_gusta": 76, "comentarios": 9},
    {"autor": "Club de rodadas (ejemplo)", "tipo": "Rodada", "icono": "bi-people",
     "texto": "Buscamos conductores para la rodada a Rosarito el domingo por la mañana.",
     "tiempo": "ayer", "me_gusta": 41, "comentarios": 6},
]

# --- Alertas Ruedas de ejemplo (ficticias) ----------------------------------
# Las fechas se calculan al arrancar la app para que siempre parezcan recientes.
from datetime import datetime, timedelta, timezone  # noqa: E402

_ahora = datetime.now(timezone.utc)

ALERTAS = [
    {"id": "ejemplo-tsuru", "nombre": "Nissan Tsuru", "carroceria": "sedán", "version": "GS II", "transmision": "manual",
     "tamano": "compacto", "anio_modelo": "2015", "color": "Blanco",
     "senas_particulares": "Calcomanía de un águila en el medallón y golpe en la salpicadera izquierda.",
     "placas": "De Baja California, terminación 47.",
     "descripcion": "Lo dejé estacionado afuera del trabajo y al salir ya no estaba. Si lo ves, no te acerques ni enfrentes a nadie: avísame por aquí.",
     "zona_referencia": "Centro, cerca del Parque Teniente Guerrero", "municipio": "Tijuana",
     "visto_por_ultima_vez": _ahora - timedelta(hours=3), "creada_en": _ahora - timedelta(hours=2, minutes=40),
     "expira_en": _ahora + timedelta(days=30), "latitud_aprox": 32.51, "longitud_aprox": -117.04,
     "mostrar_telefono": True, "estado": "activa", "foto": "tsuru.jpg", "personas_avisadas": 148,
     "emisor": {"nombre_publico": "Mariana (ejemplo)", "creado_en": _ahora - timedelta(days=210),
                "nivel_verificacion": "registrada"}},
    {"id": "ejemplo-silverado", "nombre": "Chevrolet Silverado", "carroceria": "pickup", "version": "LT doble cabina", "transmision": "automática",
     "tamano": "grande", "anio_modelo": "2012", "color": "Negro",
     "senas_particulares": "Tapa rígida en la caja y faro derecho estrellado.",
     "placas": "Sin placa delantera.",
     "descripcion": "Se la llevaron de la cochera durante la madrugada. Trae herramienta de trabajo en la caja.",
     "zona_referencia": "Playas de Tijuana, por el Malecón", "municipio": "Tijuana",
     "visto_por_ultima_vez": _ahora - timedelta(days=1, hours=5), "creada_en": _ahora - timedelta(days=1, hours=4),
     "expira_en": _ahora + timedelta(days=29), "latitud_aprox": 32.53, "longitud_aprox": -117.12,
     "mostrar_telefono": False, "estado": "activa", "foto": "silverado.jpg", "personas_avisadas": 96,
     "emisor": {"nombre_publico": "Familia Ortega (ejemplo)", "creado_en": _ahora - timedelta(days=45),
                "nivel_verificacion": "identidad_verificada"}},
]
