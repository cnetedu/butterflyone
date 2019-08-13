SECRET_KEY = 'secret'
PROJECT_ID = 'moonlit-cistern-243518'
CLOUDSQL_USER = 'root'
CLOUDSQL_PASSWORD = 'password1234'
CLOUDSQL_DATABASE = 'mydb'


class DirectConfig(object):
    SECRET_KEY = SECRET_KEY
    SQLALCHEMY_DATABASE_URI = (
    'mysql+pymysql://{user}:{password}@35.229.32.91:3306/{database}').format(
        user=CLOUDSQL_USER, password=CLOUDSQL_PASSWORD,
        database=CLOUDSQL_DATABASE)


class AppEngineConfig(object):
    SECRET_KEY = SECRET_KEY
    SQLALCHEMY_DATABASE_URI = (
    'mysql+pymysql://{user}:{password}@localhost/{database}'
    '?unix_socket=/cloudsql/moonlit-cistern-243518:us-east1:bflyone').format(
        user=CLOUDSQL_USER, password=CLOUDSQL_PASSWORD,
        database=CLOUDSQL_DATABASE)

class LocalConfig(object):
    SECRET_KEY = SECRET_KEY
    def __init__(self, sql_file_path):
        self.SQLALCHEMY_DATABASE_URI = (
            'sqlite:///' + sql_file_path
        )
