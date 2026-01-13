from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,declarative_base


DB_URL = "mysql+pymysql://root:root@localhost/smart_support_desk"

engine = create_engine(DB_URL, echo=True)
Sessionlocal = sessionmaker(autoflush=False,autocommit = False,bind=engine)

Base = declarative_base()