import pymysql
import command_args
import constants as cst
import logging


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
        self.create_company_competitors_table(cur)
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
        # TODO: deal description to take just keywords
        cur.execute(sql_create_job_table)

    def create_company_table(self, cur):
        """
        Create the company table
        :param cur: connection cursor
        """
        # TODO: think maybe drop table if exist
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

        # alter table job according to company
        sql_alter_job_table = "ALTER TABLE job ADD FOREIGN KEY (company_id) REFERENCES company (company_id);"
        cur.execute(sql_alter_job_table)
        sql_alter_job_table = "ALTER TABLE job ADD UNIQUE KEY (job_title,company_id,job_location);"
        cur.execute(sql_alter_job_table)

    def create_company_competitors_table(self, cur):
        # TODO: think maybe drop table if exist
        sql_create_company_competitors_table = """
        CREATE TABLE IF NOT EXISTS company_competitors (
        company_id int NOT NULL,
        competitor_id int NOT NULL
        );
        """
        # TODO: how to do competitors and location
        cur.execute(sql_create_company_competitors_table)

        sql_alter_competitors_table = "ALTER TABLE company_competitors ADD FOREIGN KEY (company_id) REFERENCES company (company_id);"
        cur.execute(sql_alter_competitors_table)
        sql_alter_competitors_table = "ALTER TABLE company_competitors ADD FOREIGN KEY (competitor_id) REFERENCES company (company_id);"
        cur.execute(sql_alter_competitors_table)
        sql_alter_competitors_table = "ALTER TABLE company_competitors ADD UNIQUE KEY (company_id,competitor_id);"
        cur.execute(sql_alter_competitors_table)

    def insert_company(self, company):
        """
        Insert information into company table
        """
        with self.connection.cursor() as cur:
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
            self.connection.commit()
            # logging.info("MySQL connection is closed.")
            # TODO: critical you would do sys.exit next

    def insert_competitor(self, competitor, company):
        with self.connection.cursor() as cur:
            sql_insert_competitors_table = """INSERT INTO company_competitors (company_id, competitor_id) 
            VALUES ((SELECT company_id FROM company WHERE
            company_name = % s), (SELECT company_id FROM company WHERE
            company_name = % s)) ON DUPLICATE KEY UPDATE 
            company_id=company_id """
            cur.execute(sql_insert_competitors_table, [company.get_name(),
                                                       competitor])
            self.connection.commit()

    def insert_job(self, job):
        with self.connection.cursor() as cur:
            # TODO: when problem with insert or something rollback
            sql_insert_job_table = """INSERT INTO job (job_title, job_description, job_location, 
            job_publication_date, company_id) VALUES (%s, %s, %s, %s, (SELECT company_id FROM company WHERE 
            company_name = %s)) ON DUPLICATE KEY UPDATE job_id=job_id """
            cur.execute(sql_insert_job_table, [job.get_title(), job.get_description(), job.get_location(),
                                               job.get_publication_date(), job.get_company_name()])
            self.connection.commit()

            # TODO: critical you would do sys.exit next
            # logging.info("MySQL connection is closed.")

    def get_company(self, company_name):
        with self.connection.cursor() as cur:
            sql_insert_job_table = """(SELECT company_id FROM company WHERE company_name = %s)"""
            cur.execute(sql_insert_job_table, company_name)
            result = cur.fetchone()
            if result:
                return True

            # TODO: Where to close connetcion or cur self.connection.close()
        return False



    # TODO: Where to close connetcion or cur self.connection.close()

    def create_job_location_table(self):
        pass
