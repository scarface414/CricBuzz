from schemas import dbSettings 

# engine = create_engine("postgresql://postgres:abcd@localhost:5432/TestDB" , echo=True)

config = dbSettings()
connection_string = "postgresql://{}:{}@localhost:5432/{}".format(config.user , config.password , config.database)
print(connection_string)