import mysql.connector as cn
import os


def create_connection(user: str, password: str, host: str, database: str) -> cn.connect:
    """
    Creates a `database connection`. if the connection fails,
    an error string is displayed
    Args:
        user: The username used to access the database
        password: The password used to access the database
        host: The host for the database
        database: The name of the database

    Returns: connection

    """
    try:
        connection = cn.connect(host=host,
                         database=database,
                         user=user,
                         password=password)
        if connection.is_connected():
            info = connection.get_server_info()
            print(f"Connected to MySQL server version {info}")
            cursor = connection.cursor()
            cursor.execute("select database();")
            record = cursor.fetchone()
            print(f"your are connected to databse: {record}")
            return connection
    except cn.Error as err:
        print(f"Error while connecting to the database: {err}")


if __name__ == "__main__":
    connection = create_connection(user=os.environ["db_user"],
                                   password=os.environ["db_pass"],
                                   host=os.environ["db_host"],
                                   database=os.environ["db_name"])
    cursor = connection.cursor()
    cursor.execute("select AwayPlayer1, HomePlayer1 from play_by_play_events")
    record = cursor.fetchone()
    print(record)
