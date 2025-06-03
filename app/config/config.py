class Config(object):
    MONGO_DB_USER = 'user-name'
    MONGO_DB_PASSWORD = 'password'
    MONGO_DB_URI = 'mongodb+srv://' + MONGO_DB_USER + ':' + MONGO_DB_PASSWORD + '@cluster0.n5nwjp3.mongodb.net/'
    MONGO_DB_NAME = 'db-name'

app_config = Config