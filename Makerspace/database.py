#######################################################################
# database
#
# single connecting point to database
#
# REFERENCES
# [1] https://dev.mysql.com/doc/connector-python/en/connector-python-api-errors-error.html
#######################################################################
import mysql.connector
from mysql.connector import errorcode


# connect to makerspace database
# returns the connection and the cursor
def connect_to_database():
    try:
        database_connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",  # TODO: add your password here
            database="makerspace"
        )
    except database_connection.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("invalid user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("database does not exist")
        else:
            print(err)

    database_cursor = database_connection.cursor()
    return database_connection, database_cursor


if __name__ == '__main__':
    # EXAMPLE to show database connection
    mydb, cursor = connect_to_database()
    print(f"is connected: {mydb.is_connected()}")
