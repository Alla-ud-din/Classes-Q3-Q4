from starlette.config import Config  
from starlette.datastructures import Secret
# as fastApi is build on starlette so whenever we install fastApi starlette automatically installed
try:
    config = Config('.env')
except FileNotFoundError:
    config = Config()

DATABASE_URL = config("DATABASE_URL", cast=Secret)