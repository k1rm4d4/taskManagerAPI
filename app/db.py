from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker, scoped_session


engine = None
SessionLocal = None

class Model(DeclarativeBase):
    pass

def init_engine(db_url, **engine_kwargs):
    # engine = create_engine(url=DATABASE_URL, echo= True, future=True)
    global engine, SessionLocal
    engine = create_engine(db_url, **engine_kwargs)
    # SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
    SessionLocal = scoped_session(sessionmaker(bind=engine, autoflush=False, autocommit=False))
    return engine,  SessionLocal

