"""
In this file is going to be everything related to a database connection its
easy to have all the database logic in one class and then import it from
other modules
"""

from sqlalchemy import create_engine
import os

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.dialects import registry

registry.register("cockroachdb", "cockroachdb.sqlalchemy.dialect",
                  "CockroachDBDialect")

# conn_string = "cockroachdb://kavish:erKaCOuWe-zIMxPe@free-tier.gcp-us-central1.cockroachlabs.cloud:26257" \
#                   "/second-jaguar-3728.defaultdb?sslmode=verify-full&sslrootcert=root.crt"
conn_string = "cockroachdb://kavish:erKaCOuWe-zIMxPe@free-tier.gcp-us-central1.cockroachlabs.cloud:26257" \
                  "/second-jaguar-3728.defaultdb?sslmode=disable"
engine = create_engine(os.path.expandvars(conn_string), convert_unicode=True)

session = scoped_session(sessionmaker(autocommit=False,
                                                   autoflush=False,
                                                   bind=engine))
session.verify = True
sessionmaker = sessionmaker(bind=engine)
Base = declarative_base()
Base.query = session.query_property()
