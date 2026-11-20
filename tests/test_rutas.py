"""
Pruebas de las páginas en MODO DE EJEMPLO (sin Supabase).
Ejecutar desde la carpeta del proyecto con:  python -m pytest -v
"""
import os
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app  # noqa: E402


@pytest.fixture
def cliente():
    # Forzamos el modo de ejemplo aunque tu .env tenga Supabase configurado,
    # para que estas pruebas no dependan de internet.
    app.config.update(TESTING=True, SUPABASE_URL="", SUPABASE_CLAVE_PUBLICA="")
    with app.test_client() as c:
        yield c


@pytest.mark.parametrize("ruta", [
    "/", "/comprar", "/robados-y-recuperados", "/agencias", "/comunidad", "/creditos",
    "/acerca", "/iniciar-sesion", "/registro", "/privacidad", "/carro/1",
])
def test_paginas_cargan(cliente, ruta):
    respuesta = cliente.get(ruta)
    assert respuesta.status_code == 200
    assert "Ruedas" in respuesta.get_data(as_text=True)


def test_sin_aviso_modo_ejemplo(cliente):
    # El aviso "Modo de ejemplo" se quitó de la página a petición.
    assert "Modo de ejemplo" not in cliente.get("/").get_data(as_text=True)


def test_pagina_inexistente_da_404(cliente):
    assert cliente.get("/no-existe").status_code == 404
    assert cliente.get("/carro/9999").status_code == 404


def test_catalogo_no_mezcla_robados(cliente):
    html = cliente.get("/comprar").get_data(as_text=True)
    assert "Nissan Kicks" not in html  # está robado, no en venta
    assert "Toyota Camry" in html


def test_robados_solo_muestra_robados_y_recuperados(cliente):
    html = cliente.get("/robados-y-recuperados").get_data(as_text=True)
    assert "Nissan Kicks" in html
    assert "Toyota Camry" not in html


def test_filtro_carroceria(cliente):
    html = cliente.get("/comprar?carroceria=camioneta").get_data(as_text=True)
    assert "Suzuki Jimny" in html
    assert "Toyota Camry" not in html


def test_filtro_invalido_se_ignora(cliente):
    html = cliente.get("/comprar?carroceria=<script>alert(1)</script>").get_data(as_text=True)
    assert "<script>alert(1)</script>" not in html
    assert "Toyota Camry" in html  # muestra todo, como si no hubiera filtro


def test_agencia_no_verificado_no_muestra_insignia(cliente):
    html = cliente.get("/agencias").get_data(as_text=True)
    assert "Pendiente de verificación" in html
    assert html.count("Agencia verificada</span>") == 1  # solo la agencia de ejemplo aprobado


def test_cabeceras_de_seguridad(cliente):
    r = cliente.get("/")
    assert r.headers["X-Content-Type-Options"] == "nosniff"
    assert r.headers["X-Frame-Options"] == "SAMEORIGIN"
