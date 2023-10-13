import psycopg2
from psycopg2 import sql

# Database connection parameters
db_params = {
    "dbname": "dbzd6zvga0uwb1",
    "user": "ummddmrjsbtuu",
    "password": "r&dd:*$8#}12",
    "host": "35.209.4.107",  # Change to your PostgreSQL host
    "port": "5432"        # Change to your PostgreSQL port
}

# SQL statement to create a table
create_table_query = """
    CREATE TABLE IF NOT EXISTS my_table (
        id serial PRIMARY KEY,
        name VARCHAR(255),
        age INT
    );
"""

def create_table():
    try:
        # Connect to the PostgreSQL database
        print(db_params)
        conn = psycopg2.connect(**db_params)

        print('debug')
        print(db_params)
        # Create a cursor object to interact with the database
        cursor = conn.cursor()

        # Execute the CREATE TABLE query
        cursor.execute(create_table_query)

        # Commit the transaction
        conn.commit()

        print("Table created successfully!")

    except (Exception, psycopg2.Error) as error:
        print("Error creating table:", error)
    finally:
        # Close the cursor and database connection
        if conn:
            cursor.close()
            conn.close()

if __name__ == "__main__":
    create_table()
