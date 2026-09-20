from pydantic import BaseModel, PostgresDsn


class PostgresClientTestConfig(BaseModel):
    dsn: PostgresDsn
    echo: bool = True
