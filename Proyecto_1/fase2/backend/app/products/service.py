"""Catalog business logic.

This layer knows nothing about HTTP: it takes plain values, raises plain
exceptions and returns plain objects, which is what makes it unit testable
without starting a server.
"""

import json
import logging
import os
from decimal import Decimal

import redis
from sqlalchemy.orm import Session

from app.products import repository
from app.products.models import Product

logger = logging.getLogger(__name__)

# --- Cache de productos por EAN (Redis) ----------------------------------
#
# La "pizarra compartida": vive en su propio contenedor (store-N-redis), no
# en el proceso del backend. Cada producto se guarda como JSON bajo la clave
# "product:{ean}", con expiración automática (TTL) manejada por el propio
# Redis.
PRODUCT_CACHE_TTL_SECONDS = 60
PRODUCT_CACHE_KEY_PREFIX = "product:"

_redis_client = redis.Redis.from_url(
    os.environ["REDIS_URL"],
    decode_responses=True,  # nos devuelve str en vez de bytes
)


class ProductNotFoundError(Exception):
    """No product carries the requested barcode."""

    def __init__(self, ean: str) -> None:
        super().__init__(f"No product found for EAN {ean}")
        self.ean = ean


def _cache_key(ean: str) -> str:
    return f"{PRODUCT_CACHE_KEY_PREFIX}{ean}"


# Recibe un objeto producto, por lo general desde el repositorio, y
# lo transforma en JSON para guardarlo en la caché como string.
def _product_to_cache_value(product: Product) -> str:
    """Serializa solo los campos que el cajero necesita ver."""
    return json.dumps(
        {
            "ean": product.ean,
            "name": product.name,
            "price": str(product.price),
        }
    )


# Recibe un string en formato JSON e inicializa un objeto Product con esos
# atributos. Devuelve ese producto.
def _cache_value_to_product(raw: str) -> Product:
    data = json.loads(raw)
    return Product(
        ean=data["ean"],
        name=data["name"],
        price=Decimal(data["price"]),
    )


def get_product(session: Session, ean: str) -> Product:
    """Return the product for this barcode, or raise ProductNotFoundError.

    Checks Redis first. On a miss, falls back to the repository, then stores
    the result in Redis before returning it.
    """
    cached = _redis_client.get(_cache_key(ean))
    if cached is not None:
        logger.info("Cache HIT for EAN %s", ean)
        return _cache_value_to_product(cached)

    logger.info("Cache MISS for EAN %s, querying database", ean)
    product = repository.find_product_by_ean(session, ean)
    if product is None:
        raise ProductNotFoundError(ean)

    # Guarda el producto en JSON (como string) bajo la clave del EAN, con
    # expiración automática después de PRODUCT_CACHE_TTL_SECONDS segundos.
    _redis_client.setex(
        _cache_key(ean),
        PRODUCT_CACHE_TTL_SECONDS,
        _product_to_cache_value(product),
    )

    return product


def get_products_by_eans(session: Session, eans: list[str]) -> dict[str, Product]:
    """Return the requested products keyed by EAN, omitting unknown ones.

    The payment package prices a cart through this rather than reaching into
    the catalog's repository, so package talks to package at the service
    level.
    """
    return repository.find_products_by_eans(session, eans)