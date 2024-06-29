from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class News(Base):
    __tablename__ = 'news'

    id = Column(Integer, primary_key=True)
    title = Column(String(255))
    summary = Column(Text)
    url = Column(String(2048), nullable=False)
    date = Column(String(25))  # 假设日期为字符串格式
    content = Column(Text)
    category = Column(String(255))
    source = Column(String(255))
    author = Column(String(255))
    tags = Column(String(255))
