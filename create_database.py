import pymysql
import command_args
import constants as cst
import logging
from company import Company


# TODO: Try catch for all db and also all the project
# TODO: put in constant SQL queries

class Database:
    def __init__(self):
        """
        This function connect to the MYSQL database
        """
        self.connection = pymysql.connect(host=cst.HOST, user=command_args.args.database_user,
                                          password=command_args.args.database_password,
                                          charset=cst.CHARSET,
                                          cursorclass=pymysql.cursors.DictCursor)
        logging.info("Connection with MYSQL ready")

    def create_db(self):
        """
        This function runs the queries to create the database
        """

        # TODO: think maybe drop table if exist
        cur = self.connection.cursor()
        sql_query = "CREATE DATABASE IF NOT EXISTS glassdoor;"
        cur.execute(sql_query)
        logging.info("Database was created successfully")
        sql_query = "USE glassdoor;"
        cur.execute(sql_query)
        self.create_job_table(cur)
        self.create_company_table(cur)
        sql_alter_job_table = "ALTER TABLE job ADD FOREIGN KEY (company_id) REFERENCES company (company_id);"
        cur.execute(sql_alter_job_table)
        sql_alter_job_table = "ALTER TABLE job ADD UNIQUE KEY (job_title,company_id);"
        cur.execute(sql_alter_job_table)
        logging.info("Tables were created successfully")

        # sql_query = "SHOW DATABASES"
        # cur.execute(sql_query)
        # result = cur.fetchall()
        # logging.debug(result)

    def create_job_table(self, cur):
        """
        Create the job table
        :param cur: connection cursor
        """
        # TODO: think maybe drop table if exist
        sql_create_job_table = """
        CREATE TABLE IF NOT EXISTS job (
        job_id int PRIMARY KEY NOT NULL AUTO_INCREMENT,
        job_title varchar(255) NOT NULL,
        job_description text NOT NULL,
        job_location varchar(255) NOT NULL,
        job_publication_date date NOT NULL,
        company_id int NOT NULL
        );
        """
        # TODO: check how to deal description and also find unique to title+company
        cur.execute(sql_create_job_table)

    def create_company_table(self, cur):
        """
        Create the company table
        :param cur: connection cursor
        """
        # TODO: think maybe drop table if exist
        # TODO: compare all fields type to be the same in DB/Class/DB Design
        sql_create_company_table = """
        CREATE TABLE IF NOT EXISTS company (
        company_id int PRIMARY KEY NOT NULL AUTO_INCREMENT,
        company_name varchar(255) UNIQUE NOT NULL,
        company_size varchar(255),
        company_rating float,
        company_founded int,
        company_industry varchar(255),
        company_sector varchar(255),
        company_type varchar(255),
        company_revenue varchar(255),
        company_headquarters varchar(255)
        );
        """
        # TODO: how to do competitors and location
        cur.execute(sql_create_company_table)

    def insert_company(self, company=None, flag_finish_page=False):
        """
        Insert information into company table
        """
        with self.connection.cursor() as cur:
            if not flag_finish_page:
                # TODO: if key already in the database just update mysql
                # TODO: when problem with insert or something rollback
                sql_insert_company_table = """INSERT INTO company (company_name, company_size, company_rating, 
                company_founded, company_industry, company_sector, company_type, company_revenue, 
                company_headquarters) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE 
                company_id=company_id """
                cur.execute(sql_insert_company_table, [company.get_name(),
                                                       company.get_company_size(), company.get_company_rating(),
                                                       company.get_company_founded(),
                                                       company.get_company_industry(), company.get_company_sector(),
                                                       company.get_company_type(),
                                                       company.get_company_revenue(),
                                                       company.get_company_headquarters()])
                # TODO: have problem with insert type, revenue, headquarters
            else:
                self.connection.commit()
            #logging.info("MySQL connection is closed.")
            # TODO: critical you would do sys.exit next

    def insert_job(self, job=None, flag_finish_page=False):
        with self.connection.cursor() as cur:
            if not flag_finish_page:
                # TODO: if key already in the database just update mysql
                # TODO: when problem with insert or something rollback
                #TODO: What to do with the foregin key company id
                sql_insert_job_table = """INSERT INTO job (job_title, job_description, job_location, 
                job_publication_date, company_id) VALUES (%s, %s, %s, %s, (SELECT company_id FROM company WHERE 
                company_name = %s)) ON DUPLICATE KEY UPDATE job_id=job_id """
                cur.execute(sql_insert_job_table, [job.get_title(), job.get_description(), job.get_location(),
                                                   job.get_publication_date(), job.get_company_name()])
            else:
                self.connection.commit()

            # TODO: critical you would do sys.exit next
            #logging.info("MySQL connection is closed.")


    # TODO: Where to close connetcion or cur self.connection.close()

    def create_job_location_table(self):
        pass

    def create_company_competitors_table(self):
        pass  # TODO: insert to companies id not there else just update