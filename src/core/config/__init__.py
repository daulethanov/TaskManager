class Config:
    JWT_SECRET_KEY = "secret"
    JWT_ALGORITHM = "HS256"

    POSTGRES_USER = "user"
    POSTGRES_PASSWORD = "password"
    POSTGRES_HOST = "localhost"
    POSTGRES_PORT = 5432
    POSTGRES_DB = "mydatabase"

    @property
    def SQLALCHEMY_DATABASE_URI(self) -> str:
        return (f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@"
                f"{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}")


cfg = Config()
