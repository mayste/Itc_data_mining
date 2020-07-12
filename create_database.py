import pymysql
import command_args
import constants as cst
import logging
import sql_queries as sql
import text_messages as tm
import sys


class Database:
    def __init__(self):
        """
        This function connect to the MYSQL database
        """
        try:
            self.connection = pymysql.connect(host=cst.HOST, user=command_args.args.database_user,
                                              password=command_args.args.database_password,
                                              charset=cst.CHARSET,
                                              cursorclass=pymysql.cursors.DictCursor)
            logging.info(tm.SQL_READY)
        except RuntimeError:
            logging.critical(tm.SQL_FAIL)
            sys.exit(cst.EXIT)

    def create_db(self):
        """
        This function runs the queries to create the database
        """
        try:
            # TODO: think maybe drop DB if exist- > maybe ask the user
            cur = self.connection.cursor()
            sql_query = sql.CREATE_DB
            cur.execute(sql_query)
            logging.info(tm.SQL_DB_CREATION)
            sql_query = sql.USE_DB
            cur.execute(sql_query)
            self.create_job_table(cur)
            self.create_company_table(cur)
            self.create_company_competitors_table(cur)
            logging.info(tm.SQL_TABLE_CREATION)
        except pymysql.Error:
            logging.critical(tm.SQL_FAIL_TABLE)
            self.connection.rollback()
            self.connection.close()
            sys.exit(cst.EXIT)

    def create_job_table(self, cur):
        """
        Create the job table
        :param cur: connection cursor
        """
        # TODO: think maybe drop table if exist
        sql_create_job_table = sql.CREATE_JOB_TABLE
        # TODO: deal description to take just keywords
        cur.execute(sql_create_job_table)

    def create_company_table(self, cur):
        """
        Create the company table
        :param cur: connection cursor
        """
        # TODO: think maybe drop table if exist
        sql_create_company_table = sql.CREATE_COMPANY_TABLE
        cur.execute(sql_create_company_table)

        # alter table job according to company
        sql_alter_job_table = sql.ALTER_JOB_TABLE_1
        cur.execute(sql_alter_job_table)
        sql_alter_job_table = sql.ALTER_JOB_TABLE_2
        cur.execute(sql_alter_job_table)

    def create_company_competitors_table(self, cur):
        """
        Create the competitor table
        :param cur: connection cursor
        """
        # TODO: think maybe drop table if exist
        sql_create_company_competitors_table = sql.CREATE_COMPETITOR_TABLE
        cur.execute(sql_create_company_competitors_table)

        sql_alter_competitors_table = sql.ALTER_COMPETITOR_TABLE_1
        cur.execute(sql_alter_competitors_table)
        sql_alter_competitors_table = sql.ALTER_COMPETITOR_TABLE_2
        cur.execute(sql_alter_competitors_table)
        sql_alter_competitors_table = sql.ALTER_COMPETITOR_TABLE_3
        cur.execute(sql_alter_competitors_table)

    def insert_company(self, company):
        """
        Insert information into company table
        """
        try:
            with self.connection.cursor() as cur:
                sql_insert_company_table = sql.INSERT_COMPANY_TABLE
                cur.execute(sql_insert_company_table, [company.get_name(),
                                                       company.get_company_size(), company.get_company_rating(),
                                                       company.get_company_founded(),
                                                       company.get_company_industry(), company.get_company_sector(),
                                                       company.get_company_type(),
                                                       company.get_company_revenue(),
                                                       company.get_company_headquarters()])
                self.connection.commit()
                logging.info(tm.INSERT_COMPANY)
        except pymysql.Error:
            logging.exception(tm.COMPANY_INSERT_FAIL)

    def insert_competitor(self, competitor, company):
        """
        Insert information into competitor table
        """
        try:
            with self.connection.cursor() as cur:
                sql_insert_competitors_table = sql.INSERT_COMPETITOR_TABLE
                cur.execute(sql_insert_competitors_table, [company.get_name(),
                                                           competitor])
                self.connection.commit()
                logging.info(tm.INSERT_COMPETITOR)
        except pymysql.Error:
            logging.exception(tm.COMPETITOR_INSERT_FAIL)

    def insert_job(self, job):
        """
            Insert information into job table
        """
        try:
            with self.connection.cursor() as cur:
                sql_insert_job_table = sql.INSERT_JOB_TABLE
                cur.execute(sql_insert_job_table, [job.get_title(), job.get_description(), job.get_location(),
                                                   job.get_publication_date(), job.get_company_name()])
                self.connection.commit()
                logging.info(tm.INSERT_JOB)
        except pymysql.Error:
            logging.exception(tm.JOB_INSERT_FAIL)

    def get_company(self, company_name):
        """
            Return True if company_name already in company table, else False
        """
        with self.connection.cursor() as cur:
            sql_get_company = sql.GET_COMPANY
            cur.execute(sql_get_company, company_name)
            result = cur.fetchone()
            logging.info(tm.GET_INFO_DB)
            if result:
                return True
        return False

    def close_connection_database(self):
        try:
            self.connection.cursor().close()
            self.connection.close()
            logging.info(tm.CLOSE_CONNECTION)
        except pymysql.Error:
            logging.critical(tm.CLOSE_CONNECTION_FAIL)
            sys.exit(cst.EXIT)

    def create_job_location_table(self):
        #TODO: add table for all locations of jobs and try to add address from maps API
        pass
