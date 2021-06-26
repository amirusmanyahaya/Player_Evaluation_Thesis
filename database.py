import os

from sqlalchemy import create_engine
from sqlalchemy import text


def create_connection(user: str, password: str, host: str, database: str):
    """
    Creates a `database connection`.
    Args:
        user: The username used to access the database
        password: The password used to access the database
        host: The host for the database
        database: The name of the database

    Returns: connection

    """
    engine = create_engine(
        f"mysql+mysqlconnector://{user}:{password}@{host}/{database}", echo=False
    )
    return engine


if __name__ == "__main__":
    engine = create_connection(
        user=os.environ["db_user"],
        password=os.environ["db_pass"],
        host=os.environ["db_host"],
        database=os.environ["db_name"],
    )
    with engine.begin() as connection:
        query = text("describe play_by_play_events")
        result = connection.execute(query).fetchall()
        attributes = [row[0] for row in result]
        print(attributes)
