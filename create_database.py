import pymysql
import command_args
from constants import CONSTANT_DICT
import logging


# Connect to the database
class Database:
    def __init__(self):
        self.connection = pymysql.connect(host=CONSTANT_DICT['HOST'], user=command_args.args.database_user,
                                          password=command_args.args.database_password,
                                          charset=CONSTANT_DICT['CHARSET'],
                                          cursorclass=pymysql.cursors.DictCursor)

    def create_db(self):
        # TODO: think maybe drop table if exist
        cur = self.connection.cursor()
        sql_query = "CREATE DATABASE IF NOT EXISTS glassdoor;"
        cur.execute(sql_query)
        logging.info("Database was created successfully")
        sql_query = "USE glassdoor;"
        cur.execute(sql_query)
        self.create_job_table(cur)
        self.create_company_table(cur)
        logging.info("Tables were created successfully")

        # sql_query = "SHOW DATABASES"
        # cur.execute(sql_query)
        # result = cur.fetchall()
        # logging.debug(result)

        # cur.close()

    def create_job_table(self, cur):
        sql_create_job_table = """
            CREATE TABLE IF NOT EXISTS Job (
            job_id int PRIMARY KEY NOT NULL AUTO_INCREMENT,
            job_title varchar(255) NOT NULL,
            job_description text NOT NULL,
            job_location varchar(255) NOT NULL,
            job_publication_date datetime NOT NULL,
            company_id int NOT NULL
            );
            """
        # TODO: check how to deal description
        cur.execute(sql_create_job_table)

    def create_company_table(self, cur):
        sql_create_company_table = """
            CREATE TABLE IF NOT EXISTS Company (
            company_id int PRIMARY KEY NOT NULL AUTO_INCREMENT,
            company_name varchar(255) UNIQUE NOT NULL,
            company_size varchar(255),
            company_rating int,
            company_founded year,
            company_industry varchar(255),
            company_sector varchar(255),
            company_type varchar(255),
            company_revenue varchar(255),
            company_headquarters varchar(255)
            );
            """
        cur.execute(sql_create_company_table)
        sql_alter_company_table = "ALTER TABLE Job ADD FOREIGN KEY (company_id) REFERENCES Company (company_id);"
        cur.execute(sql_alter_company_table)

        logging.info("MySQL connection is closed.")
        cur.close()

    def create_job_location_table(self):
        pass

    def create_company_competitors_table(self):
        pass

    def save_page_companies(self):
        pass

    def save_page_jobs(self):
        pass
