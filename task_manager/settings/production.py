from .base import *
import dj_database_url

load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')

DATABASES = {'default': dj_database_url.config(conn_max_age=600)}

DEBUG = False
