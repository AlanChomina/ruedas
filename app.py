"""
Ruedas - "Busca tu carro. Encuentra tu camino."
Aplicación principal de Flask: crea la app y define las rutas.

Para ejecutar en Codespaces:
    flask --app app run --debug
"""
import os

from flask import Flask, abort, render_template, request, session

from config import Config
from services import alertas as servicio_alertas
from services import carros as servicio
from services.creditos_fotos import CREDITOS_FOTOS
from services.datos_ejemplo import PUBLICACIONES
from services.estados import ESTADOS
from services.seguridad import token_csrf, verificar_csrf
from services.sesion import usuario_actual
from rutas_alertas import registrar_rutas_alertas
from rutas_cuentas import registrar_rutas_cuentas

app = Flask(__name__)
app.config.from_object(Config)

# Valores permitidos para los filtros (validación del lado del servidor).
FILTROS_PERMITIDOS = {
    "carroceria": ["sedán", "camioneta", "hatchback", "pickup"],
    "tamano": ["compacto", "mediano", "grande"],
    "transmision": ["automática", "manual"],
    "combustible": ["gasolina", "diésel", "híbrido"],
}

CARPETA_FOTOS = os.path.join(app.static_folder, "images", "carros")


# ---------------------------------------------------------------------------
# Utilidades disponibles en todas las plantillas
# ---------------------------------------------------------------------------
def foto_existe(nombre_archivo):
    """True si la foto está en static/images/carros/."""
    return bool(nombre_archivo) and os.path.isfile(os.path.join(CARPETA_FOTOS, nombre_archivo))


# Disponibles en todas las plantillas, incluidas las macros de componentes.html.
app.jinja_env.globals.update(ESTADOS=ESTADOS, foto_existe=foto_existe, csrf_token=token_csrf)
app.jinja_env.filters["hace_tiempo"] = servicio_alertas.hace_tiempo
app.jinja_env.filters["fecha_local"] = servicio_alertas.fecha_local
app.jinja_env.filters["mes_anio"] = servicio_alertas.mes_anio


@app.context_processor
def variables_de_pagina():
    return {
        # Aviso "modo de ejemplo" mientras Supabase no esté configurado.
        "modo_ejemplo": servicio.modo_ejemplo(),
        # Persona con sesión iniciada (o None) para el menú.
        "usuario_sesion": usuario_actual(),
    }


@app.before_request
def proteger_formularios():
    verificar_csrf()  # todos los formularios POST deben traer el código CSRF


@app.after_request
def cabeceras_seguridad(respuesta):
    """Cabeceras básicas que protegen contra ataques comunes."""
    respuesta.headers["X-Content-Type-Options"] = "nosniff"
    respuesta.headers["X-Frame-Options"] = "SAMEORIGIN"
    respuesta.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    if session.get("usuario"):
        # Páginas con datos personales: que el navegador no las guarde en caché.
        respuesta.headers["Cache-Control"] = "no-store"
    return respuesta


def leer_filtros():
    """Lee los filtros de la URL y descarta cualquier valor no permitido."""
    filtros = {}
    for campo, permitidos in FILTROS_PERMITIDOS.items():
        valor = request.args.get(campo, "").strip().lower()
        if valor in permitidos:
            filtros[campo] = valor
    return filtros


# ---------------------------------------------------------------------------
# Rutas
# ---------------------------------------------------------------------------
@app.route("/")
def inicio():
    return render_template("index.html", destacados=servicio.listar_destacados(),
                           agencias=servicio.listar_agencias()[:3],
                           alertas=servicio_alertas.listar_vigentes()[:3])


@app.route("/comprar")
def catalogo():
    filtros = leer_filtros()
    return render_template("catalogo.html", carros=servicio.listar_catalogo(filtros),
                           filtros=filtros, opciones=FILTROS_PERMITIDOS)


@app.route("/carro/<carro_id>")
def detalle_carro(carro_id):
    carro = servicio.obtener_carro(carro_id)
    if carro is None:
        abort(404)
    return render_template("detalle_carro.html", carro=carro)


@app.route("/robados-y-recuperados")
def robados():
    return render_template("robados.html", carros=servicio.listar_robados_recuperados())


# Alerta Ruedas: lista, detalle, emitir, "Lo vi", mi zona, notificaciones
registrar_rutas_alertas(app)


@app.route("/agencias")
def agencias():
    return render_template("agencias.html", agencias=servicio.listar_agencias())


@app.route("/comunidad")
def comunidad():
    # La comunidad se conecta a la base de datos en la Etapa 6.
    return render_template("comunidad.html", publicaciones=PUBLICACIONES)


@app.route("/acerca")
def acerca():
    return render_template("acerca.html")


# Registro, inicio de sesión, mi cuenta, etc. (Etapa 3)
registrar_rutas_cuentas(app)


@app.route("/privacidad")
def privacidad():
    return render_template("privacidad.html")


@app.route("/creditos")
def creditos():
    # Autores y licencias de las fotos de ejemplo (lo piden sus licencias).
    return render_template("creditos.html", creditos=CREDITOS_FOTOS)


# ---------------------------------------------------------------------------
# Errores
# ---------------------------------------------------------------------------
@app.errorhandler(404)
def pagina_no_encontrada(error):
    return render_template("404.html"), 404


@app.errorhandler(400)
def peticion_invalida(error):
    mensaje = getattr(error, "description", None) or "La petición no es válida."
    return render_template("error.html", titulo="Algo no salió bien", mensaje=mensaje), 400


@app.errorhandler(servicio.ErrorBaseDeDatos)
def error_base_de_datos(error):
    # El detalle técnico va a la terminal; la persona ve un mensaje amable.
    app.logger.error("Error al consultar Supabase: %s", error)
    return render_template("error_conexion.html"), 503


if __name__ == "__main__":
    app.run(debug=Config.RUEDAS_ENV == "development")
