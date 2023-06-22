import os
from configparser import ConfigParser

config = ConfigParser()
config.read('alembic.ini')
config.set('alembic', 'sqlalchemy.url', os.environ['DATABASE_URL'])

with open('alembic.ini', 'w') as configfile:
    config.write(configfile)
