

class Settings:
    BASE_URL: str = "https://qtext.io"
    EXPIRE_COOKIE: int = 60*60*24  # 1 day
    EXPIRE_CACHE: int = 60 * 15  # 15 minutes
    MAX_CACHED_ITEMS: int = 10000
    DATE_FORMAT: str = '%H:%M:%S'


settings = Settings()
