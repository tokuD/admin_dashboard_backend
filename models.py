from database import Base
from sqlalchemy import (
    Boolean,
    Column,
    String,
    Integer,
)


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String)
    email = Column(String, unique=True)
    hashed_password = Column(String)
    is_stuff = Column(Boolean, default=False)
