import os
import redis

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

redis_host = os.getenv('REDIS_HOST', 'localhost')
redis_port = os.getenv('REDIS_PORT', 6379)
redis_password = os.getenv('REDIS_PASSWORD', None)

jwt_blacklist = redis.StrictRedis(
    host=redis_host,
    port=redis_port,
    password=redis_password,
    decode_responses=True,
    db=0
    )
