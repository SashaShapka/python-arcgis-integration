import psycopg2
import argparse
from arc_gis_python_job.config import DB_NAME, PASSWORD, USER


def drop_db(cursor, db_name, user):
    sql_drop_database = f"DROP DATABASE {db_name};"
    sql_reassign_owned = f"REASSIGN OWNED BY {user} TO postgres;"
    sql_drop_owned = f"DROP OWNED BY {user};"
    sql_drop_role = f"DROP ROLE {user};"

    try:
        cursor.execute(sql_drop_database)
        cursor.execute(sql_reassign_owned)
        cursor.execute(sql_drop_owned)
        cursor.execute(sql_drop_role)
    except Exception as e:
        print(e.__str__())
        raise


def create_database(cursor, db_name, user):
    sql_create_table = f"CREATE database {db_name};"
    sql_crete_user = f"CREATE USER {user} WITH PASSWORD '{PASSWORD}';"
    sql_privileges = f"GRANT ALL PRIVILEGES ON DATABASE {db_name} TO {user};"
    sql_alter = f"ALTER DATABASE {db_name} OWNER TO {user};"

    try:
        cursor.execute(sql_create_table)
        cursor.execute(sql_crete_user)
        cursor.execute(sql_privileges)
        cursor.execute(sql_alter)
    except Exception as e:
        print(e.__str__())
        raise


def create_db(drop=False):
    db_name = DB_NAME
    user = USER

    # establish the connection
    conn = psycopg2.connect(
        database="postgres",
        user="postgres",
        password="postgres",
        host="127.0.0.1",
        port="5432",
    )

    conn.autocommit = True

    # Creating a cursor object using the cursor() method
    cursor = conn.cursor()

    if drop:
        drop_db(cursor, db_name, user)

    create_database(cursor, db_name, user)

    print("Database created successfully........")

    # Closing the connection
    conn.close()


def extend_db_by_models():
    from arcgis_python_db.db import ArcGisPythonDB

    ArcGisPythonDB(create_all=True)


def get_arguments():
    parser = argparse.ArgumentParser(description="database_management")
    # parser.add_argument("--test", help="the test database creation", default=False)
    parser.add_argument("--drop", help="delete the db before creating", default=True)
    args = parser.parse_args()
    return args


if __name__ == "__main__":
    args = get_arguments()
    create_db(drop=args.drop)
    extend_db_by_models()