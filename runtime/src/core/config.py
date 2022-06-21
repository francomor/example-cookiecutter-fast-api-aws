import os
import secrets


def getenv_boolean(var_name, default_value=False):
    result = default_value
    env_value = os.getenv(var_name)
    if env_value is not None:
        result = env_value.upper() in ("TRUE", "1")
    return result


API_PREFIX = os.getenv("API_PREFIX", '')
API_V1_STR = "/api/v1"

SECRET_KEY = os.getenv("SECRET_KEY", default=secrets.token_urlsafe(32))

ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 8  # 60 minutes * 24 hours * 8 days = 8 days

BACKEND_CORS_ORIGINS = os.getenv(
    "BACKEND_CORS_ORIGINS"
)  # a string of origins separated by commas, e.g:
# "http://localhost, http://localhost:4200, http://localhost:3000,
# http://localhost:8080, http://local.dockertoolbox.tiangolo.com"
PROJECT_NAME = os.getenv("PROJECT_NAME", "example-project")

# same default parameters as docker-composer mysql service
MYSQL_SERVER = os.getenv("MYSQL_SERVER", 'localhost')
MYSQL_USER = os.getenv("MYSQL_USER", 'user')
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", 'password')
MYSQL_DB = os.getenv("MYSQL_DB", 'database_name')
SQLALCHEMY_DATABASE_URI = (
    f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_SERVER}/{MYSQL_DB}"
)

FIRST_SUPERUSER = os.getenv("FIRST_SUPERUSER", 'admin@example.com')
FIRST_SUPERUSER_PASSWORD = os.getenv("FIRST_SUPERUSER_PASSWORD", 'admin12345')

USERS_OPEN_REGISTRATION = getenv_boolean("USERS_OPEN_REGISTRATION", True)
