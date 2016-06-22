from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from flask import g
from contextlib import contextmanager

DATABASE = 'database.db'
engine = create_engine('sqlite:///'+DATABASE)
Base = declarative_base()
# engine = create_engine('mysql://root:root@localhost/Blog')

Session = sessionmaker(bind=engine)

class CricketBase(object):

    def __repr__(self):
        return '{}<{}>'.format(self.__class__, self.__dict__)

    def as_dict(self, columns=None):
        if not columns:
            columns = [c.name for c in self.__table__.columns]
        model_dict = {column: getattr(self, column) for column in columns}
        return model_dict

def create_all():
    metadata = Base.metadata
    tables = metadata.sorted_tables
    tables_name = [table.name for table in tables]
    metadata.create_all(bind=engine)

def drop_all():
    metadata = Base.metadata
    tables = metadata.sorted_tables
    tables_name = [table.name for table in tables]
    metadata.drop_all(bind=engine)

@contextmanager
def scoped_session():
    try:
        session = Session()
        yield session
        session.commit()
    except Exception:
        print "Error occured while conencting to the database"
        session.rollback()
        raise
    finally:
        session.close()