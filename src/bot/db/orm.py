from src.bot.db import session_factory, Feedback, Base, engine


def insert_feedback(feedback: str) -> None:
    feedback = Feedback(feedback=feedback)
    with session_factory() as session:
        session.add_all([feedback])
        session.commit()


def create_tables() -> None:
    with session_factory() as session:
        Base.metadata.create_all(engine)


def delete_tables() -> None:
    with session_factory() as session:
        Base.metadata.drop_all(engine)