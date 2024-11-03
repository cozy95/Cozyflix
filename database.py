from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import DATABASE_URL

Base = declarative_base()
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)

class Video(Base):
    __tablename__ = 'videos'
    
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    file_path = Column(String, nullable=False)
    added_by = Column(String, nullable=False)

def init_db():
    Base.metadata.create_all(engine)