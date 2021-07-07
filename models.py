from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.types import String, Integer, Text
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.schema import Column, ForeignKey
import uuid
import os

engine = create_engine(os.environ['DB'], echo=False)
Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()

class User(Base):
    __tablename__ = 'user'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = Column(String(255), nullable=False, unique=True)
    password = Column(Text())

class File(Base):
    __tablename__ = 'file'
    id = Column(String(50), primary_key=True, default=uuid.uuid4)
    name = Column(String(50))
    size = Column(Integer)
    type = Column(String(50))
    location = Column(Text())
    user_id = Column(UUID(as_uuid=True), ForeignKey('user.id'), nullable=False)

Base.metadata.create_all(engine)

