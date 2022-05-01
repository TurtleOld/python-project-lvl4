from .base import * # noqa F405
import dj_database_url
import os

load_dotenv() # noqa F405

DATABASE_URL = os.getenv('DATABASE_URL')

DATABASES = {'default': dj_database_url.config(conn_max_age=600)}

DEBUG = False
