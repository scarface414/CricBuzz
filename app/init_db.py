from db import engine , Base
from models import Match,Team

Base.metadata.create_all(bind = engine)