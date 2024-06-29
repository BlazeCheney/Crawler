from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URI = 'mssql+pyodbc://sa:666666@localhost/Crawler?driver=ODBC+Driver+17+for+SQL+Server'
engine = create_engine(DATABASE_URI)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
