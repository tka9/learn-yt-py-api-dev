from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_hostname: str     
    database_port: str
    database_name: str    
    database_username: str 
    database_password: str 
    secret_key: str 
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 60

    class Config:
        env_file = ".env"
    
settings = Settings()