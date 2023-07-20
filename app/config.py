from os import environ

class SingletonMeta(type):
    """
    Singleton meta class.
    """

    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class Config(metaclass=SingletonMeta):
    """
    Config for projects application.
    """

    def __init__(self):
        self.base_url = environ.get("BASE_URL", "/")
        self.pg_host = environ.get("PG_HOST")
        self.pg_port = environ.get("PG_PORT", 5432)
        self.pg_user = environ.get("PG_USER")
        self.pg_pwd = environ.get("PG_PWD")
        self.pg_db = environ.get("PG_DB")

    @property
    def postgres_uri(self):
        """
        Mongo uri.
        """

        return f"postgresql+asyncpg://{self.pg_user}:{self.pg_pwd}@{self.pg_host}:{self.pg_port}/{self.pg_db}"


    @property
    def settings(self):
        """
        Get dict-config
        """

        return {
            "postgres": self.postgres_uri,
            "pg_host": self.pg_host,
            "pg_port": self.pg_port,
            "pg_user": self.pg_user,
            "pg_pwd": self.pg_pwd,
            "pg_db": self.pg_db,
        }


def get_settings():
    if environ.get("LOCAL_ENV", "false") == "true":
        from app.settings import settings

        return settings
    else:
        return Config().settings
