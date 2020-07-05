import pymysql
import command_args
from constants import CONSTANT_DICT
import logging


# Connect to the database
class Database:
    def __init__(self):
        self.connection = pymysql.connect(host=CONSTANT_DICT['HOST'], user=command_args.args.database_user,
                                          password=command_args.args.database_password, charset=CONSTANT_DICT['CHARSET'],
                                          cursorclass=pymysql.cursors.DictCursor)

    def create_db(self):
        try:
            cur = self.connection.cursor()
            sql_query = "CREATE DATABASE IF NOT EXISTS glassdoor"
            cur.execute(sql_query)
            sql_query = "SHOW DATABASES"
            cur.execute(sql_query)
            result = cur.fetchall()
            logging.debug(result)
        except RuntimeError as e:
            logging.exception(e)

        finally:
            cur.close()

    def create_job_table(self):
        with self.connection.cursor() as cur:
            sql_create_job_table = """SELECT MAX(nb_points) AS max_trip, MIN(nb_points) AS min_trip, AVG(nb_points) AS avg_trip 
                        FROM trips"""
            cur.execute(sql_create_job_table)
            result = cur.fetchall()
            print(result)

    def create_company_table(self):
        pass

    def create_job_location_table(self):
        pass

    def create_company_competitors_table(self):
        pass

    def save_page_companies(self):
        pass

    def save_page_jobs(self):
        pass


