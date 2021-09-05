import psycopg2
from psycopg2.extras import Json
import json


class AvailabilityDao:
    """ Derived from https://github.com/aiven/aiven-examples/blob/master/postgresql/python/main.py"""
    """ Create table method derived from https://www.postgresqltutorial.com/postgresql-python/create-tables/"""

    def __init__(self, service_uri, table_name):
        self.service_uri = service_uri
        self.table_name = table_name

        self.cursor = None
        self.db_conn = None
        self.initialize_connection()
        self.create_table_if_not_exist()

    def save(self, availability_items):
        args_str = ((x.website_url, x.status_code, x.response_time, Json(x.regex_pattern_matches)) for x in
                    availability_items)

        self.cursor.executemany("INSERT INTO " + self.table_name +
                                """(website_url, status_code, response_time, regex_pattern_matches)
                                VALUES (%s, %s, %s, %s)""",
                                args_str)

        # self.db_conn.commit()

    def fetch_all_test(self):
        print("Fetching all:")
        self.cursor.execute("SELECT * FROM " + self.table_name + ";")
        result = self.cursor.fetchall()
        [print(x) for x in result]

    def close_connection(self):
        self.cursor.close()
        self.db_conn.close()

    def initialize_connection(self):
        self.db_conn = psycopg2.connect(self.service_uri)
        self.cursor = self.db_conn.cursor()
        self.cursor.execute("SELECT current_database()")

        result = self.cursor.fetchone()
        print("Successfully connected to: {}".format(result[0]))

    def create_table_if_not_exist(self):
        self.cursor.execute(
            """
                SELECT EXISTS (
                   SELECT FROM information_schema.tables 
                   WHERE table_name   = '""" + self.table_name + """'
                );
            """
        )
        if not self.cursor.fetchone():
            print("Table :" + self.table_name + " did not exist, creating.")
            self.create_table()

    def create_table(self):
        """ Derived from https://www.postgresqltutorial.com/postgresql-python/create-tables/"""
        command = """
            CREATE TABLE """ + self.table_name + """ (
                id SERIAL PRIMARY KEY,
                website_url VARCHAR(255) NOT NULL,
                status_code INTEGER NOT NULL,
                response_time INTEGER NOT NULL,
                regex_pattern_matches JSONB
            )
            """
        try:
            self.cursor.execute(command)
            self.db_conn.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
