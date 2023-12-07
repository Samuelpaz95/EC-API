from sqlalchemy import Column, Integer, String

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

    @property
    def password(self):
        return self.__password

    @password.setter
    def password(self, plain_password):
        self.__password = plain_password
