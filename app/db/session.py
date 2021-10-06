import contextlib

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


@contextlib.contextmanager
def ManagedSession():
    """Get a session object whose lifecycle, commits and flush are managed for you.
    Expected to be used as follows:
    ```
    with ManagedSession() as session:            # multiple db_operations are done within one session.
        db_operations.select(session, **kwargs)  # db_operations is expected not to worry about session handling.
        db_operations.insert(session, **kwargs)  # after the with statement, the session commits to the database.
    ```
    """

    session = ScopedSession()
    try:
        yield session
        session.commit()
        session.flush()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()
