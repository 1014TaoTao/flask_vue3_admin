from flask import Flask
from flask_caching import Cache

cache = Cache(config={
    'CACHE_TYPE': 'simple',
})


def init_cache(app: Flask) -> None:
    """缓存中间件"""
    cache.init_app(app=app)
