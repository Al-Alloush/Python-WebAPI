APP_SECRET_KEY = "the secret key"

# to avoid error: ModuleNotFoundError: No module named 'MySQLdb'
# need to install pymysql library to update/add 'MySQLdb' module 
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:my-pass@mysql/default_db'