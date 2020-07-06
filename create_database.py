import pymysql
import command_args
from constants import CONSTANT_DICT
import logging
from company import Company


#TODO: put in constant SQL queries
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
        # TODO: think maybe drop table if exist
        sql_create_job_table = """
        CREATE TABLE IF NOT EXISTS job (
        job_id int PRIMARY KEY NOT NULL AUTO_INCREMENT,
        job_title varchar(255) NOT NULL,
        job_description text NOT NULL,
        job_location varchar(255) NOT NULL,
        job_publication_date datetime NOT NULL,
        company_id int NOT NULL
        );
        """
        # TODO: check how to deal description and also find unique to title+company
        cur.execute(sql_create_job_table)

    def create_company_table(self, cur):
        # TODO: think maybe drop table if exist
        sql_create_company_table = """
        CREATE TABLE IF NOT EXISTS company (
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
        #TODO: how to do competitors and location
        cur.execute(sql_create_company_table)
        sql_alter_company_table = "ALTER TABLE job ADD FOREIGN KEY (company_id) REFERENCES company (company_id);"
        cur.execute(sql_alter_company_table)

        logging.info("MySQL connection is closed.")
        cur.close()

    def insert_company(self, company=None, flag_finish_page=False):
        with self.connection.cursor() as cur:
            if not flag_finish_page:
                sql_create_company_table = """INSERT INTO company (company_name, company_size, company_rating, 
                company_founded, company_industry, company_sector, company_type, company_revenue, 
                company_headquarters) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)"""
                print(company)
                cur.execute(sql_create_company_table, [company.get_name(),
                                                       company.get_company_size(), company.get_company_rating(),
                                                       company.get_company_founded(),
                                                       company.get_company_industry(), company.get_company_sector(),
                                                       company.get_company_type(),
                                                       company.get_company_revenue(),
                                                       company.get_company_headquarters()])
            else:
                cur.commit()
            cur.close()
            # TODO: critical you would do sys.exit next

    def create_job_location_table(self):
        pass

    def create_company_competitors_table(self):
        pass #TODO: insert to companies id not there else just update

    def save_page_jobs(self):
        pass
