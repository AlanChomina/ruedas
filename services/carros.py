"""
Consultas de carros y agencias.

Si Supabase está configurado en .env, los datos vienen de la base de datos.
Si no, se usan los datos de ejemplo (modo de ejemplo), para que la app
siga funcionando mientras configuras Supabase.

Las plantillas reciben siempre diccionarios con la misma forma, vengan de
donde vengan, así que no tienen que cambiar.
"""
import uuid

from services import datos_ejemplo
from services.estados import ESTADOS_CATALOGO, ESTADOS_ROBADOS
from services.supabase_cliente import obtener_cliente, supabase_configurado

LIMITE_RESULTADOS = 60  # se reemplazará por paginación en la Etapa 4

CAMPOS_CARRO = (
    "id,nombre,carroceria,version,kilometraje,tamano,transmision,combustible,detalles,"
    "servicios_al_dia,unico_dueno,zona,municipio,estado,publicado_en"
)
CAMPOS_AGENCIA = "id,nombre,descripcion,zona,municipio,estado_verificacion"


class ErrorBaseDeDatos(Exception):
    """No se pudo consultar Supabase."""


def modo_ejemplo():
    return not supabase_configurado()


# ---------------------------------------------------------------------------
# Conversión de filas de la base de datos al formato de las plantillas
# ---------------------------------------------------------------------------
def texto_kilometraje(km):
    if km is None:
        return "Kilometraje desconocido"
    return f"{km:,} km"


def fila_a_carro(fila):
    return {
        "id": fila["id"],
        "nombre": fila["nombre"],
        "carroceria": fila["carroceria"],
        "version": fila.get("version") or "No especificada",
        "kilometraje": texto_kilometraje(fila.get("kilometraje")),
        "tamano": fila["tamano"],
        "transmision": fila.get("transmision") or "desconocida",
        "combustible": fila.get("combustible") or "",
        "detalles": fila.get("detalles") or "",
        "servicios_al_dia": bool(fila.get("servicios_al_dia")),
        "unico_dueno": bool(fila.get("unico_dueno")),
        "zona": fila["zona"],
        "estado": fila["estado"],
        "foto": None,  # se llena con _con_fotos() a partir de carros_fotos
    }


def fila_a_agencia(fila):
    return {
        "id": fila["id"],
        "nombre": fila["nombre"],
        "descripcion": fila.get("descripcion") or "",
        "zona": fila.get("zona") or fila.get("municipio") or "",
        "verificado": fila["estado_verificacion"] == "verificado",
        "carros": None,  # el conteo se agregará con el panel de agencia
    }


def _foto_principal(ruta):
    """Por ahora solo se aceptan nombres de archivo simples (ej. "camry.jpg")
    que existan en static/images/carros/. Las fotos subidas a Supabase Storage
    llegarán en la Etapa 4."""
    ruta = (ruta or "").strip()
    if not ruta or "/" in ruta or "\\" in ruta or ".." in ruta:
        return {}
    return {"foto": ruta}


def _con_fotos(filas):
    """Pasa las filas a carros y les agrega su primera foto (tabla carros_fotos).

    Si la consulta de fotos falla, los carros se muestran sin foto
    en lugar de romper la página.
    """
    carros = [fila_a_carro(f) for f in filas]
    ids = [str(c["id"]) for c in carros]
    if not ids:
        return carros
    try:
        fotos_filas = (obtener_cliente().table("carros_fotos")
                       .select("carro_id,ruta_archivo,orden")
                       .in_("carro_id", ids).order("orden").execute().data) or []
    except Exception:
        return carros
    primera = {}
    for f in fotos_filas:
        primera.setdefault(str(f.get("carro_id")), f.get("ruta_archivo"))
    for c in carros:
        c.update(_foto_principal(primera.get(str(c["id"]))))
    return carros


def _ejecutar(consulta):
    try:
        return consulta.execute().data
    except Exception as error:  # red, clave inválida, tabla inexistente…
        raise ErrorBaseDeDatos(str(error)) from error


# ---------------------------------------------------------------------------
# Consultas públicas
# ---------------------------------------------------------------------------
def consulta_catalogo(filtros):
    """Construye (sin ejecutar) la consulta del catálogo. Separada para poder probarla."""
    consulta = (obtener_cliente().table("carros").select(CAMPOS_CARRO)
                .in_("estado", ESTADOS_CATALOGO))
    for campo, valor in filtros.items():
        consulta = consulta.eq(campo, valor)
    return consulta.order("publicado_en", desc=True).limit(LIMITE_RESULTADOS)


def listar_catalogo(filtros):
    """Carros para compra. `filtros` ya viene validado por app.py."""
    if modo_ejemplo():
        en_catalogo = [a for a in datos_ejemplo.CARROS if a["estado"] in ESTADOS_CATALOGO]
        return [a for a in en_catalogo if all(a.get(c) == v for c, v in filtros.items())]
    return _con_fotos(_ejecutar(consulta_catalogo(filtros)))


def listar_destacados(cantidad=4):
    if modo_ejemplo():
        return [a for a in datos_ejemplo.CARROS if a["estado"] in ("disponible", "urgente")][:cantidad]
    consulta = (obtener_cliente().table("carros").select(CAMPOS_CARRO)
                .in_("estado", ["urgente", "disponible"])
                .order("publicado_en", desc=True).limit(cantidad))
    return _con_fotos(_ejecutar(consulta))


def listar_robados_recuperados():
    if modo_ejemplo():
        return [a for a in datos_ejemplo.CARROS if a["estado"] in ESTADOS_ROBADOS]
    consulta = (obtener_cliente().table("carros").select(CAMPOS_CARRO)
                .in_("estado", ESTADOS_ROBADOS)
                .order("publicado_en", desc=True).limit(LIMITE_RESULTADOS))
    return _con_fotos(_ejecutar(consulta))


def obtener_carro(carro_id):
    """Un carro por su id, o None si no existe o no es visible."""
    if modo_ejemplo():
        return next((a for a in datos_ejemplo.CARROS if str(a["id"]) == str(carro_id)), None)
    try:
        uuid.UUID(str(carro_id))  # en la base de datos los id son UUID
    except ValueError:
        return None
    consulta = (obtener_cliente().table("carros").select(CAMPOS_CARRO)
                .eq("id", carro_id).limit(1))
    filas = _ejecutar(consulta)
    return _con_fotos(filas[:1])[0] if filas else None


def listar_agencias():
    if modo_ejemplo():
        return datos_ejemplo.AGENCIAS
    consulta = (obtener_cliente().table("agencias").select(CAMPOS_AGENCIA)
                .in_("estado_verificacion", ["verificado", "pendiente"])
                .order("nombre").limit(LIMITE_RESULTADOS))
    return [fila_a_agencia(f) for f in _ejecutar(consulta)]
