from passlib.context import CryptContext


passwd_tool = CryptContext(schemes=['bcrypt'], deprecated='auto')


def gen_password(passwd):
    return passwd_tool.hash(passwd)


def verify_password(passwd, hashed_passwd):
    return passwd_tool.verify(passwd, hashed_passwd)