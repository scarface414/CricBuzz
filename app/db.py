from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base , sessionmaker

from schemas import dbSettings 

# engine = create_engine("postgresql://postgres:abcd@localhost:5432/TestDB" , echo=True)

config = dbSettings()
connection_string = "postgresql://{}:{}@localhost:5432/{}".format(config.user , config.password , config.database)

engine = create_engine(connection_string , echo=True)
Base = declarative_base()

Session = sessionmaker()