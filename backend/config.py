import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key-ppa')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///ppa.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'jwt-secret-key-ppa')
    
    # Celery Redis config
    CELERY_BROKER_URL = 'redis://localhost:6379/0'
    CELERY_RESULT_BACKEND = 'redis://localhost:6379/1'
    
    # Caching config
    CACHE_TYPE = 'RedisCache'
    CACHE_REDIS_URL = 'redis://localhost:6379/2'
    CACHE_DEFAULT_TIMEOUT = 300
