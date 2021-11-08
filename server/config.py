import os
from sqlalchemy.dialects import registry

basedir = os.path.abspath(os.path.dirname(__file__))
db_base = 'cockroachdb://kavish:erKaCOuWe-zIMxPe@free-tier.gcp-us-central1.cockroachlabs.cloud:26257/second-jaguar' \
          '-3728.defaultdb?sslmode=verify-full&sslrootcert=root.crt'


class BaseConfig:
    """Base configuration."""
    SECRET_KEY = os.getenv('SECRET_KEY', 'your_super_secret_key')
    DEBUG = False
    BCRYPT_LOG_ROUNDS = 12
    registry.register("cockroachdb", "cockroachdb.sqlalchemy.dialect",
                      "CockroachDBDialect")
    SQLALCHEMY_DATABASE_URI = db_base
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(BaseConfig):
    """Development configuration."""
    registry.register("cockroachdb", "cockroachdb.sqlalchemy.dialect",
                      "CockroachDBDialect")
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = db_base


class TestingConfig(BaseConfig):
    """Testing configuration."""
    DEBUG = True
    TESTING = True
    BCRYPT_LOG_ROUNDS = 4
    # using in-memory sqlite database to execute tests
    SQLALCHEMY_DATABASE_URI = "sqlite://"
    PRESERVE_CONTEXT_ON_EXCEPTION = False


class ProductionConfig(BaseConfig):
    """Production configuration."""
    registry.register("cockroachdb", "cockroachdb.sqlalchemy.dialect",
                      "CockroachDBDialect")
    SECRET_KEY = 'your_super_secret_key'
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = db_base
