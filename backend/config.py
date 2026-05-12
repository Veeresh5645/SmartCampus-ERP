class Config:
    SECRET_KEY = 'smartcampus-secret-key'

    SQLALCHEMY_DATABASE_URI = 'sqlite:///smartcampus.db'

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    JWT_SECRET_KEY = 'jwt-secret-key'