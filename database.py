from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import create_engine


engine = create_engine('postgresql://postgres:Dotaimba2121@localhost/challenge_db', echo=True)


Base = declarative_base()
SessionLocal = sessionmaker(bind=engine)    

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()