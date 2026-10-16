
from sqlalchemy import create_engine
from sqlalchemy.engine import URL
DB_CONFIG = {
    "host": "localhost",
    "port": 3306,
    "user": "root",
    "password": "password",  
    "database": "hospital_readmission",
}
# ------------------------------------------------------------------


def get_engine(with_database: bool = True):
    url = URL.create(
        drivername="mysql+pymysql",
        username=DB_CONFIG["user"],
        password=DB_CONFIG["password"],
        host=DB_CONFIG["host"],
        port=DB_CONFIG["port"],
        database=DB_CONFIG["database"] if with_database else None,
    )
    return create_engine(url, pool_pre_ping=True)
