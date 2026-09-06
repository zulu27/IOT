"""Catalog business logic.

This layer knows nothing about HTTP: it takes plain values, raises plain
exceptions and returns plain objects, which is what makes it unit testable
without starting a server.
"""

import logging
import threading

from cachetools import TTLCache
from sqlalchemy.orm import Session

from app.products import repository
from app.products.models import Product

logger = logging.getLogger(__name__)

# --- Cache de productos por EAN ------------------------------------------
#
# La "libretita" del mesero: guarda hasta PRODUCT_CACHE_MAXSIZE productos,
# cada uno válido por PRODUCT_CACHE_TTL_SECONDS. Pasado ese tiempo, la entrada
# se considera vencida y se vuelve a consultar la base de datos.
#
# Se protege con un lock porque varias peticiones (varias cajas) pueden
# llegar al mismo tiempo y cachetools no es seguro para uso concurrente sin
# uno.
PRODUCT_CACHE_TTL_SECONDS = 60
PRODUCT_CACHE_MAXSIZE = 512

_product_cache: TTLCache = TTLCache(maxsize=PRODUCT_CACHE_MAXSIZE, ttl=PRODUCT_CACHE_TTL_SECONDS)
_product_cache_lock = threading.Lock()


class ProductNotFoundError(Exception):
    """No product carries the requested barcode."""

    def __init__(self, ean: str) -> None:
        super().__init__(f"No product found for EAN {ean}")
        self.ean = ean


def get_product(session: Session, ean: str) -> Product:
    """Return the product for this barcode, or raise ProductNotFoundError.

    Checks the in-memory cache first. On a miss, falls back to the
    repository, then stores the result before returning it.
    """
    with _product_cache_lock:
        cached = _product_cache.get(ean)
    if cached is not None:
        logger.info("Cache HIT for EAN %s", ean)
        return cached

    logger.info("Cache MISS for EAN %s, querying database", ean)
    product = repository.find_product_by_ean(session, ean)
    if product is None:
        raise ProductNotFoundError(ean)

    # Desconecta el objeto de la sesión antes de guardarlo: así puede vivir
    # en la caché y ser leído en peticiones futuras sin depender de una
    # sesión que ya se cerró. Los valores de sus columnas ya están cargados
    # en memoria, así que leerlos después no dispara ninguna consulta nueva.
    session.expunge(product)

    with _product_cache_lock:
        _product_cache[ean] = product

    return product


def get_products_by_eans(session: Session, eans: list[str]) -> dict[str, Product]:
    """Return the requested products keyed by EAN, omitting unknown ones.

    The payment package prices a cart through this rather than reaching into
    the catalog's repository, so package talks to package at the service
    level.
    """
    return repository.find_products_by_eans(session, eans)