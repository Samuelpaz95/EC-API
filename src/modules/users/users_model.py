from passlib.context import CryptContext
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.hybrid import hybrid_property

from src.config.database import Base


class UserDB(Base):
    __tablename__ = "users"

    id: Column[int] = Column(Integer, primary_key=True, index=True)
    first_name: Column[str] = Column(String(100))
    last_name: Column[str] = Column(String(100))
    email: Column[str] = Column(
        String(255), unique=True, index=True, nullable=False)
    username: Column[str] = Column(String(100), unique=True, index=True)
    __password: Column[str] = Column(String(255), name="password")
    phone_number: Column[str] = Column(String(15))
    address: Column[str] = Column(String(100))

    @hybrid_property
    def password(self):  # type: ignore
        return '*' * 8

    @password.setter  # type: ignore
    def password(self, plain_password):
        pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        self.__password = Column(pwd_context.hash(plain_password))

    def verify_password(self, plain_password):
        pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        return pwd_context.verify(plain_password, str(self.__password))
