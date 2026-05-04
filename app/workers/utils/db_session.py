from app.db.database import SessionLocal
def get_db_session():
    """
    Returns a fresh SQLAlchemy session. 
    Ensure SessionLocal in app.db.session is configured 
    with your PostgreSQL 'agent_db' URL.
    """
    db = SessionLocal()
    try:
        return db
    except Exception as e:
        db.close()
        print(f"Error creating worker DB session: {e}")
        raise