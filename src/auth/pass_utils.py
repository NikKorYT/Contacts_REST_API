from passlib.context import CryptContext

get_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return get_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return get_context.hash(password)
