from app.db.database import SessonLocal


def get_db():
    db = SessonLocal()

    try:
        yield db
    finally:
        db.close()