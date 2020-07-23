import pymysql
import logging
import sys
import configparser


class Database:
    """
    This class contains specific functions related to DB.
    Authors: May Steinfeld & Sheryl Sitruk
    """
    def __init__(self, sql_password, sql_user):
        """
        This function connect to the MYSQL database
        """
        try:
            self.config = configparser.ConfigParser(interpolation=None)
            self.config.read('Constants')
            self.connection = pymysql.connect(host=self.config['Constant']['HOST'], user=sql_user,
                                              password=sql_password,
                                              charset=self.config['Constant']['CHARSET'],
                                              cursorclass=pymysql.cursors.DictCursor)
            logging.info(self.config['SQL']['SQL_READY'])
        except RuntimeError:
            logging.critical(self.config['SQL']['SQL_FAIL'])
            sys.exit(int(self.config['Constant']['EXIT']))

    def create_db(self):
        """
        This function runs the queries to create the database and tables
        """
        try:
            # TODO: think maybe drop DB if exist- > maybe ask the user
            cur = self.connection.cursor()
            sql_query = self.config['SQL_QUERIES']['CREATE_DB']
            cur.execute(sql_query)
            logging.info(self.config['SQL']['SQL_DB_CREATION'])
            sql_query = self.config['SQL_QUERIES']['USE_DB']
            cur.execute(sql_query)
            self.create_company_table(cur)
            self.create_job_table(cur)
            self.create_job_location_table(cur)
            self.create_company_competitors_table(cur)
            logging.info(self.config['SQL']['SQL_TABLE_CREATION'])
        except pymysql.Error:
            logging.critical(self.config['SQL']['SQL_FAIL_TABLE'])
            self.connection.rollback()
            self.connection.close()
            sys.exit(int(self.config['Constant']['EXIT']))

    def create_job_table(self, cur):
        """
        Create the job table
        :param cur: connection cursor
        """
        #TODO: DElete location
        # TODO: think maybe drop table if exist
        sql_create_job_table = self.config['SQL_QUERIES']['CREATE_JOB_TABLE']
        # TODO: deal description to take just keywords
        cur.execute(sql_create_job_table)

    def create_job_location_table(self, cur):
        # TODO: add table for all locations of jobs and try to add address from maps API
        """
        Create the job location table
        :param cur: connection cursor
        """
        # TODO: think maybe drop table if exist
        sql_create_job_location_table = self.config['SQL_QUERIES']['CREATE_JOB_LOCATION_TABLE']
        cur.execute(sql_create_job_location_table)

    def create_company_table(self, cur):
        """
        Create the company table
        :param cur: connection cursor
        """
        # TODO: think maybe drop table if exist
        sql_create_company_table = self.config['SQL_QUERIES']['CREATE_COMPANY_TABLE']
        cur.execute(sql_create_company_table)

    def create_company_competitors_table(self, cur):
        """
        Create the competitor table
        :param cur: connection cursor
        """
        # TODO: think maybe drop table if exist
        sql_create_company_competitors_table = self.config['SQL_QUERIES']['CREATE_COMPETITOR_TABLE']
        cur.execute(sql_create_company_competitors_table)

    def insert_company(self, company):
        """
        Insert information into company table
        """
        try:
            with self.connection.cursor() as cur:
                sql_insert_company_table = self.config['SQL_QUERIES']['INSERT_COMPANY_TABLE']
                cur.execute(sql_insert_company_table, [company.get_name(),
                                                       company.get_company_size(), company.get_company_rating(),
                                                       company.get_company_founded(),
                                                       company.get_company_industry(), company.get_company_sector(),
                                                       company.get_company_type(),
                                                       company.get_company_revenue(),
                                                       company.get_company_headquarters()])
                self.connection.commit()
                logging.info(self.config['SQL']['INSERT_COMPANY'])
        except pymysql.Error:
            logging.exception(self.config['SQL']['COMPANY_INSERT_FAIL'])

    def insert_competitor(self, competitor, company):
        """
        Insert information into competitor table
        """
        try:
            with self.connection.cursor() as cur:
                sql_insert_competitors_table = self.config['SQL_QUERIES']['INSERT_COMPETITOR_TABLE']
                cur.execute(sql_insert_competitors_table, [company.get_name(),
                                                           competitor])
                self.connection.commit()
                logging.info(self.config['SQL']['INSERT_COMPETITOR'])
        except pymysql.Error:
            logging.exception(self.config['SQL']['COMPETITOR_INSERT_FAIL'])

    def insert_job(self, job):
        """
            Insert information into job table
        """
        try:
            with self.connection.cursor() as cur:
                sql_insert_job_table = self.config['SQL_QUERIES']['INSERT_JOB_TABLE']
                cur.execute(sql_insert_job_table, [job.get_title(), job.get_description(),
                                                   job.get_publication_date(), job.get_company_name()])
                self.connection.commit()
                logging.info(self.config['SQL']['INSERT_JOB'])
        except pymysql.Error:
            logging.exception(self.config['SQL']['JOB_INSERT_FAIL'])

    def insert_job_location(self, google_api_info):
        """
            Insert information into job location table
        """
        try:
            with self.connection.cursor() as cur:
                sql_insert_job_location_table = self.config['SQL_QUERIES']['INSERT_JOB_LOCATION_TABLE']
                cur.execute(sql_insert_job_location_table, [google_api_info.get_address_google(),
                                                            google_api_info.get_longitude_google(),
                                                            google_api_info.get_latitude_google()])
                self.connection.commit()
                logging.info(self.config['SQL']['INSERT_JOB_LOCATION'])
        except pymysql.Error:
            logging.exception(self.config['SQL']['JOB_LOCATION_INSERT_FAIL'])

    def get_company(self, company_name):
        """
            Return True if company_name already in company table, else False
        """
        with self.connection.cursor() as cur:
            sql_get_company = self.config['SQL_QUERIES']['GET_COMPANY']
            cur.execute(sql_get_company, company_name)
            result = cur.fetchone()
            logging.info(self.config['General']['GET_INFO_DB'])
            if result:
                return True
        return False

    def close_connection_database(self):
        """
        This function close the DB connection
        :return:
        """
        try:
            self.connection.cursor().close()
            self.connection.close()
            logging.info(self.config['General']['CLOSE_CONNECTION'])
        except pymysql.Error:
            logging.critical(self.config['General']['CLOSE_CONNECTION_FAIL'])
            sys.exit(int(self.config['Constant']['EXIT']))
