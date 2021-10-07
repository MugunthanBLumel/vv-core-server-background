from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from app.conf.config import settings

try:
    engine = create_engine(settings.SQLALCHEMY_DATABASE_URI, echo=False)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    ScopedSession = scoped_session(
        sessionmaker(autocommit=False, autoflush=False, bind=engine)
    )
except Exception as identifier:
    print(identifier)
