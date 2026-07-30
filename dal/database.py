import pymssql
from contextlib import contextmanager
from config import Config


class Database:
    @staticmethod
    def _connect():
        return pymssql.connect(
            server=Config.DB_SERVER,
            port=Config.DB_PORT,
            user=Config.DB_USER,
            password=Config.DB_PASSWORD,
            database=Config.DB_NAME,
            as_dict=True,
            autocommit=True,
        )

    @staticmethod
    @contextmanager
    def connection():
        """
        Otvara pymssql konekciju sa autocommit=True.
        Transakcije se rjesavaju INSIDE stored procedura (BEGIN TRAN / COMMIT / ROLLBACK
        u TRY/CATCH blokovima) — Python NE upravlja transakcijama.
        """
        conn = Database._connect()
        try:
            yield conn
        finally:
            conn.close()

    @staticmethod
    def query_list(sql, params=None):
        """Izvrsi SQL i vrati listu redova kao dict."""
        with Database.connection() as conn:
            cursor = conn.cursor()
            cursor.execute(sql, params or {})
            try:
                rows = cursor.fetchall()
            except pymssql.OperationalError:
                rows = []
            cursor.close()
            return rows

    @staticmethod
    def query_single(sql, params=None):
        """Izvrsi SQL i vrati prvi red (dict) ili None."""
        rows = Database.query_list(sql, params)
        return rows[0] if rows else None

    @staticmethod
    def execute(sql, params=None):
        """Izvrsi SQL bez ocekivanog rezultata."""
        with Database.connection() as conn:
            cursor = conn.cursor()
            cursor.execute(sql, params or {})
            cursor.close()
