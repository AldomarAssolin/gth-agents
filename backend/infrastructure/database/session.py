from app.extensions import db


def SessionLocal():
    return db.session
