from sqlmodel import create_engine, SQLModel, Session, text
import os

DB_URL = "sqlite:///rank_flux.db"
# Enable WAL mode for high-speed concurrent logging
engine = create_engine(DB_URL, connect_args={"check_same_thread": False})

def init_db():
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        # Enable WAL via PRAGMA
        session.exec(text("PRAGMA journal_mode=WAL;"))
        session.commit()

def get_session():
    return Session(engine)
