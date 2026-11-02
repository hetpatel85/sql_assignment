"""
config.py
---------
MySQL connection settings, used by load_data.py, the notebooks and app.py.

The password is NOT written here. It is read from .streamlit/secrets.toml:
    MYSQL_PASSWORD = "your-mysql-password"
That file is listed in .gitignore, so the password is never uploaded to GitHub.
"""

import os
import tomllib
from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.engine import URL

PROJECT_DIR = Path(__file__).resolve().parent
SECRETS_FILE = PROJECT_DIR / ".streamlit" / "secrets.toml"


def read_secret(name: str, default=None):
    """Read a private setting from .streamlit/secrets.toml, or from an environment variable."""
    if SECRETS_FILE.exists():
        with open(SECRETS_FILE, "rb") as f:
            secrets = tomllib.load(f)
        if name in secrets:
            return secrets[name]
    return os.environ.get(name, default)


DB_CONFIG = {
    "host": "localhost",
    "port": 3306,
    "user": "root",
    "password": read_secret("MYSQL_PASSWORD", ""),
    "database": "hospital_readmission",
}


def get_engine(with_database: bool = True):
    """
    Returns a SQLAlchemy engine connected to MySQL.
    with_database=False connects to the MySQL server only
    (needed before the database itself has been created).
    """
    url = URL.create(
        drivername="mysql+pymysql",
        username=DB_CONFIG["user"],
        password=DB_CONFIG["password"],
        host=DB_CONFIG["host"],
        port=DB_CONFIG["port"],
        database=DB_CONFIG["database"] if with_database else None,
    )
    return create_engine(url, pool_pre_ping=True)
