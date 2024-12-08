from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str
    secret_key: str
    mail_username: str = "test"
    mail_password: str = "test"
    mail_from: str = "admin@25web.com"
    mail_port: int = 1025
    mail_server: str = "localhost"
    cloudinary_name: str 
    cloudinary_api_key: str
    cloudinary_api_secret: str

    class Config:
        env_file = ".env"
        extra = "allow"


settings = Settings()
