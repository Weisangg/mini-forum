from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto") # schemes превращает пароль в хэшированый и auto то что при обнавлении старые даные перепишуться под новые

def password_hash(password):
    return pwd_context.hash(password)

def password_verify(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)