from sqlalchemy.orm import Session


class DBSessionContext(object):
    def __init__(self, db: Session = None):
        self.db = db

    def __enter__(self):
        return self.db

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            self.db.rollback()
        else:
            self.db.commit()


class AppService(DBSessionContext):
    pass


class AppCrud(DBSessionContext):
    pass
