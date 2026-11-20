"""
Estados de un carro en Ruedas.

Cada estado tiene: texto visible, icono (Bootstrap Icons) y clase de color.
Se definen en un solo lugar para que todas las pantallas usen las mismas insignias.
"""

ESTADOS = {
    "disponible": {"texto": "En venta", "icono": "bi-tag-fill", "clase": "estado-disponible"},
    "en_proceso": {"texto": "En trato", "icono": "bi-hourglass-split", "clase": "estado-proceso"},
    "vendido": {"texto": "Vendido", "icono": "bi-check-circle-fill", "clase": "estado-vendido"},
    "en_consignacion": {"texto": "En consignación", "icono": "bi-shop", "clase": "estado-consignacion"},
    "robado": {"texto": "Robado", "icono": "bi-search", "clase": "estado-robado"},
    "recuperado": {"texto": "Recuperado", "icono": "bi-geo-alt", "clase": "estado-recuperado"},
    "en_taller": {"texto": "En taller", "icono": "bi-wrench", "clase": "estado-taller"},
    "urgente": {"texto": "Urge vender", "icono": "bi-lightning-charge-fill", "clase": "estado-urgente"},
}

# Estados que aparecen en el catálogo de VENTA.
# Robados y recuperados tienen su propia sección: no se mezclan con las ventas.
ESTADOS_CATALOGO = ["disponible", "urgente", "en_proceso", "en_consignacion", "en_taller"]

# Estados de la sección "Robados y recuperados".
ESTADOS_ROBADOS = ["robado", "recuperado"]
