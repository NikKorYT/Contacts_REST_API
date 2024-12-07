from fastapi_mail import ConnectionConfig, FastMail, MessageSchema 
from config.general import settings

mail_conf = ConnectionConfig(
    MAIL_USERNAME=settings.mail_username,
    MAIL_PASSWORD=settings.mail_password,
    MAIL_FROM=settings.mail_from,
    MAIL_PORT=settings.mail_port,
    MAIL_SERVER=settings.mail_server,
    MAIL_STARTTLS=False,  # Changed from True
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=False  # Changed from True since MailHog doesn't need auth
)

async def send_verification_email(email: str, email_body: str):
    message = MessageSchema(
        subject="Email Verification",
        recipients=[email],
        body=email_body,
        subtype="html",
    )
    fm = FastMail(mail_conf)
    await fm.send_message(message)